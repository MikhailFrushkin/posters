import win32print
from loguru import logger


def enum_printers(start=None) -> list:
    """Получение имен доступных принтеров, подключенных по USB портам"""
    flags = win32print.PRINTER_ENUM_LOCAL
    level = 2

    printers = win32print.EnumPrinters(flags, None, level)

    usb_printers = []

    for printer in printers:
        for port in printer['pPortName'].split(','):
            if not start:
                if port.strip().startswith('USB'):
                    logger.info("\nИмя: {}".format(printer['pPrinterName']))
                    logger.info("Драйвер: {}".format(printer['pDriverName']))
                    logger.info("Порт: {}".format(port.strip()))
                    logger.info(
                        "Сетевой принтер: {}".format(printer['Attributes'] & win32print.PRINTER_ATTRIBUTE_NETWORK != 0))
                    logger.info("Статус: {}".format(printer['Status']))
                    logger.info("")

                    usb_printers.append(printer['pPrinterName'])
            else:
                usb_printers.append(printer['pPrinterName'])

    logger.info("Доступные принтеры, подключенные по USB: {}".format(", ".join(usb_printers)))
    return usb_printers


if __name__ == '__main__':
    enum_printers()
