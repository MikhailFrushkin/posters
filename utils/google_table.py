import re

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


def df_in_xlsx(df, filename, max_width=50):
    # Создание нового рабочего книги Excel
    workbook = Workbook()
    # Создание нового листа в рабочей книге
    sheet = workbook.active
    # Конвертация DataFrame в строки данных
    for row in dataframe_to_rows(df, index=False, header=True):
        sheet.append(row)
        # Ограничение ширины колонок
    for column in sheet.columns:
        column_letter = column[0].column_letter
        max_length = max(len(str(cell.value)) for cell in column)
        adjusted_width = min(max_length + 2, max_width)
        sheet.column_dimensions[column_letter].width = adjusted_width
    # Сохранение рабочей книги в файл
    workbook.save(f"{filename}.xlsx")


def remove_urls(text):
    pattern = re.compile(r'https?://\S+|www\.\S+')
    return re.sub(pattern, '', text)


def main():
    df = pd.read_excel('гуглтаблица.xlsx', usecols=['шепс', 'Наименование', 'Артикул на ВБ', 'POSTER-LIGAFOOTB'],
                       dtype=str)
    df = df[~df['Артикул на ВБ'].isna() &
            df['Наименование'].apply(lambda x: isinstance(x, str) and not x.startswith('https'))
            ]
    df['Артикул на ВБ'] = df['Артикул на ВБ'].apply(lambda x: x.lower().replace(' ', ',').replace(',,', ','))
    df['Наименование'] = df['Наименование'].apply(lambda x: x.lower().replace('постеры', '').replace('постер', ''))
    df['Наименование'] = df['Наименование'].str.strip()
    df['Наименование'] = df['Наименование'].apply(lambda x: remove_urls(x) if isinstance(x, str) else x)
    df = df[df['Артикул на ВБ'].apply(lambda x: len(x.split(',')) == 1)]
    print(df.columns)
    df_in_xlsx(df, 'Артикула')


if __name__ == '__main__':
    main()
