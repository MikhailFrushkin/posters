import win32api
import win32print
import win32con
from loguru import logger


def apply_print_settings(printer_name: str, dev_mode_parameters: dict, file: str) -> None:
    """Найстройка выбранного принтера и печать файла"""
    print_defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
    printer_handle = win32print.OpenPrinter(printer_name, print_defaults)
    logger.debug(f"параметры принтера: {printer_handle}")
    try:
        # Получаем текущую конфигурацию принтера
        printer_info = win32print.GetPrinter(printer_handle, 2)
        dev_mode = printer_info["pDevMode"]

        # Применяем параметры конфигурации
        for key, value in dev_mode_parameters.items():
            setattr(dev_mode, key, value)

        # Устанавливаем обновленную конфигурацию принтера
        win32print.SetPrinter(printer_handle, 2, printer_info, 0)
        print("Параметры печати успешно применены.")
        # Предупреждаем принтер о старте печати
        win32print.StartDocPrinter(printer_handle, 1, [file, None, "raw"])
        # 2 в начале для открытия pdf и его сворачивания, для открытия без сворачивания поменяйте на 1
        win32api.ShellExecute(2, 'print', file, '.', '/manualstoprint', 0)
        ## "Закрываем" принтер
        win32print.ClosePrinter(printer_handle)

    except Exception as e:
        print("Ошибка при применении параметров печати:", str(e))
    finally:
        # Закрываем принтер
        win32print.ClosePrinter(printer_handle)


def enum_printers() -> list:
    """Получение имен доступных принтеров"""
    flags = win32print.PRINTER_ENUM_LOCAL
    level = 2

    printers = win32print.EnumPrinters(flags, None, level)

    printer_list_name = [printer['pPrinterName'] for printer in printers]
    logger.info("Доступный принтер: {}".format(*printer_list_name))
    return printer_list_name


if __name__ == '__main__':
    # размер, ориентация, качество
    dev_mode_parameters = {
        "PaperSize": win32con.DMPAPER_A3,
        "Orientation": win32con.DMORIENT_PORTRAIT,
        "PrintQuality": win32con.DMRES_HIGH,
    }

    printer_name = enum_printers()[0]
    file = 'temp/image.png'
    apply_print_settings(printer_name, dev_mode_parameters, file)