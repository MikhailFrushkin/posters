import asyncio
import itertools
import os
import subprocess
import sys

from PyPDF2 import PdfReader
from PyQt5.QtWidgets import QMessageBox
from loguru import logger

from config import FilesOnPrint, stiker_path, ready_path, acrobat_path
from utils.search_file import search_file


async def print_pdf(file_path, num_copies, printer_name):
    # Проверка, поддерживается ли печать через subprocess на вашей платформе
    if sys.platform != 'win32':
        print("Печать PDF поддерживается только в Windows.")
        return

    # Проверка наличия файла Adobe Acrobat Reader
    if not os.path.isfile(acrobat_path):
        print("Adobe Acrobat Reader не найден.")
        return

    try:
        # Открытие PDF-файла с использованием PyPDF2
        with open(file_path, "rb") as f:
            pdf = PdfReader(f)

            # Формирование команды для печати файла
            print_command = f'"{acrobat_path}" /N /T "{file_path}" "{printer_name}"'

            # Печать указанного числа копий
            for _ in range(num_copies):
                # Запуск процесса печати
                subprocess.run(print_command, shell=True)

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


async def queue_sticker(printer_list, file_list, self=None):
    count = 0

    for file, printer in zip(file_list, itertools.cycle(printer_list)):
        file_path, num_copies = file
        await print_pdf(file_path, num_copies, printer)

        count += 1

        if self:
            self.progress_bar.setValue(count + 1)
            filename = file_path.split('\\')[-1]
            self.progress_label.setText(f"Печать: {filename}\nНа принтер: {printer}")

if __name__ == '__main__':
    printer_list = ['Fax', 'Отправить в OneNote 16']
    order = [
        FilesOnPrint(art='POSTER-BLACKPINK-GLOSS', count=1, name='Постеры OG Buda картина А3 набор', status='✅'),
        FilesOnPrint(art='POSTER-BLACKPINK-MAT', count=2, name='Постер asdasdasd', status='✅')
    ]
    file_tuple = create_file_list(order)

    asyncio.run(queue_sticker(printer_list, file_tuple))
