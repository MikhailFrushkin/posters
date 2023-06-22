import itertools

import win32api
import win32con
import win32print
from PyQt5.QtWidgets import QMessageBox
from loguru import logger

from config import FilesOnPrint, ready_path, stiker_path
from utils.search_file import search_file


def is_printer_ready(handle):
    """
    PRINTER_STATUS_PAUSED: 1
    PRINTER_STATUS_ERROR: 2
    PRINTER_STATUS_PENDING_DELETION: 4
    PRINTER_STATUS_PAPER_JAM: 8
    PRINTER_STATUS_PAPER_OUT: 16
    PRINTER_STATUS_OUTPUT_BIN_FULL: 2048
    PRINTER_STATUS_NOT_AVAILABLE: 4096
    PRINTER_STATUS_NO_TONER: 262144
    PRINTER_STATUS_OFFLINE: 128
    PRINTER_STATUS_PRINTING: 1024
    PRINTER_STATUS_OUTPUT_BIN_FULL: 2048
    PRINTER_STATUS_USER_INTERVENTION: 1048576
    """
    try:
        printer_info = win32print.GetPrinter(handle, 2)
        status = printer_info['Status']
        error_statuses = [
            win32print.PRINTER_STATUS_ERROR,
            win32print.PRINTER_STATUS_PAPER_JAM,
            win32print.PRINTER_STATUS_PAPER_OUT,
        ]
        return all((status & flag == 0) for flag in error_statuses)
    except Exception as e:
            print(f"Ошибка при проверке статуса принтера: {e}")
            return False


def queue(printer_list, file_list, type_files):
    """Печать постеров"""
    dev_mode_parameters = {
        "PaperSize": win32con.DMPAPER_A3,
        "Orientation": win32con.DMORIENT_PORTRAIT,
        "PrintQuality": win32con.DMRES_HIGH,
    }
    if type_files == 'Матовые':
        printer_list = [i.split('(')[0].strip() for i in printer_list if 'мат' in i]
    else:
        printer_list = [i.split('(')[0].strip() for i in printer_list if 'мат' not in i]
    if len(printer_list) == 0:
        return False
    # Циклическое распределение файлов по принтерам
    for file, printer in zip(file_list, itertools.cycle(printer_list)):
        logger.debug(f"Печать файла {file} на принтере {printer}")
        win32print.SetDefaultPrinter(printer)
        level = 2
        while True:
            try:
                print_defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
                printer_handle = win32print.OpenPrinter(printer, print_defaults)
                # Получаем текущую конфигурацию принтера
                printer_info = win32print.GetPrinter(printer_handle, level)
                dev_mode = printer_info["pDevMode"]
                # Применяем параметры конфигурации
                for key, value in dev_mode_parameters.items():
                    setattr(dev_mode, key, value)
                # Устанавливаем количество копий
                dev_mode.Copies = file[1]
                # Устанавливаем обновленную конфигурацию принтера
                win32print.SetPrinter(printer_handle, level, printer_info, 0)
                logger.info("Параметры печати успешно применены.")
                win32print.StartDocPrinter(printer_handle, 1, [file[0], None, "raw"])
                # 2 в начале для открытия pdf и его сворачивания, для открытия без сворачивания поменяйте на 1
                win32api.ShellExecute(2, 'print', file[0], '.', '/manualstoprint', 0)
                while True:
                    ready = is_printer_ready(printer_handle)
                    if ready:
                        logger.debug(win32print.GetPrinter(printer_handle, level)['pDevMode'].Copies)
                        logger.success(f"Принтер '{printer}' готов к печати.")
                        break
                    else:
                        logger.error(f"Принтер '{printer}' не готов к печати или его статус неизвестен.")
                        break
                break
            except Exception as e:
                logger.error(f"Ошибка при печати стикеров: {e}")
                try:
                    error_code = win32print.PRINTER_STATUS_ERROR
                    logger.info(f"Ошибка: {error_code}")
                except Exception as ex:
                    logger.error(f'Другая ошибка {ex}')
                    break
            finally:
                win32print.ClosePrinter(printer_handle)


def queue_sticker(printer_list, file_list, self=None):
    """Печать стикеров"""
    for file, printer in zip(file_list, itertools.cycle(printer_list)):
        logger.debug(f"Печать файла {file} на принтере {printer}")
        win32print.SetDefaultPrinter(printer)
        while True:
            try:
                printdefaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
                handle = win32print.OpenPrinter(printer, printdefaults)
                level = 2
                ## Получаем значения принтера
                attributes = win32print.GetPrinter(handle, level)
                ## Настройка количества копий
                attributes['pDevMode'].Copies = file[1]
                ## Передаем нужные значения в принтер
                win32print.SetPrinter(handle, level, attributes, 0)
                win32print.GetPrinter(handle, level)['pDevMode'].Copies
                # Предупреждаем принтер о старте печати
                win32print.StartDocPrinter(handle, 1, [file[0], None, "raw"])
                ## 2 в начале для открытия pdf и его сворачивания, для открытия без сворачивания поменяйте на 1
                win32api.ShellExecute(2, 'print', file[0], '.', '/manualstoprint', 0)
                while True:
                    ready = is_printer_ready(handle)
                    if ready:
                        logger.debug(win32print.GetPrinter(handle, level)['pDevMode'].Copies)
                        logger.success(f"Принтер '{printer}' готов к печати.")
                        break
                    else:
                        logger.error(f"Принтер '{printer}' не готов к печати или его статус неизвестен.")
                        break
                break
            except Exception as e:
                logger.error(f"Ошибка при печати стикеров: {e}")
                try:
                    error_code = win32print.PRINTER_STATUS_ERROR
                    logger.info(f"Ошибка: {error_code}")
                except Exception as ex:
                    logger.error(f'Другая ошибка {ex}')
                    break
            finally:
                win32print.ClosePrinter(handle)


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


if __name__ == '__main__':
    printer_list = ['Fax', 'Отправить в OneNote 16 (матовый)']
    order = [
        FilesOnPrint(art='POSTER-BLACKPINK-GLOSS', count=1, name='Постеры OG Buda картина А3 набор', status='✅'),
        FilesOnPrint(art='POSTER-BLACKPINK-MAT', count=2, name='Постер asdasdasd', status='✅')
    ]
    file_tuple = create_file_list(order)
    queue(printer_list, file_tuple, type_files='Матовые')
    #
    # printer_list = ['Отправить в OneNote 16']
    # order = [FilesOnPrint(art='POSTER-ATOMICHEART-GLOSS', count=2, name='Атомик', status='✅')]
    # file_tuple = create_file_list(order, stiker_path)
    # queue_sticker(printer_list, file_tuple)
