import itertools

import win32api
import win32con
import win32print
from loguru import logger

from config import FilesOnPrint, ready_path, stiker_path
from utils.search_file import search_file


def is_printer_ready(printer_name):
    try:
        printer_info = win32print.GetPrinter(printer_name, 2)
        status = printer_info['Status']
        ready_statuses = [
            win32print.PRINTER_STATUS_PRINTING,
            win32print.PRINTER_STATUS_PROCESSING,
        ]
        return any(status & ready_status for ready_status in ready_statuses)
    except Exception as e:
        print(f"Ошибка при проверке статуса принтера: {e}")
        return False


def queue(printer_list, file_list, type_files):
    """
    0: PRINTER_STATUS_PAUSED - принтер приостановлен
    1: PRINTER_STATUS_ERROR - ошибка принтера
    2: PRINTER_STATUS_PENDING_DELETION - принтер ожидает удаления
    3: PRINTER_STATUS_PAPER_JAM - замятие бумаги в принтере
    4: PRINTER_STATUS_PAPER_OUT - бумага в принтере закончилась
    5: PRINTER_STATUS_MANUAL_FEED - требуется ручная подача бумаги
    6: PRINTER_STATUS_PAPER_PROBLEM - проблема с бумагой
    7: PRINTER_STATUS_OFFLINE - принтер находится в автономном режиме
    8: PRINTER_STATUS_IO_ACTIVE - активная операция ввода-вывода
    9: PRINTER_STATUS_BUSY - принтер занят
    10: PRINTER_STATUS_PRINTING - принтер выполняет печать
    11: PRINTER_STATUS_OUTPUT_BIN_FULL - выходной лоток принтера заполнен
    12: PRINTER_STATUS_NOT_AVAILABLE - принтер недоступен
    13: PRINTER_STATUS_WAITING - ожидание принтера
    14: PRINTER_STATUS_PROCESSING - принтер обрабатывает задание
    15: PRINTER_STATUS_INITIALIZING - принтер инициализируется
    16: PRINTER_STATUS_WARMING_UP - принтер прогревается
    17: PRINTER_STATUS_TONER_LOW - низкий уровень тонера
    18: PRINTER_STATUS_NO_TONER - нет тонера
    """
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
        while True:
            try:
                print_defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
                printer_handle = win32print.OpenPrinter(printer, print_defaults)
                logger.info(f"параметры принтера: {printer_handle}")

                # Получаем текущую конфигурацию принтера
                printer_info = win32print.GetPrinter(printer_handle, 2)

                dev_mode = printer_info["pDevMode"]

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
                while True:
                    printer_info = win32print.GetPrinter(printer_handle, 2)
                    status = printer_info['Status']
                    if status is not None:
                        logger.debug(f"Статус принтера '{printer}': {status}")
                        ready = is_printer_ready(printer)
                        if ready:
                            logger.success(f"Принтер '{printer}' готов к печати.")
                            break
                        else:
                            logger.error(f"Принтер '{printer}' не готов к печати или его статус неизвестен.")
                            break

                break

            except Exception as e:
                logger.error(f"Ошибка при применении параметров печати: {e}")
                try:
                    error_code = win32print.PRINTER_STATUS_ERROR()
                    if error_code == win32print.PRINTER_STATUS_PAPER_OUT:
                        logger.info("Ошибка: Нет бумаги")

                except Exception as ex:
                    logger.error(f'Другая ошибка {ex}')
                    break
            finally:
                win32print.ClosePrinter(printer_handle)


def queue_stikers(printer_list, file_list):
    # Циклическое распределение файлов по принтерам

    for file, printer in zip(file_list, itertools.cycle(printer_list)):
        logger.debug(f"Печать файла {file} на принтере {printer}")
        win32print.SetDefaultPrinter(printer)
        try:
            logger.debug(file)
            print_defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
            printer_handle = win32print.OpenPrinter(printer, print_defaults)
            # Получаем текущую конфигурацию принтера
            printer_info = win32print.GetPrinter(printer_handle, 2)
            dev_mode = printer_info["pDevMode"]
            # Устанавливаем количество копий
            dev_mode.Copies = file[1]
            printer_info["pDevMode"] = dev_mode
            win32print.SetPrinter(printer_handle, 2, printer_info, 0)
            logger.info("Параметры печати успешно применены.")
            win32print.StartDocPrinter(printer_handle, 1, [file[0], None, "raw"])
            # 2 в начале для открытия pdf и его сворачивания, для открытия без сворачивания поменяйте на 1
            win32api.ShellExecute(2, 'print', file[0], '.', '/manualstoprint', 0)
        except Exception as e:
            logger.error(f"Ошибка при печати стикеров: {e}")
            try:
                error_code = win32print.PRINTER_STATUS_ERROR()
                if error_code == win32print.PRINTER_STATUS_PAPER_OUT:
                    logger.info("Ошибка: Нет бумаги")
            except Exception as ex:
                logger.error(f'Другая ошибка {ex}')
                break
        finally:
            win32print.ClosePrinter(printer_handle)


def create_file_list(orders, directory=ready_path):
    file_tuple = tuple()
    for item in orders:
        path_file = search_file(f"{item.art}.pdf", directory)
        file_tuple += ((path_file, item.count),)
    return file_tuple


if __name__ == '__main__':
    # printer_list = ['Fax', 'Отправить в OneNote 16 (матовый)']
    # order = [
    #     FilesOnPrint(art='POSTER-BLACKPINK-GLOSS', count=1, name='Постеры OG Buda картина А3 набор', status='✅'),
    #     FilesOnPrint(art='POSTER-BLACKPINK-MAT', count=1, name='Постер asdasdasd', status='✅')
    # ]
    # file_tuple = create_file_list(order)
    # queue(printer_list, file_tuple, type_files='Матовые')

    printer_list = ['Xprinter XP-365B']
    order = [FilesOnPrint(art='POSTER-ATOMICHEART-GLOSS', count=2, name='Атомик', status='✅'),
             FilesOnPrint(art='POSTER-BLACKPINK-MAT', count=1, name='Постер asdasdasd', status='✅')]
    file_tuple = create_file_list(order, stiker_path)
    queue_stikers(printer_list, file_tuple)
