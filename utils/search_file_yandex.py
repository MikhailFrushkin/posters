import asyncio
from urllib.parse import quote

import aiohttp
import pandas as pd
from loguru import logger

from config import token, df_in_xlsx


async def get_folders(directory_path, folder_name, token):
    url = f"https://cloud-api.yandex.net/v1/disk/resources?path={quote(directory_path)}&limit=1000"
    headers = {"Authorization": f"OAuth {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            print(response.status)
            if response.status == 200:
                data = await response.json()
                for item in data["_embedded"]['items']:
                    if item['type'] == 'dir':
                        if item['name'].lower() == folder_name.lower():
                            return item['path']
                        else:
                            subfolder_path = await get_folders(item['path'], folder_name, token)
                            if subfolder_path:
                                return subfolder_path
            else:
                print(directory_path)
    return None


def search(folder_path, folder_name):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_folders(folder_path, folder_name, token))

    if result:
        print(f"Найдена папка: {result}")
    else:
        print("Целевая папка не найдена.")


async def traverse_yandex_disk(folder_path, target_folders, result_dict):
    url = f"https://cloud-api.yandex.net/v1/disk/resources?path={quote(folder_path)}&limit=1000"
    headers = {"Authorization": f"OAuth {token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            try:
                for item in data["_embedded"]['items']:
                    if item["type"] == "dir" and item["name"].lower() in target_folders:
                        result_dict[item["name"]] = item["path"]
                        logger.error(f'Найден артикул {item["name"]} {item["path"]}')
                    elif item["type"] == "dir":
                        await traverse_yandex_disk(item["path"], target_folders, result_dict)
                        logger.info(f'Проверена папка(файл){item["name"]} {item["path"]}')
            except Exception as ex:
                logger.debug(f'Ошибка при поиске папки {item["name"]} {ex}')


async def main():
    df = pd.read_excel('гуглтаблица.xlsx', usecols=['шепс', 'Наименование', 'Артикул на ВБ', 'POSTER-LIGAFOOTB'],
                       dtype=str)
    list_arts = []
    df = df[~df['Артикул на ВБ'].isna()]
    df['Артикул на ВБ'] = df['Артикул на ВБ'].apply(lambda x: x.lower().replace(' ', ',').replace(',,', ','))
    for row in df['Артикул на ВБ']:
        artikuls = str(row).split(',')
        list_arts.extend(artikuls)
    target_folders = [artikul.strip() for artikul in list_arts if len(artikul.strip()) != 0]
    starting_folder = "/Значки ANIKOYA  02 23/03 - POSUTA (плакаты)/"
    result_dict = {}

    await traverse_yandex_disk(starting_folder, target_folders, result_dict)

    df = pd.DataFrame(list(result_dict.items()), columns=['Артикул', 'Путь'])
    df_in_xlsx(df, 'Пути к артикулам')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
