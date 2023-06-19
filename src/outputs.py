import csv
import datetime as dt

from prettytable import PrettyTable

import logging

from constants import BASE_DIR, DATETIME_FORMAT


def control_output(results, cli_args):
    """Контролер вывода данных отработаного парсера"""
    output = cli_args.output
    # match output:
    #     case 'pretty':
    #         pretty_output(results)
    #     case 'file':
    #         file_output(results, cli_args)
    #     case _:
    #         default_output(results)
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    """Вывод по умолчанию ввиде строк в консоль"""
    for row in results:
        print(*row)


def file_output(results, cli_args):
    """Вывод ввиде файла таблици"""
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')


def pretty_output(results):
    """Вывод ввиде отформатированных строк в консоль"""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)
