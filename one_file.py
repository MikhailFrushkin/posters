import datetime

from reportlab.lib.pagesizes import A3
from reportlab.pdfgen import canvas
import glob


def one_pdf(folder_path):
    # Ищем все файлы с расширениями PNG и JPG
    poster_files = glob.glob(f"{folder_path}/*.png") + glob.glob(f"{folder_path}/*.jpg")
    poster_files = sorted(poster_files)
    # Выводим найденные файлы
    for file_path in poster_files:
        print(file_path)
    # Создание нового PDF файла
    pdf_filename = 'combined_posters.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=A3)
    # Размещение каждого постера в виде очереди на отдельной странице PDF
    for i, poster_file in enumerate(poster_files):
        c.drawImage(poster_file, 0, 0, width=A3[0], height=A3[1])
        if i != len(poster_files) - 1:
            c.showPage()
    c.save()


if __name__ == '__main__':
    time_start = datetime.datetime.now()
    one_pdf(folder_path='/home/mikhail/PycharmProjects/posters/posters')
    print(f'Время выполнения: {datetime.datetime.now() - time_start}')
