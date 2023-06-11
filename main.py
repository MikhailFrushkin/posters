from pathlib import Path

import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QCheckBox
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView, \
    QAbstractItemView
from loguru import logger

from config import FilesOnPrint, ready_path
from utils.read_excel import read_excel_file
from utils.read_printers import enum_printers
from utils.search_file import search_file


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 738)
        font = QtGui.QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(font)
        self.verticalLayout_2.addWidget(self.label_3)
        self.listView = QtWidgets.QListView(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.listView.setFont(font)
        self.listView.setMinimumSize(300, 500)
        self.listView.setObjectName("listView")
        self.verticalLayout_2.addWidget(self.listView)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(17, 119, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setMaxLength(154000)
        self.lineEdit.setFrame(True)
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pushButton_2)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 688, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Список артикулов:"))
        self.label_2.setText(_translate("MainWindow", "Доступные принтеры для печати:"))
        self.label.setText(_translate("MainWindow", "Выберите файл заказа:"))
        self.pushButton.setText(_translate("MainWindow", "Загрузить файл "))
        self.pushButton_2.setText(_translate("MainWindow", "Сформировать очереди"))


class QueueDialog(QWidget):
    def __init__(self, files_on_print, printers, title, parent=None):
        super().__init__(parent)
        self.files_on_print = files_on_print
        self.printers = printers
        self.setWindowTitle(title)

        layout = QVBoxLayout(self)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(4)  # Добавление колонки "Название"
        self.tableWidget.setMinimumSize(800, 300)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Название", "Артикул", "Количество", "Найден"])  # Обновленные заголовки

        font = self.tableWidget.font()
        font.setPointSize(14)
        self.tableWidget.setFont(font)

        self.tableWidget.setRowCount(len(self.files_on_print))

        for row, file_on_print in enumerate(self.files_on_print):
            name_item = QTableWidgetItem(file_on_print.name)  # Получение названия из датакласса
            art_item = QTableWidgetItem(file_on_print.art)
            count_item = QTableWidgetItem(str(file_on_print.count))
            status_item = QTableWidgetItem(str(file_on_print.status))
            self.tableWidget.setItem(row, 0, name_item)  # Установка элемента в колонку "Название"
            self.tableWidget.setItem(row, 1, art_item)
            self.tableWidget.setItem(row, 2, count_item)
            self.tableWidget.setItem(row, 3, status_item)

        layout.addWidget(self.tableWidget)

        font = self.tableWidget.font()

        print_button = QPushButton("Печать", self)
        print_button.setFont(font)
        print_button.clicked.connect(self.evt_btn_print_clicked)
        layout.addWidget(print_button)

        print_all_button = QPushButton("Печатать все", self)
        print_all_button.setFont(font)
        print_all_button.clicked.connect(self.evt_btn_print_all_clicked)
        layout.addWidget(print_all_button)

        # Установка режима выделения целых строк
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Установка ширины колонки "Артикул" в 80% от ширины окна
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    def evt_btn_print_clicked(self):
        selected_data = self.get_selected_data()
        if selected_data:
            QMessageBox.information(self, 'Отправка на печать', "Отправлено на печать:\n{}".format(
                '\n'.join([f'{item.art}, {item.count} шт.' for item in selected_data])))
            print(self.windowTitle())
        else:
            QMessageBox.information(self, 'Отправка на печать', 'Ни одна строка не выбрана')

    def evt_btn_print_all_clicked(self):
        all_data = self.get_all_data()
        print(self.windowTitle())

        if all_data:
            QMessageBox.information(self, 'Отправка на печать', "Отправлено на печать:\n{}".format(
                '\n'.join([f'{item.art}, {item.count} шт.' for item in all_data])))
        else:
            QMessageBox.information(self, 'Отправка на печать', 'Таблица пуста')

    def get_selected_data(self):
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        data = []
        for row in selected_rows:
            name = self.tableWidget.item(row.row(), 0).text()
            art = self.tableWidget.item(row.row(), 1).text()
            count = self.tableWidget.item(row.row(), 2).text()
            status = self.tableWidget.item(row.row(), 3).text()
            if status == '✅':
                data.append(FilesOnPrint(name=name, art=art, count=int(count)))
        return data

    def get_all_data(self):
        data = []
        for row in range(self.tableWidget.rowCount()):
            name = self.tableWidget.item(row, 0).text()
            art = self.tableWidget.item(row, 1).text()
            count = self.tableWidget.item(row, 2).text()
            status = self.tableWidget.item(row, 3).text()
            if status == '✅':
                data.append(FilesOnPrint(name=name, art=art, count=int(count)))
        return data


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_dir = Path.cwd()
        self.pushButton.clicked.connect(self.evt_btn_open_file_clicked)
        self.pushButton_2.clicked.connect(self.evt_btn_create_queue)
        try:
            printers_list = enum_printers()
            for printer in printers_list:
                self.addPrinterCheckbox(printer)
                self.addPrinterCheckbox(printer, is_matte=True)

        except Exception as ex:
            logger.debug(ex)
        self.dialogs = []

    def update_list_view(self, values):
        model = QtCore.QStringListModel()
        model.setStringList(values)
        self.listView.setModel(model)

    def addPrinterCheckbox(self, printer_name, is_matte=False):
        checkbox = QCheckBox(self.formatPrinterName(printer_name, is_matte), self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        checkbox.setFont(font)
        checkbox.setObjectName(printer_name)
        self.verticalLayout.addWidget(checkbox)

    def formatPrinterName(self, printer_name, is_matte):
        if is_matte:
            return printer_name + " (матовый)"
        else:
            return printer_name

    def evt_btn_open_file_clicked(self):
        """Ивент на кнопку загрузить файл"""
        res = QFileDialog.getOpenFileName(self, 'Загрузить файл', f'{self.current_dir}', 'Лист XLSX (*.xlsx)')
        if res[0] != '':
            self.lineEdit.setText(res[0])
            counts_art = read_excel_file(self.lineEdit.text())
            print(counts_art)
            values = [f"{item.name} - {item.art}: {item.count} шт." for item in counts_art]
            self.update_list_view(values)

    def evt_btn_create_queue(self):
        """Ивент на кнопку Сформировать очереди"""
        if self.lineEdit.text() != '':
            try:
                # Формирования словаря с глянцевой печатью и матовой
                directory = ready_path
                counts_art = read_excel_file(self.lineEdit.text())
                for item in counts_art:
                    status = search_file(filename=f"{item.art}.pdf", directory=directory)
                    if status:
                        item.status = '✅'
                art_list = []
                art_list_mat = []
                logger.info(counts_art)
                for item in counts_art:
                    if 'MAT' in [q.strip() for q in item.art.split('-')]:
                        art_list_mat.append(item)
                    else:
                        art_list.append(item)
            except Exception as ex:
                logger.debug(ex)

            try:
                # Список выбранных принтеров
                checked_checkboxes = []
                for i in range(self.verticalLayout.count()):
                    item = self.verticalLayout.itemAt(i)
                    # Получаем фактический виджет, если элемент является QLayoutItem
                    widget = item.widget()
                    # Проверяем, является ли виджет флажком (QCheckBox) и отмечен ли он
                    if isinstance(widget, QtWidgets.QCheckBox) and widget.isChecked():
                        checked_checkboxes.append(widget.text())
                if len(checked_checkboxes) == 0:
                    QMessageBox.information(self, 'Инфо', 'Не выбран ни один принтер')
                else:
                    dialog = QueueDialog(art_list, checked_checkboxes, 'Глянцевые')
                    dialog2 = QueueDialog(art_list_mat, checked_checkboxes, 'Матовые')
                    self.dialogs.append(dialog)
                    self.dialogs.append(dialog2)
                    dialog.show()
                    dialog2.show()
            except Exception as ex:
                logger.error(ex)
        else:
            QMessageBox.information(self, 'Инфо', 'Загрузите заказ')


if __name__ == '__main__':
    import sys

    logger.add(sink="logs/logs.log", level="INFO", format="{time} {level} {message}")
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
