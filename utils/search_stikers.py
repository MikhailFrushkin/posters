import io
import os
import re

from PyQt5.QtWidgets import QMessageBox
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from loguru import logger

from config import main_path, stiker_path, SearchProgress, google_sticker_path

credentials = service_account.Credentials.from_service_account_file('google_acc.json')
service = build('drive', 'v3', credentials=credentials,  static_discovery=False)
folder_url = f"https://drive.google.com/drive/folders/{google_sticker_path}"
local_directory = f"{stiker_path}"


def search_files_by_folder_url(folder_url: str) -> list:
    """Поиск конкретного файла в папке на гугл диске"""
    # Извлекаем идентификатор папки из URL
    folder_id = re.search(r'/folders/([^/]+)', folder_url).group(1)

    # Формируем запрос для поиска файлов в указанной папке
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    return items


def search_files(query: str) -> list:
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    return items


def download_file(file_id: str, file_name: str) -> None:
    """Загрузка файла с гугл диска"""
    try:
        if not os.path.exists(f"{stiker_path}/{file_name}"):
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            with open(f"{stiker_path}/{file_name}", 'wb') as f:
                f.write(fh.getvalue())
                logger.success("Файл сохранен: {}".format(file_name))
        else:
            logger.success("Файл существует: {}".format(file_name))

    except:
        request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
        fh = io.FileIO(f"{stiker_path}/{file_name}", 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        logger.success("Файл сохранен: {}".format(file_name))


def download_files_from_folder(folder_url: str, destination_folder: str = f"{stiker_path}") -> None:
    """Загрузка всех файлов по урлу"""
    folder_id = re.search(r'/folders/([^/]+)', folder_url).group(1)

    query = f"'{folder_id}' in parents"
    page_token = None
    while True:
        results = service.files().list(q=query, fields="nextPageToken, files(id, name)", pageSize=1000,
                                       pageToken=page_token).execute()
        items = results.get('files', [])
        page_token = results.get('nextPageToken')
        if items:
            for item in items:
                file_id = item['id']
                file_name = item['name'].replace('\n', '')
                destination_path = os.path.join(destination_folder, file_name)

                if not os.path.exists(destination_path):
                    try:
                        download_file(file_id, file_name)
                    except Exception as ex:
                        logger.error(f"Ошибка загрузки файла: {file_name} {ex}")
                else:
                    logger.info(f"Файл уже существует: {file_name}")
        else:
            break

        if page_token is None:
            break


def get_all_files_in_folder(folder_url: str) -> list:
    """Получение списка файлов по урлу на гугл диске"""
    folder_id = re.search(r'/folders/([^/]+)', folder_url).group(1)
    files = []

    query = f"'{folder_id}' in parents"
    page_token = None
    while True:
        results = service.files().list(q=query, fields="nextPageToken, files(id, name)", pageSize=1000,
                                       pageToken=page_token).execute()
        items = results.get('files', [])
        page_token = results.get('nextPageToken')
        if items:
            files.extend(items)
        if page_token is None:
            break
    return files


def compare_files_with_local_directory(folder_url: str, local_directory: str) -> list:
    """Сравнивание файлов на гугл диске и компе"""
    folder_id = re.search(r'/folders/([^/]+)', folder_url).group(1)

    # Получение списка файлов на Google Диске
    query = f"'{folder_id}' in parents"
    page_token = None
    drive_files = []
    while True:
        results = service.files().list(q=query, fields="nextPageToken, files(id, name)", pageSize=1000,
                                       pageToken=page_token).execute()
        items = results.get('files', [])
        page_token = results.get('nextPageToken')

        if items:
            drive_files.extend(items)

        if page_token is None:
            break

    # Получение списка файлов в локальной директории
    local_files = []
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            local_files.append(file)

    # Сравнение списков файлов
    missing_files = []
    for drive_file in drive_files:
        if not drive_file['name'].endswith('.pdf'):
            logger.error(drive_file['name'])
        drive_file_name = drive_file['name']
        if drive_file_name not in local_files:
            missing_files.append(drive_file_name)

    return missing_files


def dowload_srikers(self=None):
    missing_files = compare_files_with_local_directory(folder_url, local_directory)
    logger.success(f'Количество новых стикеров на я.диске: {len(missing_files)}')
    logger.success(f'Список новых стикеров: {missing_files}')
    progress = SearchProgress(len(missing_files), self)
    if len(missing_files) != 0:
        if self:
            QMessageBox.information(self, 'Инфо', f'Список новых стикеров: {missing_files}')

        # Поиск файла и загрузка
        for item in missing_files:
            query = f"name='{item}'"

            files = search_files(query)
            if files:
                file_id = files[0]['id']
                file_name = files[0]['name']
                try:
                    download_file(file_id, file_name)
                    progress.update_progress()
                except Exception as ex:
                    logger.error(f'Ошибка скачивания стикера {query} {ex}')
            else:
                print("Файл не найден.")

        progress = SearchProgress(1, self)
        progress.update_progress()
        QMessageBox.information(self, 'Инфо', 'Загрузка завершена')
    else:
        if self:
            QMessageBox.information(self, 'Инфо', f'Новых стикеров не найдено')


if __name__ == '__main__':
    dowload_srikers()
