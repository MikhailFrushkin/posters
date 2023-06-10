import datetime
import os
from urllib.parse import quote

import pandas as pd
import requests
from loguru import logger

from config import token
from utils.google_table import df_in_xlsx
from utils.one_file import one_pdf


def bytes_to_megabytes(size_in_bytes):
    size_in_mb = size_in_bytes / (1024 * 1024)
    return round(size_in_mb, 2)


def get_yandex_disk_files(folder_path, token):
    url = f"https://cloud-api.yandex.net/v1/disk/resources?path={quote(folder_path)}"
    headers = {
        "Authorization": f"OAuth {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            files = response.json()["_embedded"]["items"]
            file_list = []
            for file in files:
                if file["type"] == "file" and file["name"].lower().endswith((".png", ".jpg")):
                    name = file["name"]
                    path = file["path"]
                    size = file["size"]
                    size_mb = bytes_to_megabytes(size)
                    code = path.split('/')[-2] if '/' in path else ''  # Извлечение имени папки из пути
                    file_tuple = (name, path, code, size_mb)
                    file_list.append(file_tuple)
                elif file["type"] == "dir":
                    subfolder_files = get_yandex_disk_files(file["path"], token)
                    file_list.extend(subfolder_files)
            return file_list
        except Exception as ex:
            print(ex)
            return []
    else:
        logger.error("Ошибка при получении списка файлов.")
        return []


def download_image(folder_path, file_path, filename):
    url = f"https://cloud-api.yandex.net/v1/disk/resources/download?path={quote(folder_path)}"
    headers = {
        "Authorization": f"OAuth {token}"
    }
    response = requests.get(url, headers=headers)
    download_url = response.json()["href"]
    image_response = requests.get(download_url)
    with open(os.path.join(file_path, filename), "wb") as file:
        file.write(image_response.content)


def count_files(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count


def find_folders_with_incorrect_file_count(directory):
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            file_count = count_files(folder_path)
            if file_count != 3:
                print(folder_path)



if __name__ == '__main__':
    # folder_path = "/Значки ANIKOYA  02 23/03 - POSUTA (плакаты)/Валерия/14+ продолжение/POSTER-14+PRODOLZHENIE-GLOSS-3"  # Путь к папке на Яндекс.Диске

    # df = pd.read_excel('../files/обновленный_файл.xlsx')
    # df['Путь'] = df['Путь'].apply(lambda x: x[5:])
    # combined_list = df[['Путь', 'Артикул']].values.tolist()
    # for number, i in enumerate(combined_list, start=1):
    #     file_path = f'E:\\Ярослав\\Готовые постеры по 3 шт\\{i[1]}'
    #     count = 3
    #     if not os.path.exists(file_path):
    #         if i[1].endswith('6'):
    #             count = 6
    #         logger.info(f'Прогресс: {number} из {len(combined_list)}')
    #         os.makedirs(file_path)
    #         logger.info(f'Папка {file_path} успешно создана.')
    #         file_list = get_yandex_disk_files(i[0], token)
    #         sorted_elements = sorted(file_list, key=lambda x: x[3], reverse=True)
    #
    #         for num, item in enumerate(sorted_elements[:count], start=1):
    #             logger.info(f"{num} Скачавание {item[1]}")
    #             try:
    #                 download_image(folder_path=f'{item[1][5:]}',
    #                                file_path=file_path,
    #                                filename=f'{num}.png')
    #             except Exception as ex:
    #                 logger.error(f"Ошибка загрузки файла {item[1]} {ex}")
    #     else:
    #         logger.info(f'Папка {file_path} уже существует.')
    #Проверка что в папке папки с 3мя файлами
    # find_folders_with_incorrect_file_count('E:\\Ярослав\\Готовые постеры по 3 шт')
    bad_list = []
    directory = 'E:\\Ярослав\\Готовые постеры по 3 шт'
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            try:
                full_path = os.path.join(directory, folder)
                if not os.path.exists(f'E:\\Ярослав\\Готовые постеры по 3 шт\\Готовые постеры по 3 шт\\{folder}.pdf'):
                    # print(f'E:\\Ярослав\\Готовые постеры по 3 шт\\Готовые постеры по 3 шт\\{folder}.pdf')
                    time_start = datetime.datetime.now()
                    one_pdf(folder_path=full_path, filename=folder)
                    logger.info(f'{folder}|Время выполнения: {datetime.datetime.now() - time_start}')
                    pass
                else:
                    logger.info(f'{folder} существует')
            except Exception as ex:
                logger.error(f'{folder} ошибка соединения файлов {ex}')
                with open('Не объединенные артикула.txt', 'a') as f:
                    f.write(f'{folder}\n')
                bad_list.append(folder)

    bad_df = pd.DataFrame({'Артикул': bad_list})
    df_in_xlsx(bad_df, 'Не объединенные артикула')
