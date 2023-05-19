import win32print
import win32con


def apply_print_settings(printer_name, dev_mode_parameters):
    """Найстройка выбранного принтера"""
    printer_handle = win32print.OpenPrinter(printer_name)
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
    except Exception as e:
        print("Ошибка при применении параметров печати:", str(e))
    finally:
        # Закрываем принтер
        win32print.ClosePrinter(printer_handle)


def enum_printers():
    """Получение имен доступных принтеров"""
    flags = win32print.PRINTER_ENUM_LOCAL
    level = 2

    printers = win32print.EnumPrinters(flags, None, level)
    for printer in printers:
        name = printer
        print("Printer Name:", name['pPrinterName'])


enum_printers()

printer_name = "Отправить в OneNote 16"
#размер, ориентация, качество
dev_mode_parameters = {
    "PaperSize": win32con.DMPAPER_A3,
    "Orientation": win32con.DMORIENT_PORTRAIT,
    "PrintQuality": win32con.DMRES_HIGH,
}

apply_print_settings(printer_name, dev_mode_parameters)
