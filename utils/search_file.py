import os


def search_file(filename, directory):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None


if __name__ == '__main__':
    # Пример использования
    filename = "POSTER-BLACKPINK-GLOSS.pdf"
    directory = r'C:\Users\A3_posters\Готовые постеры по 3 шт'
    result = search_file(filename, directory)
    if result:
        print("Файл найден:", result)
    else:
        print("Файл не найден.")
