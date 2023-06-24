import os

from PyQt5.QtWidgets import QApplication, QSpinBox, QVBoxLayout, QDialog, QDialogButtonBox
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QImage, QPainter

from config import ready_path


class PrintDialog(QDialog):
    def __init__(self, file_paths):
        super().__init__()

        self.file_paths = file_paths
        self.printer = QPrinter()
        self.printer.setPrinterName("Мой принтер")  # Установите имя вашего принтера

        self.print_dialog = QPrintDialog(self.printer, self)
        self.print_dialog.setOptions(QPrintDialog.PrintToFile | QPrintDialog.PrintPageRange)

        self.copy_spinboxes = []

        layout = QVBoxLayout()
        for file_path in self.file_paths:
            document = QFileInfo(file_path)
            if document.exists() and document.isFile():
                copy_spinbox = QSpinBox()
                copy_spinbox.setMinimum(1)
                copy_spinbox.setMaximum(100)
                copy_spinbox.setValue(1)
                self.copy_spinboxes.append(copy_spinbox)

                layout.addWidget(copy_spinbox)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.print_documents)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def print_documents(self):
        if self.print_dialog.exec_() != QPrintDialog.Accepted:
            return  # Пользователь отменил диалог печати

        for file_path, copy_spinbox in zip(self.file_paths, self.copy_spinboxes):
            document = QFileInfo(file_path)
            if document.exists() and document.isFile():
                num_copies = copy_spinbox.value()
                for _ in range(num_copies):
                    self.printer.setOutputFileName(file_path)
                    self.printer.setOutputFormat(QPrinter.PdfFormat)
                    self.printer.setDocName(document.fileName())
                    self.printer.setFullPage(True)

                    # Вывод на печать
                    image = QImage(file_path)
                    self.printer.newPage()
                    painter = QPainter(self.printer)
                    painter.drawImage(0, 0, image)
                    painter.end()


app = QApplication([])
file_paths = [
    os.path.join(ready_path, 'poster-tinybunny.xariton-mat-3.pdf'),
    os.path.join(ready_path, 'poster-slavya.bl-gloss-3.pdf')
]
print_dialog = PrintDialog(file_paths)
print_dialog.exec_()
