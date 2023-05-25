import json

import requests
from config import token


def bytes_to_megabytes(size_in_bytes):
    size_in_mb = size_in_bytes / (1024 * 1024)
    return round(size_in_mb, 2)


def get_yandex_disk_files(folder_path, token):
    url = f"https://cloud-api.yandex.net/v1/disk/resources?path={folder_path}"
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
                    # if '-' in code and code.isupper():
                    file_tuple = (name, path, code, size_mb)
                    file_list.append(file_tuple)
                elif file["type"] == "dir":
                    subfolder_files = get_yandex_disk_files(file["path"], token)
                    file_list.extend(subfolder_files)
            print(file_list)
            return file_list
        except Exception as ex:
            print(ex)
            return []
    else:
        print("Ошибка при получении списка файлов.")
        return []


folder_path = "/Значки ANIKOYA  02 23/ОДИНОЧКИ/Мария"  # Путь к папке на Яндекс.Диске
# folder_path = "/Downloads"  # Путь к папке на Яндекс.Диске

file_list = get_yandex_disk_files(folder_path, token)
for file in file_list:
    print(f"Артикул: {file[2]} Имя: {file[0]}, Путь: {file[1]}, Размер: {file[3]} МБ")

# result = {}
#
# for item in file_list:
#     name, path, code, size_mb = item
#     if code in result:
#         result[code].append([name, path, size_mb])
#     else:
#         result[code] = [[name, path, size_mb]]

# with open('json.json', "w") as f:
#     json.dump(result, f, ensure_ascii=False, indent=4)
# print(result)
