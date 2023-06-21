from enum import Enum
from pathlib import Path


BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}


class Header(Enum):
    WHATS_NEW = ('Ссылка на статью', 'Заголовок', 'Редактор, Автор')
    LATEST_VERSIONS = ('Ссылка на документацию', 'Версия', 'Статус')
    ALL_STATUS_PEP = ('Статус', 'Количество')


class LogMessage(Enum):
    NO_PARSE = 'На странице {url} нет необходимой информации.'
    DOWLOAD_ZIP = 'Архив был загружен и сохранён: {path}'
    DISCREPANCY_STATUS = 'Несовпадающие статусы:\n{statuses}'
    SAVE_FILE = 'Файл с результатами был сохранён: {path}'
    START_PARSER = 'Парсер запущен!'
    START_ARG = 'Аргументы командной строки: {args}'
    END_PARSER = 'Парсер завершил работу.'
    ERROR_DOWLOAD_URL = 'Возникла ошибка при загрузке страницы {url}'
    ERROR_TAG_FIND = 'Не найден тег {tag} {attrs}'
    ERROR_TAGS_FIND = 'Не найдены теги {tag} {attrs}'
