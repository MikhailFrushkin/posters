import pandas as pd


def read_excel_file(file):
    df = pd.read_excel(file)
    counts = df['Артикул продавца'].value_counts().to_dict()
    return counts


if __name__ == '__main__':
    read_excel_file('../Заказы.xlsx')
