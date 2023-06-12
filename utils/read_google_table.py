import os
import re
import pandas as pd
from config import df_in_xlsx
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


def read_codes_on_google(CREDENTIALS_FILE='google_acc.json'):
    file_path = 'Артикула с гугл таблицы.xlsx'
    old_file_path = 'Старые артикула с гугл таблицы.xlsx'
    if os.path.exists(file_path):
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
        os.rename(file_path, old_file_path)
    # Файл, полученный в Google Developer Console
    # ID Google Sheets документа (можно взять из его URL)
    # spreadsheet_id = '1CGN9T4E5RjK1MCEDCVpYz-sRp8udtA9RZ13Uc52xVsk'
    spreadsheet_id = '1IaXufU8CYTQsMDxEvynBzlRAFm_G43Kll0PO3lvQDxA'

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Пример чтения файла
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:L30000',

    ).execute()

    data = values['values']
    headers = data[0]  # Заголовки столбцов из первого элемента списка значений
    rows = data[1:]
    # Проверка количества столбцов и создание DataFrame
    if len(headers) != len(rows[0]):
        print("Ошибка: количество столбцов не совпадает с количеством значений.")
    else:
        df = pd.DataFrame(rows, columns=headers)
        print(df)
        df_in_xlsx(df, 'Таблица гугл')

    list_art = []
    df = pd.read_excel('Таблица гугл.xlsx', usecols=['Наименование', 'Артикул на ВБ'],
                       dtype=str)
    df = df[~df['Артикул на ВБ'].isna() &
            df['Наименование'].apply(lambda x: isinstance(x, str) and not x.startswith('https'))
            ]
    df['Артикул на ВБ'] = df['Артикул на ВБ'].apply(lambda x: re.sub(r'\s+', ',', x))
    df['Артикул на ВБ'] = df['Артикул на ВБ'].apply(lambda x: x.lower().replace(',,', ','))
    df['Артикул на ВБ'].apply(lambda x: list_art.extend(x.split(',')))
    list_art = [i for i in list_art if len(i) > 0 and '-' in i]
    df = pd.DataFrame({'Артикул': list_art})
    df_in_xlsx(df, 'Артикула с гугл таблицы')

    df1 = pd.read_excel('Старые артикула с гугл таблицы.xlsx')
    df1 = df1.reindex(columns=df.columns)
    df1 = df1.reindex(index=df.index)
    diff = df.compare(df1)
    print(diff)
    merged = df1.merge(df, indicator=True, how='outer')
    diff = merged[merged['_merge'] != 'both']
    diff.to_excel("отличия.xlsx", index=True)
    diff = diff[~diff['Артикул'].isna()]
    list_new_arts = diff['Артикул'].unique().tolist()
    print(list_new_arts)

    return list_art


if __name__ == '__main__':
    read_codes_on_google()
