import datetime

from reportlab.lib.pagesizes import A3
from reportlab.pdfgen import canvas
from PIL import Image
import glob

from config import ready_path


def one_pdf(folder_path, filename):
    # Ищем все файлы с расширениями PNG и JPG
    poster_files = glob.glob(f"{folder_path}/*.png") + glob.glob(f"{folder_path}/*.jpg")
    poster_files = sorted(poster_files)

    # Создание нового PDF файла
    pdf_filename = f'{ready_path}\\{filename}.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=A3)
    # Размещение каждого постера в виде очереди на отдельной странице PDF
    for i, poster_file in enumerate(poster_files):
        c.drawImage(poster_file, 0, 0, width=A3[0], height=A3[1])
        if i != len(poster_files) - 1:
            c.showPage()
    c.save()


def combine_images(filepaths, output_filepath):
    # Определяем размер итогового изображения
    width, height = (297 * 3, 420)  # Размер А3: 297мм x 420мм

    # Создаем пустое изображение с необходимым размером
    combined_image = Image.new('RGB', (width, height))

    x_offset = 0
    for filepath in filepaths:
        # Открываем каждое изображение
        image = Image.open(filepath)

        # Масштабируем изображение до ширины А3
        scaled_image = image.resize((297, 420))

        # Вставляем масштабированное изображение в пустое изображение
        combined_image.paste(scaled_image, (x_offset, 0))

        # Увеличиваем смещение для следующего изображения
        x_offset += 297

    # Сохраняем итоговое изображение
    combined_image.save(output_filepath)


if __name__ == '__main__':
    time_start = datetime.datetime.now()
    one_pdf(folder_path='/home/mikhail/PycharmProjects/posters/posters')
    print(f'Время выполнения: {datetime.datetime.now() - time_start}')
