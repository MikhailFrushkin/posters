import asyncio
import os
from urllib.parse import quote

import aiohttp
import pandas as pd
from loguru import logger

from config import token, df_in_xlsx, SearchProgress, path_base_y_disc, main_path, ready_path
from utils.read_google_table import read_codes_on_google


# async def traverse_yandex_disk(session, folder_path, target_folders, result_dict, progress):
#     url = f"https://cloud-api.yandex.net/v1/disk/resources?path={quote(folder_path)}&limit=1000"
#     headers = {"Authorization": f"OAuth {token}"}
#     try:
#         async with session.get(url, headers=headers) as response:
#             data = await response.json()
#             for item in data["_embedded"]['items']:
#                 if item["type"] == "dir" and item["name"].lower() in target_folders:
#                     result_dict[item["name"].lower()] = item["path"]
#                     logger.success(f'Найден артикул {item["name"]} {item["path"]} current_folder: {progress}')
#                     progress.update_progress()
#                 elif item["type"] == "dir":
#                     await traverse_yandex_disk(session, item["path"], target_folders, result_dict, progress)
#                     logger.info(f'Проверена папка(файл) {item["name"]} {item["path"]}')
#     except Exception as ex:
#         logger.debug(f'Ошибка при поиске папки {folder_path} {ex}')
#
#
# async def main_search(self=None):
#     list_arts = list(map(lambda x: x.lower(), read_codes_on_google()))
#     print(list_arts)
#     logger.info(list_arts)
#
#     if list_arts:
#         starting_folder = path_base_y_disc
#         result_dict = {}
#         progress = SearchProgress(len(list_arts), self)
#         async with aiohttp.ClientSession() as session:
#             tasks = [traverse_yandex_disk(session, starting_folder, list_arts, result_dict, progress)]
#             await asyncio.gather(*tasks)
#
#         df = pd.DataFrame(list(result_dict.items()), columns=['Артикул', 'Путь'])
#         if self:
#             logger.info('Создан документ Пути к артикулам.xlsx')
#         df_in_xlsx(df, 'Пути к артикулам')
#         try:
#             df_all_arts = pd.read_excel('files/Артикула с гугл таблицы.xlsx')
#             df_result = df_all_arts.merge(df, on='Артикул', how='outer')
#             df_result = df_result[df_result['Путь'].isna()]
#             if self:
#                 logger.info('Создан документ Разница артикулов с гугл.таблицы и на я.диске.xlsx')
#             df_in_xlsx(df_result, 'Разница артикулов с гугл.таблицы и на я.диске')
#         except Exception as ex:
#             logger.error(f'Ошибка создания файла "Разница артикулов с гугл.таблицы и на я.диске" {ex}')
#         return True


async def traverse_yandex_disk(session, folder_path, target_folders, result_dict, progress=None):
    url = f"https://cloud-api.yandex.net/v1/disk/resources?path={quote(folder_path)}&limit=1000"
    headers = {"Authorization": f"OAuth {token}"}
    try:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            tasks = []
            for item in data["_embedded"]["items"]:
                if item["type"] == "dir":
                    result_dict[item["name"].lower()] = item["path"]
                    task = traverse_yandex_disk(session, item["path"], target_folders, result_dict, progress)
                    tasks.append(task)
            if tasks:
                await asyncio.gather(*tasks)
    except Exception as ex:
        logger.debug(f'Ошибка при поиске папки {folder_path} {ex}')


async def main_search(self=None):
    target_folders = list(map(lambda x: x.lower(), read_codes_on_google()))

    if target_folders:
        folder_path = path_base_y_disc
        result_dict = {}
        async with aiohttp.ClientSession() as session:
            await traverse_yandex_disk(session, folder_path, target_folders, result_dict)

        df = pd.DataFrame(list(result_dict.items()), columns=['Артикул', 'Путь'])
        logger.info('Создан документ Пути к артикулам.xlsx')
        df_in_xlsx(df, 'Пути к артикулам')


        def get_all_folder_names(directory):
            files_names = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    files_name = file
                    files_names.append(files_name.lower().replace('.pdf', ''))
            return files_names

        all_folder_names = get_all_folder_names(ready_path)
        df = df[df['Артикул'].isin(target_folders) & ~df['Артикул'].isin(all_folder_names)]
        df_in_xlsx(df, 'Разница артикулов с гугл.таблицы и на я.диске')
        return True


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_search())
