from collections import Counter
import logging
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, MAIN_DOC_URL, PEP_DOC_URL
from constants import Header as head
from constants import LogMessage as lm
from outputs import control_output
from utils import (LatestVersion, NewInfoPep, check_status, find_all_tag,
                   find_tag, get_response)

""" TODO
FAILED tests/test_main.py::test_mode_to_function - AssertionError:
Убедитесь, что в модуле `main.py` в объекте `MODE_TO_FUNCTION` `whats_new`
- это функция.
(；⌣̀_⌣́)
Вынести всю логику парсеров в отдельный parsers.py
а сюда портировать, также непозволяет, так pytest перестает видеть
папку downloads, полагаю из-за того что ненаходит BASE_DIR в main.
MODE_TO_FUNCTION = {
    'whats-new': 'whats_new',
    'latest-versions': 'latest_versions',
    'download': 'download',
    'pep': 'pep',
}
"""


def whats_new(session):
    """Мод whats-new парсер собирает нововедения"""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        logging.info(lm.NO_PARSE.value.format(url=whats_new_url))
        return
    soup = BeautifulSoup(response.text, 'lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = find_all_tag(
        div_with_ul, 'li', attrs={'class': 'toctree-l1'})
    results = [head.WHATS_NEW.value]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            logging.info(lm.NO_PARSE.value.format(url=version_link))
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            NewInfoPep(version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session):
    """Мод latest-versions парсер собирает информацию о последних версиях"""
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        logging.info(lm.NO_PARSE.value.format(url=MAIN_DOC_URL))
        return
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = find_all_tag(sidebar, 'ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = find_all_tag(ul, 'a')
            break
    else:
        raise Exception('Ничего не нашлось')
    result = [head.LATEST_VERSIONS.value]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        pre_match = re.search(pattern, a_tag.text)
        if pre_match:
            version, status = pre_match.groups()
        else:
            version, status = a_tag.text, ''
        result.append(LatestVersion(link, version, status))
    return result


def download(session):
    """Мод download скачивает актуальную документацию"""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        logging.info(lm.NO_PARSE.value.format(url=downloads_url))
        return
    soup = BeautifulSoup(response.text, 'lxml')
    table_tag = find_tag(soup, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(lm.DOWLOAD_ZIP.value.format(path=archive_path))


def pep(session):
    """Мод pep получает информацию о статусах pep и их количестве"""
    response = get_response(session, PEP_DOC_URL)
    if response is None:
        logging.info(lm.NO_PARSE.value.format(url=PEP_DOC_URL))
        return
    soup = BeautifulSoup(response.text, 'lxml')
    section_numerical_index = find_tag(
        soup, 'section', attrs={'id': 'numerical-index'})
    table_body = find_tag(section_numerical_index, 'tbody')
    tr_tags = find_all_tag(table_body, 'tr')
    table_result = Counter()
    discrepancy = list()
    for tr_tag in tqdm(tr_tags):
        td_tags = find_all_tag(tr_tag, 'td')
        status = td_tags[0].text[1:]
        href = td_tags[1].a['href']
        pep_url = urljoin(PEP_DOC_URL, href)
        response = get_response(session, pep_url)
        if response is None:
            logging.info(lm.NO_PARSE.value.format(url=pep_url))
            continue
        new_soup = BeautifulSoup(response.text, 'lxml')
        status_pep_card = find_tag(new_soup, 'abbr')
        if (info := check_status(pep_url, status_pep_card.text, status)):
            discrepancy.append(info)
        table_result.update((status_pep_card.text,))
    if discrepancy:
        logging.info(
           lm.DISCREPANCY_STATUS.value.format(statuses="".join(discrepancy))
        )
    result = [
        head.ALL_STATUS_PEP.value,
        *table_result.items(),
        ('Total', sum(table_result.values()))
    ]
    return result


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info(lm.START_PARSER.value)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(lm.START_ARG.value.format(args=args))
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    # results = eval(MODE_TO_FUNCTION[parser_mode])(session) TODO
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info(lm.END_PARSER.value)


if __name__ == '__main__':
    main()
