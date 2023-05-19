import win32print
import os


def print_image(file_path, printer_name):
    # Открываем принтер
    printer = win32print.OpenPrinter(printer_name)

    # Получаем настройки принтера
    default_printer_info = win32print.GetPrinter(printer, 2)

    # Устанавливаем настройки печати (например, ориентацию и масштаб)
    devmode = win32print.DocumentProperties(None, printer, printer_name, default_printer_info['pDevMode'], None, 0)
    devmode.Orientation = win32print.DMORIENT_LANDSCAPE  # Пример настройки ориентации печати
    # devmode.Scale = 50  # Пример настройки масштаба печати
    # devmode.Color = win32print.DMCOLOR_COLOR  # Пример настройки цветности печати

    # Открываем файл изображения
    with open(file_path, 'rb') as file:
        # Создаем объект документа для печати
        hprinter = win32print.GetPrinter(printer, 2)['hPrinter']
        hjob = win32print.StartDocPrinter(hprinter, 1, ('Print Job', None, 'RAW'))
        win32print.StartPagePrinter(hprinter)

        # Читаем данные из файла и записываем их в очередь печати
        data = file.read()
        win32print.WritePrinter(hprinter, data)

        # Завершаем страницу и документ
        win32print.EndPagePrinter(hprinter)
        win32print.EndDocPrinter(hprinter)

    # Закрываем принтер
    win32print.ClosePrinter(printer)


# Пример использования
image_folder = 'C:/path/to/images'  # Путь к папке с изображениями
printer_name = win32print.GetDefaultPrinter()  # Получаем имя текущего принтера

# Обходим все файлы в папке с изображениями и отправляем их на печать
for filename in os.listdir(image_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        file_path = os.path.join(image_folder, filename)
        print_image(file_path, printer_name)
