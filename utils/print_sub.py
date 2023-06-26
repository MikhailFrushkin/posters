import itertools
import os
import subprocess
import sys

from PyQt5.QtWidgets import QMessageBox
from loguru import logger

from config import FilesOnPrint, ready_path, acrobat_path
from utils.search_file import search_file


def print_pdf(file_path, num_copies, printer_name):
    # Проверка, поддерживается ли печать через subprocess на вашей платформе
    if sys.platform != 'win32':
        print("Печать PDF поддерживается только в Windows.")
    # Проверка наличия файла Adobe Acrobat Reader
    if not os.path.isfile(acrobat_path):
        print("Adobe Acrobat Reader не найден.")
        return
    try:
        print_processes = []
        # Открытие PDF-файла с использованием PyPDF2
        with open(file_path, "rb") as f:
            # Формирование команды для печати файла
            print_command = f'"{acrobat_path}" /N /T "{file_path}" "{printer_name}"'
            # print_command = (
            #     f'"{acrobat_path}" /N /T '
            #     f'/O "ориентация" '  # Замените "ориентация" на "Landscape" для горизонтальной ориентации или "Portrait" для вертикальной ориентации
            #     f'/P "без полей" '  # Замените "без полей" на "No" для печати с полями или "Yes" для печати без полей
            #     f'"{file_path}" "{printer_name}"'
            # )
            # Печать указанного числа копий
            for _ in range(num_copies):
                # Запуск процесса печати
                print_process = subprocess.Popen(print_command, shell=True)
                print_processes.append(print_process)
        logger.success(f'Файл {file_path} отправлен на печать ({num_copies} копий). на принтер {printer_name}')
    except Exception as e:
        logger.error(f'Возникла ошибка при печати файла: {e}')


def create_file_list(orders, directory=ready_path, self=None):
    bad_arts = []
    file_tuple = tuple()
    for item in orders:
        path_file = search_file(f"{item.art}.pdf", directory)
        if path_file:
            file_tuple += ((path_file, item.count),)
        else:
            bad_arts.append(item.art)
    if self and len(bad_arts) > 0:
        QMessageBox.warning(self, 'Не найдено', f'Файлы не найденны\n{bad_arts}')

    return file_tuple


def queue(printer_list, file_list, type_files, self=None):
    """Печать постеров"""
    if self:
        self.progress_label.setText("Прогресс: 0%")
        self.progress_bar.setValue(0)
        total = len(file_list)
        completed = 0
    if type_files == 'Матовые':
        printer_list = [i.split('(')[0].strip() for i in printer_list if 'мат' in i.lower()]
    else:
        printer_list = [i.split('(')[0].strip() for i in printer_list if 'мат' not in i.lower()]

    if len(printer_list) == 0:
        return False
    tuple_printing = tuple()
    for file, printer in zip(file_list, itertools.cycle(printer_list)):
        tuple_printing += ((file[0], file[1], printer),)
    for item in tuple_printing:
        file_path, num_copies, printer_name = item
        print_pdf(file_path, num_copies, printer_name)
        if self:
            completed += 1
            progress = int((completed / total) * 100)
            self.progress_label.setText(f"Прогресс: {progress}%")
            self.progress_bar.setValue(progress)


def queue_sticker(printer_list, file_list, self=None):
    tuple_printing = tuple()
    count = 0

    for file, printer in zip(file_list, itertools.cycle(printer_list)):
        tuple_printing += ((file[0], file[1], printer),)
    for item in tuple_printing:
        file_path, num_copies, printer_name = item
        print_pdf(file_path, num_copies, printer_name)
        count += 1
        if self:
            self.progress_bar.setValue(count + 1)
            filename = file_path.split('\\')[-1]
            self.progress_label.setText(f"Печать: {filename}\nНа принтер: {printer_name}")


if __name__ == '__main__':
    printer_list = ['Fax', 'Отправить в OneNote 16']
    order = [
        FilesOnPrint(art='POSTER-BLACKPINK-GLOSS', count=1, name='Постеры OG Buda картина А3 набор', status='✅'),
        FilesOnPrint(art='POSTER-BLACKPINK-MAT', count=2, name='Постер asdasdasd', status='✅')
    ]
    file_tuple = create_file_list(order)

    tuple_printing = queue_sticker(printer_list, file_tuple)
