from config import token
from urllib.parse import quote
import asyncio
import aiohttp


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


if __name__ == '__main__':
    folder_path = "/Значки ANIKOYA  02 23/03 - POSUTA (плакаты)/"
    folder_name = "егор крид"  # Искомое название папки
    # search(folder_path, folder_name)
