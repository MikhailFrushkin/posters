import itertools

import win32api
import win32con
import win32print
from loguru import logger

from utils.search_file import search_file


def queue(printer_list, file_list):
    dev_mode_parameters = {
        "PaperSize": win32con.DMPAPER_A3,
        "Orientation": win32con.DMORIENT_PORTRAIT,
        "PrintQuality": win32con.DMRES_HIGH,
    }

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
            print("Ошибка при применении параметров печати:", str(e))
        finally:
            # Закрываем принтер
            win32print.ClosePrinter(printer_handle)


def create_file_list(orders: dict) -> list:
    directory = r'C:\Users\A3_posters\Готовые постеры по 3 шт'
    file_list = list()
    for key, value in orders.items():
        file_list.append((search_file(f"{key}.pdf", directory), value))
    return file_list


if __name__ == '__main__':
    printer_list = ['Отправить в OneNote 16', 'Fax']
    order = {'POSTER-ATOMICHEART-GLOSS': 3, 'POSTER-BLACKPINK-GLOSS': 2}
    file_list = create_file_list(order)
    # print(file_list)
    queue(printer_list, file_list)
