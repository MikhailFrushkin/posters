import json
import os
import urllib.parse

from config import token
import requests

from utils.search_files_on_ydisk import bytes_to_megabytes


def rename_file(file_path, new_name):
    print((file_path[5:], new_name))
    headers = {
        'Authorization': f'OAuth {token}',
    }
    params = {
        'path': file_path,
        'overwrite': 'true',
        'fields': 'name',
        'name': new_name
    }

    url = 'https://cloud-api.yandex.net/v1/disk/resources/move'
    response = requests.post(url, headers=headers, params=params)

    if response.status_code == 200:
        print(f'File "{file_path}" renamed to "{new_name}" successfully.')
    else:
        print(f'Failed to rename file. Error code: {response.status_code}')


def get_file_size(file_path):
    headers = {
        "Authorization": f"OAuth {token}"
    }
    url = f"https://cloud-api.yandex.net/v1/disk/resources"
    params = {
        "path": file_path
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["size"]
    else:
        return -1


def get_largest_files(folder_path, limit=3):
    headers = {
        "Authorization": f"OAuth {token}"
    }
    url = f"https://cloud-api.yandex.net/v1/disk/resources"
    params = {
        "path": folder_path,
        "limit": 1000,
        "fields": "items.name,items.path,items.type"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        items = data['_embedded']["items"]
        with open(f'{folder_path.split("/")[-1]}.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
        # Фильтрация файлов по расширению и ключевым словам в имени

        filtered_items = [item for item in items if item["type"] == "file"
                          and item["name"].lower().endswith((".png", ".jpg"))
                          and "мокап" not in item["name"].lower()
                          and "титульник" not in item["name"].lower()
                          and "размер" not in item["name"].lower()]

        # Сортировка файлов по размеру
        sorted_items = sorted(filtered_items, key=lambda x: get_file_size(x["path"]), reverse=True)
        return sorted_items[:limit]
    else:
        return []


def main():
    # Укажите список папок, в которых нужно найти файлы
    folder_list = [
        "/Значки ANIKOYA  02 23/03 - POSUTA (плакаты)/Валерия/14+ продолжение/POSTER-14+PRODOLZHENIE-MAT-3"]

    for folder_path in folder_list:
        largest_files = get_largest_files(folder_path, limit=3)
        if largest_files:
            print(f"Три самых больших файла в папке {folder_path}:")
            for index, file in enumerate(largest_files, start=1):
                file_name, file_extension = os.path.splitext(file["name"])
                new_name = f"{index}{file_extension}"
                print(new_name)
                rename_file(file["path"], new_name)
            print()
        else:
            print(f"В папке {folder_path} не найдено файлов, удовлетворяющих условиям.")


if __name__ == '__main__':
    main()
