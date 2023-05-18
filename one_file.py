from reportlab.lib.pagesizes import A3
from reportlab.pdfgen import canvas

# Список файлов постеров
poster_files = [
    '1.png',
    '2.png',
    '3.png',
]

# Создание нового PDF файла
pdf_filename = 'combined_posters.pdf'
c = canvas.Canvas(pdf_filename, pagesize=A3)

# Размещение каждого постера в виде очереди на отдельной странице PDF
for i, poster_file in enumerate(poster_files):
    c.drawImage(poster_file, 0, 0, width=A3[0], height=A3[1])
    if i != len(poster_files) - 1:
        c.showPage()

# Завершение создания PDF файла
c.save()