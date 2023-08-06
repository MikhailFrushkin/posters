import os
import re
from pprint import pprint

import pandas as pd
from loguru import logger

from config import df_in_xlsx, path_root, id_google_table
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


def read_codes_on_google(CREDENTIALS_FILE=f'{path_root}/google_acc.json'):
    logger.debug('Читаю гугл таблицу')
    file_path = 'files/Артикула с гугл таблицы.xlsx'
    old_file_path = 'files/Старые артикула с гугл таблицы.xlsx'
    if os.path.exists(file_path):
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
        os.rename(file_path, old_file_path)
    spreadsheet_id = f'{id_google_table}'
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http=httpAuth, static_discovery=False)
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A1:O30000',

        ).execute()
    except Exception as ex:
        logger.error(f'Ошибка чтения гуглтаблицы {ex}')
    data = values.get('values', [])
    headers = data[0]
    for row in data:
        missing_columns = len(headers) - len(row)
        if missing_columns > 0:
            row += [''] * missing_columns

    headers = data[0]  # Заголовки столбцов из первого элемента списка значений
    rows = data[1:]
    # Проверка количества столбцов и создание DataFrame
    lines_list = []
    if len(headers) != len(rows[0]):
        print("Ошибка: количество столбцов не совпадает с количеством значений.")
    else:
        df = pd.DataFrame(rows, columns=headers)
        df_in_xlsx(df, 'Таблица гугл')

    list_art = []
    df = pd.read_excel('files/Таблица гугл.xlsx', usecols=['Наименование', 'Артикул на ВБ'],
                       dtype=str)
    df = df[~df['Артикул на ВБ'].isna() &
            df['Наименование'].apply(lambda x: isinstance(x, str) and not x.startswith('https'))
            ]
    df['Артикул на ВБ'] = df['Артикул на ВБ'].apply(lambda x: re.sub(r'\s+', ' ', x))
    df['Артикул на ВБ'] = df['Артикул на ВБ'].apply(lambda x: x.replace(',', ' '))
    df['Артикул на ВБ'] = df['Артикул на ВБ'].apply(lambda x: list_art.extend(x.split()))
    list_art = [i for i in list_art if len(i) > 0 and '-' in i]
    print(len(list_art))

    return list_art


if __name__ == '__main__':
    read_codes_on_google()
