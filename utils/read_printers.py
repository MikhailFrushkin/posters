import win32print
from loguru import logger


def enum_printers() -> list:
    """Получение имен доступных принтеров"""
    flags = win32print.PRINTER_ENUM_LOCAL
    level = 2

    printers = win32print.EnumPrinters(flags, None, level)

    for printer in printers:
        logger.info("\nИмя: {}".format(printer['pPrinterName']))
        logger.info("Драйвер: {}".format(printer['pDriverName']))
        logger.info("Порт: {}".format(printer['pPortName']))
        logger.info("Сетевой принтер: {}".format(printer['Attributes'] & win32print.PRINTER_ATTRIBUTE_NETWORK != 0))
        logger.info("Статус: {}".format(printer['Status']))
        logger.info("")
    printer_list_name = [printer['pPrinterName'] for printer in printers]
    logger.info("Доступные принтеры: {}".format(", ".join(printer_list_name)))

    return printer_list_name


if __name__ == '__main__':
    enum_printers()
