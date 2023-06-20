import os

from config import main_path


def search_file(filename, directory):
    for root, dirs, files in os.walk(directory):
        if filename.lower() in list(map(str.lower, files)):
            return os.path.join(root, filename)
    return None


if __name__ == '__main__':
    # Пример использования
    filename = "POSTER-BLACKPINK-GLOSS.pdf"
    directory = main_path
    result = search_file(filename, directory)
    if result:
        print("Файл найден:", result)
    else:
        print("Файл не найден.")
