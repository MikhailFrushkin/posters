import datetime
import os
from urllib.parse import quote

import pandas as pd
import requests
from loguru import logger

from config import token, df_in_xlsx, main_path, ready_path
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


def dowloads_files(self, df_new, new_arts):
    current_folder = 0
    df = pd.read_excel(df_new)
    df['Путь'] = df['Путь'].apply(lambda x: x[5:])
    combined_list = df[['Путь', 'Артикул']].values.tolist()
    logger.info(f'{combined_list}')
    total_folders = len(new_arts) * 3
    for number, i in enumerate(combined_list, start=1):
        file_path = f'{main_path}\\{i[1]}'
        count = 3
        if not os.path.exists(file_path):
            if i[1].endswith('6'):
                count = 6
            logger.info(f'Прогресс: {number} из {len(combined_list)}')
            os.makedirs(file_path)
            logger.info(f'Папка {file_path} успешно создана.')
            file_list = get_yandex_disk_files(i[0], token)
            sorted_elements = sorted(file_list, key=lambda x: x[3], reverse=True)

            for num, item in enumerate(sorted_elements[:count], start=1):
                logger.info(f"{num} Скачавание {item[1]}")
                try:
                    download_image(folder_path=f'{item[1][5:]}',
                                   file_path=file_path,
                                   filename=f'{num}.png')
                    current_folder += 1
                    self.update_progress(current_folder, total_folders)

                except Exception as ex:
                    logger.error(f"Ошибка загрузки файла {item[1]} {ex}")
        else:
            logger.info(f'Папка {file_path} уже существует.')


def unions_arts(self, new_arts):
    bad_list = []
    directory = main_path
    total_folders = len(new_arts)
    current_folder = 0

    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            try:
                full_path = os.path.join(directory, folder)
                if not os.path.exists(f'{ready_path}\\{folder}.pdf'):
                    time_start = datetime.datetime.now()
                    one_pdf(folder_path=full_path, filename=folder)
                    logger.info(f'{folder}|Время выполнения: {datetime.datetime.now() - time_start}')
                    pass
                else:
                    logger.info(f'{folder} существует')

                current_folder += 1
                self.update_progress(current_folder, total_folders)
            except Exception as ex:
                logger.error(f'{folder} ошибка соединения файлов {ex}')
                with open('Не объединенные артикула.txt', 'a') as f:
                    f.write(f'{folder}\n')
                bad_list.append(folder)

    bad_df = pd.DataFrame({'Артикул': bad_list})
    df_in_xlsx(bad_df, 'Не объединенные артикула')


def new_arts(new_file):
    new_df = pd.read_excel(new_file)
    new_arts = new_df['Артикул'].str.lower().unique().tolist()

    directory = main_path
    excluded_folder = "Готовые постеры по 3 шт"  # Исключаемая папка

    folders = [folder.lower() for folder in os.listdir(directory) if
               os.path.isdir(os.path.join(directory, folder)) and folder != excluded_folder]

    missing_elements = list(set(new_arts) - set(folders))

    logger.info(missing_elements)
    return missing_elements


if __name__ == '__main__':
    # Проверка что в папке папки с 3мя файлами
    # find_folders_with_incorrect_file_count(main_path')
    new_arts('Пути к артикулам.xlsx')

    # dowloads_files('Пути к артикулам.xlsx')
    # unions_arts()
