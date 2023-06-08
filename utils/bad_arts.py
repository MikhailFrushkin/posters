import pandas as pd


def main():
    df_all = pd.read_excel('список артикулов.xlsx')
    all_list = df_all['Артикул'].unique().tolist()
    print('Количество артикулов: {}'.format(len(all_list)))

    df_goods = pd.read_excel('../files/обновленный_файл.xlsx')
    goods_list = df_goods['Артикул'].unique().tolist()
    print('Количество найденых артикулов на яндекс диске: {}'.format(len(goods_list)))
    print(goods_list)

    goods_list = goods_list.extend(all_list)
    for item in goods_list:
        pass
    print(len(all_list))


if __name__ == '__main__':
    main()