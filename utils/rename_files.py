from PyQt5.QtWidgets import QMessageBox
from loguru import logger
import os

count_glob = 0


def rename_files(file_data):
    folder_path, file_list = file_data

    for index, filename in enumerate(file_list, start=1):
        file_extension = os.path.splitext(filename)[1]
        new_filename = f"{index}{file_extension}"
        old_filepath = os.path.join(folder_path, filename)
        new_filepath = os.path.join(folder_path, new_filename)
        os.rename(old_filepath, new_filepath)

    print(f"{file_data}\nФайлы переименованы успешно.")


def count_files_posters(folder: str, count_all_files, self) -> tuple:
    global count_glob
    exclude_keywords = ['размер', 'титул', 'мокап', 'moc', 'mos', 'рекомен', 'реки', 'подлож', 'шаблон']
    count = 0
    good_count = [3, 6, 10]
    good_list_files = []
    for filename in os.listdir(folder):
        file_extension = os.path.splitext(filename)[1]
        if file_extension.lower() in ['.png', '.jpg'] and not any(
                keyword in filename.lower() for keyword in exclude_keywords):
            count += 1
            good_list_files.append(filename)

    count_glob += 1
    if count not in good_count:
        logger.error(f"{count_glob}{folder} Количество файлов без указанных ключевых слов: {count}")
    if count_all_files and count_all_files != count:
        logger.error(f"{folder} не соответствует количество файлов {count}/{count_all_files}")
        if self:
            QMessageBox.warning(self, 'Ошибка',
                                    f"{folder} не соответствует количество файлов {count}/{count_all_files}")
    return tuple((folder, good_list_files), )


def count_objects_in_folders(directory, self=None):
    folder_info = []

    for root, dirs, files in os.walk(directory):
        num_objects = len(dirs) + len(files)
        folder_info.append((root, num_objects, root.split('\\')[-1]))

    sorted_folder_info = sorted(folder_info, key=lambda x: x[1], reverse=True)

    for folder, num_objects, papka in sorted_folder_info:
        count = None
        papka = papka.split('-')[-2:]
        for element in papka:
            value = element[-2:]
            if value.endswith('3'):
                count = 3
            elif value.endswith('6'):
                count = 6
            elif value.endswith('10'):
                count = 10
        logger.error(f"Папка: {folder}, Количество объектов: {num_objects} Из {count} постеров")
        try:
            rename_files(count_files_posters(folder, count, self))
        except Exception as ex:
            logger.error(ex)


if __name__ == '__main__':
    directory = r'E:\Новая база\Готовые\poster-kaws-gloss-3'
    # Замените "путь/к/папке" на нужный путь к директории
    count_objects_in_folders(directory)
    # count_files_posters(r'E:\Новая база\Готовые\poster-italy-gloss')
    # rename_files(('E:\\Новая база\\Готовые\\poster-winx-gloss', ['1. Феи винкс.png', '2. Феи винкс.png', '3. Феи винкс.png']))
