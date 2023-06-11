import itertools

import win32api
import win32con
import win32print
from loguru import logger

from config import FilesOnPrint, ready_path
from utils.search_file import search_file


def queue(printer_list, file_list, type_files):
    dev_mode_parameters = {
        "PaperSize": win32con.DMPAPER_A3,
        "Orientation": win32con.DMORIENT_PORTRAIT,
        "PrintQuality": win32con.DMRES_HIGH,
    }
    if type_files == 'Матовые':
        printer_list = [i.split('(')[0].strip() for i in printer_list if 'мат' in i]
        print(printer_list)
        print(file_list)
        print(type_files)
    # Циклическое распределение файлов по принтерам
    printer_file_pairs = zip(printer_list, itertools.cycle(file_list))
    for printer, file in printer_file_pairs:
        print(printer, file)

        print_defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
        printer_handle = win32print.OpenPrinter(printer, print_defaults)
        logger.info(f"параметры принтера: {printer_handle}")
        # Получаем текущую конфигурацию принтера
        printer_info = win32print.GetPrinter(printer_handle, 2)
        dev_mode = printer_info["pDevMode"]
        try:
            # Применяем параметры конфигурации
            for key, value in dev_mode_parameters.items():
                setattr(dev_mode, key, value)
            # Устанавливаем количество копий
            dev_mode.Copies = file[1]
            # Устанавливаем обновленную конфигурацию принтера
            win32print.SetPrinter(printer_handle, 2, printer_info, 0)
            logger.info("Параметры печати успешно применены.")

            win32print.StartDocPrinter(printer_handle, 1, [file[0], None, "raw"])
            # 2 в начале для открытия pdf и его сворачивания, для открытия без сворачивания поменяйте на 1
            win32api.ShellExecute(2, 'print', file[0], '.', '/manualstoprint', 0)
            # "Закрываем" принтер
        except Exception as e:
            logger.error(f"Ошибка при применении параметров печати:{e}")
        finally:
            # Закрываем принтер
            win32print.ClosePrinter(printer_handle)


def create_file_list(orders):
    directory = ready_path
    file_tuple = tuple()
    for item in orders:
        path_file = search_file(f"{item.art}.pdf", directory)
        file_tuple += ((path_file, item.count),)
    return file_tuple


if __name__ == '__main__':
    # Нужна обработка ошибок при печати, проплевывает, остаавливается печать
    # отправляет на принтер по умолчанию
    printer_list = ['Fax', 'Отправить в OneNote 16 (матовый)']
    order = [FilesOnPrint(art='POSTER-ATOMICHEART-GLOSS', count=5, name='Атомик', status='✅'),
             FilesOnPrint(art='POSTER-BLACKPINK-GLOSS', count=1, name='Постеры OG Buda картина А3 набор', status='✅'),
             FilesOnPrint(art='POSTER-BLACKPINK-MAT', count=1, name='Постер asdasdasd', status='✅')]
    file_tuple = create_file_list(order)
    queue(printer_list, file_tuple, type_files='Матовые')
