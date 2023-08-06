import os
from typing import List

import pandas as pd
from config import FilesOnPrint


def read_excel_file(file: str) -> List[FilesOnPrint]:
    df = pd.read_excel(file)
    df = df.groupby('Артикул продавца').agg({
        'Название товара': 'first',
        'Стикер': 'count',
    }).reset_index()
    df = df.rename(columns={'Стикер': 'Количество'})

    files_on_print = []
    for index, row in df.iterrows():
        file_on_print = FilesOnPrint(art=row['Артикул продавца'], name=row['Название товара'], count=row['Количество'])
        files_on_print.append(file_on_print)

    return files_on_print



if __name__ == '__main__':
    print(read_excel_file('../Заказы.xlsx'))
