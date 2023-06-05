import subprocess
import os


gimp_path = '/usr/bin/gimp'

# Имя файла, содержащего слои

# Папка для сохранения нового файла
folder = '/home/mikhail/PycharmProjects/posters/temp'

def add_images_to_gimp(file_path, image_paths):
    # Формируем команду для вызова GIMP с необходимыми параметрами
    cmd = [f'{gimp_path}', '--no-interface', '-b',
           '(python-fu-batch-add-layers RUN-NONINTERACTIVE "{}" "{}" "{}")'.format(file_path, *image_paths)]

    # Вызываем GIMP с помощью subprocess
    subprocess.run(cmd, check=True)


# Пример использования
file_path = '/home/mikhail/PycharmProjects/posters/temp/слоями.xcf'
image_paths = ['/home/mikhail/PycharmProjects/posters/1 В.png',
               '/home/mikhail/PycharmProjects/posters/2 В.png',
               '/home/mikhail/PycharmProjects/posters/3 В.png']

# add_images_to_gimp(file_path, image_paths)


def qwerty(filename):
    gimp_command = [
        gimp_path,
        '-i',
        '-b',
        f'(gimp-file-load RUN-NONINTERACTIVE "{filename}" "{filename}")',
        '-b',
        '(gimp-image-undo-group-start 1)',  # Начало группы отмены действий
        '-b',
        '(gimp-layer-new-from-visible (car (gimp-image-get-active-drawable (aref (cadr (gimp-image-list)) 0))))',  # Дублирование слоя
        '-b',
        '(gimp-image-add-layer (aref (cadr (gimp-image-list)) 0) (car (gimp-layer-new-from-visible (car (gimp-image-get-active-drawable (aref (cadr (gimp-image-list)) 0))))))',  # Добавление дублированного слоя
        '-b',
        '(gimp-image-add-layer (aref (cadr (gimp-image-list)) 0) (car (gimp-layer-new-from-visible (car (gimp-image-get-active-drawable (aref (cadr (gimp-image-list)) 0))))))',  # Добавление еще одного дублированного слоя
        '-b',
        '(gimp-image-undo-group-end 1)',  # Конец группы отмены действий
        '-b',
        f'(gimp-file-save RUN-NONINTERACTIVE 1 (car (gimp-image-merge-visible-layers (aref (cadr (gimp-image-list)) 0) 0)) '
        f'"{os.path.join(folder, "new.xcf")}" "new.xcf")',
        '-b',
        '(gimp-quit 0)'
    ]
    subprocess.run(gimp_command, shell=False)


qwerty('/home/mikhail/PycharmProjects/site_Yaroslav/main/files/SKZ-5NEW-NABORxPLYAZH37/SKZ-5NEW-NABORxPLYAZH37.xcf')

