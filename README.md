# Проект парсинга pep
## Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=gray)](https://www.python.org/) [![Beautifulsoup4](https://img.shields.io/badge/-Beautifulsoup4-464646?style=flat&logoColor=56C0C0&color=gray)](https://www.crummy.com/software/BeautifulSoup/) [![Prettytable](https://img.shields.io/badge/-Prettytable-464646?style=flat&color=gray)](https://github.com/jazzband/prettytable)

Полный список модулей, используемых в проекте, доступен в [requirements.txt](https://github.com/NECROshizo/bs4_parser_pep/blob/master/requirements.txt)
## Линтеры
[![Flake8](https://img.shields.io/badge/-flake8-464646?style=flat&logo=flake8&logoColor=56C0C0&color=gray)](https://flake8.pycqa.org/)

## Описание проекта
Данный парсер выполняет следующие функции:
- Собират ссылки на статьи о нововведениях в Python, переходить по ним и забирать информацию об авторах и редакторах статей.
- Собират информацию о статусах версий Python.
- Скачиват архив с актуальной документацией.

## Установка и настройки
#### Клонирование репозитория:

```
git clone git@github.com:NECROshizo/bs4_parser_pep.git
```

#### Создание виртуального окружения:

```
python -m venv venv
```

#### Запуск виртуального окружения:

```
source venv/Scripts/activate - команда для Windows
source venv/bin/activate - команда для Linux и macOS
```
#### Установка зависимостей:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## Использование проекта
#### Краткая справка
Для получения краткой справки используете ключь **-h** или **--help**
```
python src/main.py -h
```
Полученное краткое описание
```
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```
#### Режимы работы
- **whats-new** режим собирающий список изменений в python
- **latest-versions** режим собирающий список последних версий и ссылки на них
- **download** режим скачивающий архив с документацией python в формате pdf
- **pep** режим собирающий список статусов PEP и их количество
#### Аргументы
- **-c, --clear-cache**очищает ранее закешируемые страницы
- **-o {pretty,file}, --output {pretty,file}** способ конечного вывода информации
## Примеры работы
#### Команда с выводом в консоль (режим вывода по умолчанию)
```
python src/main.py latest-versions
```
**Полученный результат**
```
Ссылка на документацию Версия Статус
https://docs.python.org/3.13/ 3.13 in development
https://docs.python.org/3.12/ 3.12 pre-release
https://docs.python.org/3.11/ 3.11 stable
https://docs.python.org/3.10/ 3.10 security-fixes
https://docs.python.org/3.9/ 3.9 security-fixes
https://docs.python.org/3.8/ 3.8 security-fixes
https://docs.python.org/3.7/ 3.7 security-fixes
https://docs.python.org/3.6/ 3.6 EOL
https://docs.python.org/3.5/ 3.5 EOL
https://docs.python.org/2.7/ 2.7 EOL
https://www.python.org/doc/versions/ All versions
```
#### Команда c отформатированным выводом в консоль 
```
python src/main.py latest-versions -o pretty
```
**Полученный результат**
```
+--------------------------------------+--------------+----------------+
| Ссылка на документацию               | Версия       | Статус         |
+--------------------------------------+--------------+----------------+
| https://docs.python.org/3.13/        | 3.13         | in development |
| https://docs.python.org/3.12/        | 3.12         | pre-release    |
| https://docs.python.org/3.11/        | 3.11         | stable         |
| https://docs.python.org/3.10/        | 3.10         | security-fixes |
| https://docs.python.org/3.9/         | 3.9          | security-fixes |
| https://docs.python.org/3.8/         | 3.8          | security-fixes |
| https://docs.python.org/3.7/         | 3.7          | security-fixes |
| https://docs.python.org/3.6/         | 3.6          | EOL            |
| https://docs.python.org/3.5/         | 3.5          | EOL            |
| https://docs.python.org/2.7/         | 2.7          | EOL            |
| https://www.python.org/doc/versions/ | All versions |                |
+--------------------------------------+--------------+----------------+
```

#### Команда c записью в фаил 
```
python src/main.py latest-versions -o file
```
**Полученный результат**
Результат записывается в фаил формата csv с указанием даты создания и режима работы ( например latest-versions_2023-06-19_19-59-17)
**Содержание файла**
```
"Ссылка на документацию","Версия","Статус"
"https://docs.python.org/3.13/","3.13","in development"
"https://docs.python.org/3.12/","3.12","pre-release"
"https://docs.python.org/3.11/","3.11","stable"
"https://docs.python.org/3.10/","3.10","security-fixes"
"https://docs.python.org/3.9/","3.9","security-fixes"
"https://docs.python.org/3.8/","3.8","security-fixes"
"https://docs.python.org/3.7/","3.7","security-fixes"
"https://docs.python.org/3.6/","3.6","EOL"
"https://docs.python.org/3.5/","3.5","EOL"
"https://docs.python.org/2.7/","2.7","EOL"
"https://www.python.org/doc/versions/","All versions",""
```
## Автор
[**Оганин Пётр**](https://github.com/NECROshizo) 
2023 г.
