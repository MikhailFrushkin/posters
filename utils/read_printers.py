import win32print
from loguru import logger


def enum_printers() -> list:
    """Получение имен доступных принтеров"""
    flags = win32print.PRINTER_ENUM_LOCAL
    level = 2

    printers = win32print.EnumPrinters(flags, None, level)

    printer_list_name = [printer['pPrinterName'] for printer in printers]
    logger.info("Доступные принтеры: {}".format(", ".join(printer_list_name)))

    return printer_list_name
