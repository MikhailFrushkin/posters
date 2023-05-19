import cups
import os


def print_image(file_path, printer_name):
    # Создаем подключение к серверу CUPS
    conn = cups.Connection()

    # Получаем список доступных принтеров
    printers = conn.getPrinters()

    # Проверяем, существует ли указанный принтер
    if printer_name not in printers:
        print("Принтер '{}' не найден.".format(printer_name))
        return

    # Получаем настройки принтера
    printer_options = conn.getPrinterAttributes(printer_name)

    # Устанавливаем настройки печати (например, ориентацию и масштаб)
    job_options = {
        'media': printer_options['media-default'],  # Пример настройки типа бумаги
        'orientation-requested': cups.CUPS_ORIENTATION_LANDSCAPE,  # Пример настройки ориентации печати
        # Дополнительные настройки можно добавить по аналогии
    }

    # Отправляем файл изображения на печать
    print_job = conn.printFile(printer_name, file_path, "Print Job", job_options)

    # Проверяем статус печати
    print_status = conn.getJobAttributes(print_job, printer_name)
    if print_status['printer-state'] == cups.IPP_JOB_COMPLETED:
        print("Печать завершена.")
    else:
        print("Произошла ошибка при печати.")
        print("Статус печати:", print_status['printer-state-message'])


# Пример использования
image_folder = '/path/to/images'  # Путь к папке с изображениями
printer_name = 'printer_name'  # Имя принтера

# Обходим все файлы в папке с изображениями и отправляем их на печать
for filename in os.listdir(image_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        file_path = os.path.join(image_folder, filename)
        print_image(file_path, printer_name)
