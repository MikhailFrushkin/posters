from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from environs import Env
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

path = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()

token = env.str('token')
main_path = 'E:\\Новая база\\Готовые'
ready_path = 'E:\\Новая база\\Готовые pdf'
stiker_path = 'E:\\Новая база\\!Стикеры'
path_base_y_disc = "/Значки ANIKOYA  02 23/03 - POSUTA (плакаты)"

class SearchProgress:
    def __init__(self, total_folders, progress_bar, current_folder=0):
        self.current_folder = current_folder
        self.total_folders = total_folders
        self.progress_bar = progress_bar

    def update_progress(self):
        self.current_folder += 1
        self.progress_bar.update_progress(self.current_folder, self.total_folders)

    def __str__(self):
        return str(self.current_folder)


@dataclass
class FilesOnPrint:
    art: str
    count: int
    name: Optional[str] = None
    status: str = '❌'
    # '✅'


def df_in_xlsx(df, filename, max_width=50):
    # Создание нового рабочего книги Excel
    workbook = Workbook()
    # Создание нового листа в рабочей книге
    sheet = workbook.active
    # Конвертация DataFrame в строки данных
    for row in dataframe_to_rows(df, index=False, header=True):
        sheet.append(row)
        # Ограничение ширины колонок
    for column in sheet.columns:
        column_letter = column[0].column_letter
        max_length = max(len(str(cell.value)) for cell in column)
        adjusted_width = min(max_length + 2, max_width)
        sheet.column_dimensions[column_letter].width = adjusted_width
    # Сохранение рабочей книги в файл
    workbook.save(f"{filename}.xlsx")
