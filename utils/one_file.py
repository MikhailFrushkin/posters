import datetime
import os
import tempfile
from io import BytesIO

from reportlab.lib.pagesizes import A3
from reportlab.pdfgen import canvas
from PIL import Image
import glob
from loguru import logger
from config import ready_path, main_path


def one_pdf(folder_path, filename):
    # Ищем все файлы с расширениями PNG и JPG
    pdf_filename = f'{ready_path}\\{filename}.pdf'
    if os.path.exists(pdf_filename):
        logger.debug(f'Файл существует: {pdf_filename}')
    else:
        poster_files = glob.glob(f"{folder_path}/*.png") + glob.glob(f"{folder_path}/*.jpg")
        poster_files = sorted(poster_files)
        good_files = []
        for file in poster_files:
            name = file.split('\\')[-1].split('.')[0]
            if name.isdigit():
                good_files.append(file)

        # Создание нового PDF файла
        c = canvas.Canvas(pdf_filename, pagesize=A3)
        # Размещение каждого постера в виде очереди на отдельной странице PDF
        for i, poster_file in enumerate(good_files):
            image = Image.open(poster_file)
            width, height = image.size
            # logger.info(f'{poster_file} {width} {height}')
            if width > height:  # Горизонтальная ориентация
                rotated_image = image.rotate(90, expand=True)  # Поворот изображения на 90 градусов
                try:
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                        rotated_image.save(temp_file.name, format='JPEG')
                        c.drawImage(temp_file.name, 0, 0, width=A3[0], height=A3[1])
                except Exception as ex:
                    logger.error(ex)
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                        rotated_image.save(temp_file.name, format='PNG')
                        c.drawImage(temp_file.name, 0, 0, width=A3[0], height=A3[1])
            else:  # Вертикальная ориентация
                c.drawImage(poster_file, 0, 0, width=A3[0], height=A3[1])
            if i != len(poster_files) - 1:
                c.showPage()
        c.save()
        logger.success(f'Создан файл: {pdf_filename}')


if __name__ == '__main__':
    count = 0
    for address, dirs, files in os.walk(main_path):
        for dir in dirs:
            count += 1
            logger.info(f'{count}/{len(dirs)} Папка {dir}')
            time_start = datetime.datetime.now()
            one_pdf(folder_path=os.path.join(main_path, dir), filename=dir)
            logger.info(f'Время выполнения: {datetime.datetime.now() - time_start}')
    # one_pdf(folder_path=r'E:\Новая база\Готовые\poster-maneskin-mat', filename='poster-maneskin-mat')
    # one_pdf(folder_path=r'E:\Новая база\Готовые\poster-mandalaorecmech-gloss', filename='poster-mandalaorecmech-gloss')
