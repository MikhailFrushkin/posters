import datetime
import glob
import os

import pandas as pd
from PIL import Image
from loguru import logger
from config import df_in_xlsx
list_bad = []


def one_pdf(folder_path, filename):
    global list_bad
    poster_files = glob.glob(f"{folder_path}/*.png") + glob.glob(f"{folder_path}/*.jpg")
    poster_files = sorted(poster_files)
    good_files = []
    for file in poster_files:
        name = file.split('\\')[-1].split('.')[0]
        if name.isdigit():
            good_files.append(file)
    logger.success(good_files)
    for i, poster_file in enumerate(good_files):
        image = Image.open(poster_file)
        width, height = image.size
        if width > height:  # Горизонтальная ориентация
            logger.info(f'{poster_file} {width} {height}')
            list_bad.append(filename)


if __name__ == '__main__':
    count = 0
    main_path = 'E:\\Новая база\\Готовые'
    ready_path = 'E:\\Новая база\\Готовые pdf'
    stiker_path = 'E:\\Новая база\\!Стикеры'
    for address, dirs, files in os.walk(main_path):
        for dir in dirs:
            count += 1
            logger.info(f'{count}/{len(dirs)} Папка {dir}')
            time_start = datetime.datetime.now()
            one_pdf(folder_path=os.path.join(main_path, dir), filename=dir)
            logger.info(f'Время выполнения: {datetime.datetime.now() - time_start}')
    logger.error(list_bad)
    df = pd.DataFrame(set(list_bad), columns=['Артикул'])
    df_in_xlsx(df, 'Объединеные артикула для проверки')
