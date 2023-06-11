import pandas as pd

from config import df_in_xlsx


def find_missing_elements(list1, list2):
    missing_elements = []
    for element in list1:
        if element.lower() not in list2:
            missing_elements.append(element)
    return missing_elements


def main():
    df_all = pd.read_excel('список артикулов.xlsx')
    all_list = df_all['Артикул'].str.lower().unique().tolist()
    print('Количество артикулов: {}'.format(len(all_list)))

    df_goods = pd.read_excel('../files/обновленный_файл.xlsx')
    goods_list = df_goods['Артикул'].str.lower().unique().tolist()
    print('Количество найденых артикулов на яндекс диске: {}'.format(len(goods_list)))

    missing_elements = find_missing_elements(all_list, goods_list)

    print(len(missing_elements))
    df_bad = pd.DataFrame({'Артикул': missing_elements})
    df_in_xlsx(df_bad, 'Не найденные артикула')


if __name__ == '__main__':
    main()