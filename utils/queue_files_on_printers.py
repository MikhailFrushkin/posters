import itertools
import time

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
    Присоединенное к системе устройство не работает.: 31
    """
    try:
        printer_info = win32print.GetPrinter(handle, 2)
        status = printer_info['Status']
        logger.debug(f'Статуса принтера {status}')
        error_statuses = [
            win32print.PRINTER_STATUS_ERROR,
            win32print.PRINTER_STATUS_PAPER_JAM,
            win32print.PRINTER_STATUS_PAPER_OUT,
            win32print.PRINTER_STATUS_PRINTING,
        ]
        return all((status & flag == 0) for flag in error_statuses)
    except Exception as e:
        print(f"Ошибка при проверке статуса принтера: {e}")
        return False


def queue(printer_list, file_list, type_files, self=None):
    """Печать постеров"""
    if self:
        self.progress_label.setText("Прогресс: 0%")
        self.progress_bar.setValue(0)
        total = len(file_list)
        completed = 0
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
    # # Циклическое распределение файлов по принтерам
    # for file, printer in zip(file_list, itertools.cycle(printer_list)):
    #     logger.debug(f"Печать файла {file} на принтере {printer}")
    #     win32print.SetDefaultPrinter(printer)
    #     level = 2
    #     while True:
    #         try:
    #             print_defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
    #             printer_handle = win32print.OpenPrinter(printer, print_defaults)
    #             # Получаем текущую конфигурацию принтера
    #             printer_info = win32print.GetPrinter(printer_handle, level)
    #             dev_mode = printer_info["pDevMode"]
    #             # Применяем параметры конфигурации
    #             for key, value in dev_mode_parameters.items():
    #                 setattr(dev_mode, key, value)
    #             # Устанавливаем количество копий
    #             dev_mode.Copies = file[1]
    #             # Устанавливаем обновленную конфигурацию принтера
    #             win32print.SetPrinter(printer_handle, level, printer_info, 0)
    #             logger.info("Параметры печати успешно применены.")
    #             win32print.StartDocPrinter(printer_handle, 1, [file[0], None, "raw"])
    #             # 2 в начале для открытия pdf и его сворачивания, для открытия без сворачивания поменяйте на 1
    #             win32api.ShellExecute(2, 'print', file[0], '.', '/manualstoprint', 0)
    #             while True:
    #                 ready = is_printer_ready(printer_handle)
    #                 if ready:
    #                     logger.debug(win32print.GetPrinter(printer_handle, level)['pDevMode'].Copies)
    #                     logger.success(f"Принтер '{printer}' готов к печати.")
    #                     break
    #                 else:
    #                     logger.error(f"Принтер '{printer}' не готов к печати или его статус неизвестен.")
    #                     break
    #             break
    #         except Exception as e:
    #             logger.error(f"Ошибка при печати постеров: {e}")
    #             try:
    #                 error_code = win32print.PRINTER_STATUS_ERROR
    #                 logger.info(f"Ошибка: {error_code}")
    #             except Exception as ex:
    #                 logger.error(f'Другая ошибка {ex}')
    #                 break
    #         finally:
    #             win32print.ClosePrinter(printer_handle)
    printer_status = [False] * len(printer_list)
    count = 0

    for file, printer in zip(file_list, itertools.cycle(printer_list)):
        logger.debug(f"Печать файла {file} на принтере {printer}")
        level = 2
        while True:
            try:
                # Проверяем статусы всех принтеров
                for index, printer_name in enumerate(printer_list):
                    if not printer_status[index]:
                        # Если принтер не занят печатью, используем его
                        win32print.SetDefaultPrinter(printer)
                        print_defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
                        printer_handle = win32print.OpenPrinter(printer_name, print_defaults)
                        printer_info = win32print.GetPrinter(printer_handle, level)
                        dev_mode = printer_info["pDevMode"]
                        dev_mode.Copies = file[1]
                        # Применяем параметры конфигурации
                        for key, value in dev_mode_parameters.items():
                            setattr(dev_mode, key, value)
                        win32print.SetPrinter(printer_handle, level, printer_info, 0)
                        logger.info("Параметры печати успешно применены.")
                        hJob = win32print.StartDocPrinter(printer_handle, 1, [file[0], None, "raw"])
                        job_info = win32print.GetJob(printer_handle, hJob, win32print.JOB_INFO_1)
                        win32api.ShellExecute(2, 'print', file[0], '.', '/manualstoprint', 0)
                        while job_info["Status"] != win32print.JOB_STATUS_COMPLETE:
                            logger.debug(job_info["Status"])
                            time.sleep(5)
                            # job_info = win32print.GetJob(printer_handle, hJob, win32print.JOB_INFO_1)
                            job_info["Status"] = win32print.JOB_STATUS_COMPLETE
                            logger.debug(job_info["Status"])
                        logger.success(f"Принтер '{printer_name}' завершил печать файла.")
                        count += 1
                        printer_status[index] = False  # Устанавливаем флаг принтера как свободный
                        if self:
                            completed += 1
                            progress = int((completed / total) * 100)
                            self.progress_label.setText(f"Прогресс: {progress}%")
                            self.progress_bar.setValue(progress)
                        break  # Выходим из цикла проверки принтеров
                else:
                    # Если все принтеры заняты печатью, ждем 1 секунду и повторяем цикл
                    time.sleep(1)
                    continue
                break  # Выходим из основного цикла печати
            except Exception as e:
                logger.error(f"Ошибка при печати стикеров: {e}")
                try:
                    error_code = win32print.PRINTER_STATUS_ERROR
                    logger.info(f"Ошибка: {error_code}")
                except Exception as ex:
                    logger.error(f'Другая ошибка {ex}')
                    break
            finally:
                try:
                    win32print.ClosePrinter(printer_handle)
                except Exception as ex:
                    logger.error(ex)
                break


def queue_sticker(printer_list, file_list, self=None):
    """Печать стикеров"""
    # Создаем список флагов для отслеживания статуса принтеров
    printer_status = [False] * len(printer_list)
    count = 0

    for file, printer in zip(file_list, itertools.cycle(printer_list)):
        logger.debug(f"Печать файла {file} на принтере {printer}")
        level = 2
        self.progress_bar.setValue(count + 1)
        while True:
            try:
                # Проверяем статусы всех принтеров
                for index, printer_name in enumerate(printer_list):
                    if not printer_status[index]:
                        # Если принтер не занят печатью, используем его
                        filename = file[0].split('\\')[-1]
                        self.progress_label.setText(f"Печать: {filename} на принтер: {printer}")
                        win32print.SetDefaultPrinter(printer)
                        print_defaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
                        printer_handle = win32print.OpenPrinter(printer_name, print_defaults)
                        printer_info = win32print.GetPrinter(printer_handle, level)
                        dev_mode = printer_info["pDevMode"]
                        dev_mode.Copies = file[1]
                        win32print.SetPrinter(printer_handle, level, printer_info, 0)
                        logger.info("Параметры печати успешно применены.")
                        hJob = win32print.StartDocPrinter(printer_handle, 1, [file[0], None, "raw"])
                        job_info = win32print.GetJob(printer_handle, hJob, win32print.JOB_INFO_1)
                        win32api.ShellExecute(2, 'print', file[0], '.', '/manualstoprint', 0)
                        while job_info["Status"] != win32print.JOB_STATUS_COMPLETE:
                            logger.debug(job_info["Status"])
                            time.sleep(3)
                            # job_info = win32print.GetJob(printer_handle, hJob, win32print.JOB_INFO_1)
                            job_info["Status"] = win32print.JOB_STATUS_COMPLETE
                            logger.debug(job_info["Status"])
                        logger.success(f"Принтер '{printer_name}' завершил печать файла.")
                        count += 1
                        printer_status[index] = False  # Устанавливаем флаг принтера как свободный
                        # win32print.ClosePrinter(printer_handle)
                        break  # Выходим из цикла проверки принтеров
                else:
                    # Если все принтеры заняты печатью, ждем 1 секунду и повторяем цикл
                    time.sleep(1)
                    continue
                break  # Выходим из основного цикла печати
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
                break
    self.reject()


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
    # printer_list = ['Fax', 'Отправить в OneNote 16 (матовый)']
    # order = [
    #     FilesOnPrint(art='POSTER-BLACKPINK-GLOSS', count=1, name='Постеры OG Buda картина А3 набор', status='✅'),
    #     FilesOnPrint(art='POSTER-BLACKPINK-MAT', count=2, name='Постер asdasdasd', status='✅')
    # ]
    # file_tuple = create_file_list(order)
    # queue(printer_list, file_tuple, type_files='Матовые')

    printer_list = ['Fax']
    order = [FilesOnPrint(art='POSTER-BITVA.MATVEEVD-GLOSS-3', count=1,
                          name='Постеры Дмитрий Матвеев Чернокнижник постеры Интерьерные', status='✅'),
             FilesOnPrint(art='POSTER-BITVA.MATVEEVD-GLOSS-6', count=2,
                          name='Постеры Дмитрий Матвеев Чернокнижник постеры Интерьерные', status='✅'),
             FilesOnPrint(art='POSTER-BITVA.SHEPSOLEG-MAT-3', count=1, name='Постеры Олег Шепс постеры Интерьерные А3',
                          status='✅')]
    file_tuple = create_file_list(order, stiker_path)
    queue_sticker(printer_list, file_tuple)
