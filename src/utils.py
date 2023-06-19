import logging

from requests import RequestException
from exceptions import ParserFindTagException

from constants import EXPECTED_STATUS


def get_response(session, url):
    """Перехваь ошибки RequestException при получение страници"""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    """Перехват ошибки при поиске тега"""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def find_all_tag(soup, tag, attrs=None):
    """Перехват ошибки при поиске тегов"""
    searched_tags = soup.find_all(tag, attrs=(attrs or {}))
    if not searched_tags:
        error_msg = f'Не найдены теги {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tags


def check_status(card_url, status_pep_card, status_pep_list):
    """Проверка соответствия статуса в общем списке и в карточке PEP"""
    if status_pep_card not in (expect := EXPECTED_STATUS[status_pep_list]):
        info_message = (
            f'Карточка: {card_url}\n'
            f'Статус в карточке: {status_pep_card}\n'
            f'Ожидается {expect}\n'
        )
        return info_message
