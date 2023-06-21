import asyncio
from urllib.parse import quote

import aiohttp
import pandas as pd
from loguru import logger

from config import token, df_in_xlsx, SearchProgress
from utils.read_google_table import read_codes_on_google



async def get_folders(session, directory_path, folder_name, token):
    url = f"https://cloud-api.yandex.net/v1/disk/resources?path={quote(directory_path)}&limit=1000"
    headers = {"Authorization": f"OAuth {token}"}
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            for item in data["_embedded"]['items']:
                if item['type'] == 'dir':
                    if item['name'].lower() == folder_name.lower():
                        return item['path']
                    else:
                        subfolder_path = await get_folders(session, item['path'], folder_name, token)
                        if subfolder_path:
                            return subfolder_path
        else:
            print(directory_path)
    return None


async def search(folder_path, folder_name):
    async with aiohttp.ClientSession() as session:
        result = await get_folders(session, folder_path, folder_name, token)

    if result:
        print(f"Найдена папка: {result}")
    else:
        print("Целевая папка не найдена.")


async def traverse_yandex_disk(session, folder_path, target_folders, result_dict, self, progress):
    url = f"https://cloud-api.yandex.net/v1/disk/resources?path={quote(folder_path)}&limit=1000"
    headers = {"Authorization": f"OAuth {token}"}
    async with session.get(url, headers=headers) as response:
        data = await response.json()
        try:
            for item in data["_embedded"]['items']:
                if item["type"] == "dir" and item["name"].lower() in target_folders:
                    result_dict[item["name"].lower()] = item["path"]
                    logger.success(f'Найден артикул {item["name"]} {item["path"]} current_folder: {progress}')
                    progress.update_progress()
                elif item["type"] == "dir":
                    await traverse_yandex_disk(session, item["path"], target_folders, result_dict, self, progress)
                    logger.info(f'Проверена папка(файл){item["name"]} {item["path"]}')

        except Exception as ex:
            logger.debug(f'Ошибка при поиске папки {item["name"]} {ex}')


async def main_search(self=None):
    list_arts = read_codes_on_google()
    if list_arts:
        starting_folder = "/Значки ANIKOYA  02 23/03 - POSUTA (плакаты)/Михаил/"
        result_dict = {}
        progress = SearchProgress(len(list_arts), self)
        async with aiohttp.ClientSession() as session:
            await traverse_yandex_disk(session, starting_folder, list_arts, result_dict, self, progress)

        df = pd.DataFrame(list(result_dict.items()), columns=['Артикул', 'Путь'])
        df_in_xlsx(df, 'Пути к артикулам')
        return True

if __name__ == '__main__':
    asyncio.run(main_search())
