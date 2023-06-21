from dataclasses import dataclass
import logging

from exceptions import ParserFindTagException
from requests import RequestException


from constants import EXPECTED_STATUS
from constants import LogMessage as lm


class GenerateForOut:
    """
    Генератор для вывода данных через аргументы:
    -o {pretty,file}, --output {pretty,file}
    """

    def __post_init__(self):
        self.all_field = []
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index == len(self.all_field):
            raise StopIteration
        return self.all_field[self.index]

    def __len__(self):
        return len(self.all_field)


@dataclass
class NewInfoPep(GenerateForOut):
    """Данные о нововедениях"""
    link: str
    header: str
    info: str

    def __post_init__(self):
        self.all_field = [self.link, self.header, self.info]
        self.index = -1


@dataclass
class LatestVersion(GenerateForOut):
    """Данные о версиях"""
    link: str
    version: str
    status: str

    def __post_init__(self):
        self.all_field = [self.link, self.version, self.status]
        self.index = -1


def get_response(session, url):
    """Перехваь ошибки RequestException при получение страници"""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            lm.ERROR_DOWLOAD_URL.value.format(url=url),
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    """Перехват ошибки при поиске тега"""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = lm.ERROR_TAG_FIND.value.format(tag=tag, attrs=attrs)
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def find_all_tag(soup, tag, attrs=None):
    """Перехват ошибки при поиске тегов"""
    searched_tags = soup.find_all(tag, attrs=(attrs or {}))
    if not searched_tags:
        error_msg = lm.ERROR_TAGS_FIND.value.format(tag=tag, attrs=attrs)
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
