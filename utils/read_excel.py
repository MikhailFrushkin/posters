import pandas as pd


def read_excel_file(file: str) -> dict:
    df = pd.read_excel(file)
    counts = df['Артикул продавца'].value_counts().to_dict()
    df = df.groupby('Артикул продавца').agg({
        'Название товара': 'first',
        'Стикер': 'count',
    }).reset_index()
    df = df.rename(columns={'Стикер': 'Количество'})
    df.sort_values('Количество', ascending=False).to_excel('files/Сгруппированный заказ.xlsx', index=False)
    print(counts)
    return counts


if __name__ == '__main__':
    read_excel_file('../Заказы.xlsx')
