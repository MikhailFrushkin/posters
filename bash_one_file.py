import subprocess

# Путь к исполняемому файлу GIMP
GIMP_PATH = '/usr/bin/gimp'

# Путь к изображениям, которые нужно добавить
IMAGE1 = "C:\\Users\\A3_posters\\1.png"
IMAGE2 = "C:\\Users\\A3_posters\\2.png"
IMAGE3 = "C:\\Users\\A3_posters\\3.png"

# Название и путь для сохранения результирующего изображения
OUTPUT_IMAGE = "результирующему_изображению.png"

# Размер нового изображения А3 в пикселях (420 мм x 297 мм при 300 пикселей/дюйм)
WIDTH = 4961
HEIGHT = 3508

# Создание временного bash-скрипта
bash_script = f"""#!/bin/bash
gimp -i -b - <<EOF
(let* (
        (image-path "{OUTPUT_IMAGE}")
        (image (car (gimp-file-load RUN-NONINTERACTIVE "{IMAGE1}" "{IMAGE1}")))
        (drawable (car (gimp-image-get-active-layer image)))
        (x 0)
        (y 0)
      )
  (gimp-image-resize image 4961 3508 0 0)
  (gimp-image-set-filename image image-path)

  (foreach layer-path '("{IMAGE2}" "{IMAGE3}")
    (begin
      (let (
             (new-layer (car (gimp-file-load-layer image layer-path)))
           )
        (gimp-layer-set-offsets new-layer x y)
        (gimp-image-add-layer image new-layer 0)
      )
      (set! x (if (> (+ x (/ (car (gimp-drawable-width drawable)) 2)) (car (gimp-image-width image))) 0 (+ x (/ (car (gimp-drawable-width drawable)) 2))))
      (set! y (if (> (+ y (/ (car (gimp-drawable-height drawable)) 2)) (car (gimp-image-height image))) 0 (+ y (/ (car (gimp-drawable-height drawable)) 2))))
    )
  )
  (gimp-file-save RUN-NONINTERACTIVE image drawable image-path image-path)
  (gimp-image-delete image)
)

(gimp-quit 0)
EOF
"""

subprocess.run(bash_script, shell=False)
