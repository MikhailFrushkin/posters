from config import token
import requests


def download_image(folder_path, file_path):
    url = f"https://cloud-api.yandex.net/v1/disk/resources/download?path={folder_path}"
    headers = {
        "Authorization": f"OAuth {token}"
    }
    response = requests.get(url, headers=headers)
    download_url = response.json()["href"]
    image_response = requests.get(download_url)
    with open(file_path, "wb") as file:
        file.write(image_response.content)


folder_path = "/Downloads/POSTER-KOSMOS-GLOSS/1 Космос.jpg"  # Замените на фактический URL изображения на Яндекс.Диске
save_path = "temp/image.png"  # Путь, по которому нужно сохранить изображение

download_image(folder_path, save_path)
