import asyncio
import datetime
import os
from urllib.parse import quote

import pandas as pd
import requests
from loguru import logger

from config import token, df_in_xlsx, main_path, ready_path, SearchProgress
from utils.one_file import one_pdf
from utils.rename_files import count_objects_in_folders
from utils.search_file_yandex import main_search


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


def dowloads_files(df_new, self=None):
    def download_files(source_folder, target_folder, token):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization': 'OAuth ' + token}
        params = {
            'path': target_folder[5:],
            'limit': 1000,  # Максимальное количество элементов в одном запросе
        }
        response = requests.get(url, headers=headers, params=params)
        logger.debug(f'Получен ответ: {response.status_code}')

        if response.status_code == 200:
            resource_data = response.json()
            for item in resource_data['_embedded']['items']:
                if item['type'] == 'file':
                    download_url = item['file']
                    download_response = requests.get(download_url)
                    if download_response.status_code == 200:
                        file_path = os.path.join(source_folder, item['name'])
                        with open(file_path, 'wb') as file:
                            file.write(download_response.content)
                            logger.success(f'Загружен файл {item["name"]}')
                elif item['type'] == 'dir':
                    logger.info(f"Переход в папку {item['path']}")
                    download_files(source_folder, target_folder + "/" + item['name'], token)

    folder_path = main_path
    df = pd.read_excel(df_new)
    if self:
        progress = SearchProgress(len(df), self)
    # Итерация по строкам и передача значений в функцию
    for index, row in df.iterrows():
        vpr = row['Артикул']
        target_folder = row['Путь']
        if not os.path.exists(os.path.join(folder_path, vpr)):
            os.makedirs(os.path.join(folder_path, vpr))
            logger.debug(f"Скачивание артикула {vpr}")
            try:
                download_files(os.path.join(folder_path, vpr), target_folder, token)
                if self:
                    progress.update_progress()
            except Exception as ex:
                logger.error(f'Ошибка загрузки {os.path.join(folder_path, vpr)}|{target_folder}|{ex}')
        else:
            logger.debug(f'Папка существует {os.path.join(folder_path, vpr)}')
        try:
            count_objects_in_folders(os.path.join(main_path, vpr))
        except Exception as ex:
            logger.error(f'Ошибка переименовывания папки {os.path.join(main_path, vpr)}')


def unions_arts(self, new_arts):
    print(new_arts)
    if self:
        progress = SearchProgress(len(new_arts), self)
    for art in new_arts:
        full_path = os.path.join(main_path, art)
        time_start = datetime.datetime.now()
        try:
            logger.info(f'{art} ... соединение!')
            one_pdf(folder_path=full_path, filename=art)
            logger.info(f'{art}|Время выполнения: {datetime.datetime.now() - time_start}')
            if self:
                progress.update_progress()
        except Exception as ex:
            logger.error(f'{art} ошибка соединения файлов {ex}')
            with open('Не объединенные артикула.txt', 'a') as f:
                f.write(f'{art}\n')



def missing_arts(new_file):
    new_df = pd.read_excel(new_file)
    new_arts = new_df['Артикул'].str.lower().unique().tolist()

    directory = main_path
    excluded_folder = "Готовые постеры по 3 шт"  # Исключаемая папка

    folders = [folder.lower() for folder in os.listdir(directory) if
               os.path.isdir(os.path.join(directory, folder)) and folder != excluded_folder]
    logger.debug(f'Количество артикулов в директории {main_path}: {len(folders)}')
    logger.debug(f'Количество артикулов в файле {new_file}: {len(new_arts)}')
    missing_elements = list(set(new_arts) - set(folders))
    logger.debug(f'разница артикулов: {missing_elements}')
    return new_arts


def new_arts(new_file, self=None):
    # получение и сохранение артикулов с гугл таблицы
    asyncio.run(main_search(self))
    missing_elements = []
    missing_arts(new_file)
    logger.info(missing_elements)
    return missing_elements


if __name__ == '__main__':
    # Проверка что в папке папки с 3мя файлами
    # find_folders_with_incorrect_file_count(main_path')
    new_arts('Пути к артикулам.xlsx')

    # dowloads_files('Пути к артикулам.xlsx')
    # unions_arts()
