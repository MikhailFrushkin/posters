from pathlib import Path

import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFileDialog, QCheckBox, QApplication, QProgressBar, QDialog, QLabel, QBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView, \
    QAbstractItemView
from loguru import logger

from config import FilesOnPrint, ready_path, stiker_path, SearchProgress
from utils.dowloads_files_yzndex import new_arts, unions_arts, dowloads_files, missing_arts
from utils.queue_files_on_printers import queue, create_file_list, queue_sticker
from utils.read_excel import read_excel_file
from utils.read_printers import enum_printers
from utils.search_file import search_file
from utils.search_stikers import dowload_srikers


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 750)
        font = QtGui.QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout_3.setSpacing(16)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setMinimumSize(QtCore.QSize(8, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.listView.setFont(font)
        self.listView.setAutoScroll(True)
        self.listView.setTabKeyNavigation(False)
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
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)
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
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_3.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 685, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Печать постеров"))
        self.label_3.setText(_translate("MainWindow", "Список артикулов:"))
        self.label_2.setText(_translate("MainWindow", "Доступные принтеры для печати:"))
        self.label.setText(_translate("MainWindow", "Выберите файл заказа:"))
        self.pushButton.setText(_translate("MainWindow", "Загрузить файл "))
        self.pushButton_3.setText(_translate("MainWindow", "Проверить базу"))
        self.pushButton_2.setText(_translate("MainWindow", "Сформировать очереди"))
        self.pushButton_4.setText(_translate("MainWindow", "Напечатать стикеры"))


# class QueueDialog(QWidget):
#     def __init__(self, files_on_print, printers, title, parent=None):
#         super().__init__(parent)
#         self.files_on_print = files_on_print
#         self.printers = printers
#         self.setWindowTitle(title)
#
#         layout = QVBoxLayout(self)
#
#         self.tableWidget = QTableWidget(self)
#         self.tableWidget.setColumnCount(4)  # Добавление колонки "Название"
#         self.tableWidget.setMinimumSize(800, 300)
#         self.tableWidget.setHorizontalHeaderLabels(
#             ["Название", "Артикул", "Количество", "Найден"])  # Обновленные заголовки
#
#         font = self.tableWidget.font()
#         font.setPointSize(14)
#         self.tableWidget.setFont(font)
#
#         self.tableWidget.setRowCount(len(self.files_on_print))
#
#         for row, file_on_print in enumerate(self.files_on_print):
#             name_item = QTableWidgetItem(file_on_print.name)  # Получение названия из датакласса
#             art_item = QTableWidgetItem(file_on_print.art)
#             count_item = QTableWidgetItem(str(file_on_print.count))
#             status_item = QTableWidgetItem(str(file_on_print.status))
#             self.tableWidget.setItem(row, 0, name_item)  # Установка элемента в колонку "Название"
#             self.tableWidget.setItem(row, 1, art_item)
#             self.tableWidget.setItem(row, 2, count_item)
#             self.tableWidget.setItem(row, 3, status_item)
#
#         layout.addWidget(self.tableWidget)
#
#         font = self.tableWidget.font()
#
#         print_button = QPushButton("Печать", self)
#         print_button.setFont(font)
#         print_button.clicked.connect(self.evt_btn_print_clicked)
#         layout.addWidget(print_button)
#
#         print_all_button = QPushButton("Печатать все", self)
#         print_all_button.setFont(font)
#         print_all_button.clicked.connect(self.evt_btn_print_all_clicked)
#         layout.addWidget(print_all_button)
#
#         # Установка режима выделения целых строк
#         self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
#
#         # Установка ширины колонки "Артикул" в 80% от ширины окна
#         header = self.tableWidget.horizontalHeader()
#         header.setSectionResizeMode(0, QHeaderView.Stretch)
#         header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
#         header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
#
#     def evt_btn_print_clicked(self):
#         selected_data = self.get_selected_data()
#         if selected_data:
#             file_tuple = create_file_list(selected_data)
#             flag = queue(self.printers, file_tuple, type_files=self.windowTitle())
#             if flag == False:
#                 QMessageBox.warning(self, 'Отправка на печать',
#                                     f"Не выбран принтер для {'Глянцевой' if self.windowTitle() == 'Глянцевые' else 'Матовой'} печати")
#             else:
#                 QMessageBox.information(self, 'Отправка на печать', "Отправлено на печать:\n{}".format(
#                     '\n'.join([f'{item.art}, {item.count} шт.' for item in selected_data])))
#         else:
#             QMessageBox.information(self, 'Отправка на печать', 'Ни одна строка не выбрана')
#
#     def evt_btn_print_all_clicked(self):
#         all_data = self.get_all_data()
#
#         if all_data:
#             file_tuple = create_file_list(all_data)
#             flag = queue(self.printers, file_tuple, type_files=self.windowTitle())
#             if flag == False:
#                 QMessageBox.warning(self, 'Отправка на печать',
#                                     f"Не выбран принтер для {'Глянцевой' if self.windowTitle() == 'Глянцевые' else 'Матовой'} печати")
#             else:
#                 QMessageBox.information(self, 'Отправка на печать', "Отправлено на печать:\n{}".format(
#                     '\n'.join([f'{item.art}, {item.count} шт.' for item in all_data])))
#         else:
#             QMessageBox.information(self, 'Отправка на печать', 'Таблица пуста')
#
#     def get_selected_data(self):
#         selected_rows = self.tableWidget.selectionModel().selectedRows()
#         data = []
#         for row in selected_rows:
#             name = self.tableWidget.item(row.row(), 0).text()
#             art = self.tableWidget.item(row.row(), 1).text()
#             count = self.tableWidget.item(row.row(), 2).text()
#             status = self.tableWidget.item(row.row(), 3).text()
#             if status == '✅':
#                 data.append(FilesOnPrint(name=name, art=art, count=int(count)))
#         return data
#
#     def get_all_data(self):
#         data = []
#         for row in range(self.tableWidget.rowCount()):
#             name = self.tableWidget.item(row, 0).text()
#             art = self.tableWidget.item(row, 1).text()
#             count = self.tableWidget.item(row, 2).text()
#             status = self.tableWidget.item(row, 3).text()
#             if status == '✅':
#                 data.append(FilesOnPrint(name=name, art=art, count=int(count)))
#         return data
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

        self.progress_label = QLabel("Прогресс:", self)
        self.progress_label.setFont(font)
        layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

    def evt_btn_print_clicked(self):
        selected_data = self.get_selected_data()
        if selected_data:
            file_tuple = create_file_list(selected_data)
            flag = queue(self.printers, file_tuple, type_files=self.windowTitle(), self=self)
            if flag == False:
                QMessageBox.warning(self, 'Отправка на печать',
                                    f"Не выбран принтер для {'Глянцевой' if self.windowTitle() == 'Глянцевые' else 'Матовой'} печати")
            else:
                QMessageBox.information(self, 'Отправка на печать', "Отправлено на печать:\n{}".format(
                    '\n'.join([f'{item.art}, {item.count} шт.' for item in selected_data])))
        else:
            QMessageBox.information(self, 'Отправка на печать', 'Ни одна строка не выбрана')

    def evt_btn_print_all_clicked(self):
        all_data = self.get_all_data()
        if all_data:
            file_tuple = create_file_list(all_data)
            flag = queue(self.printers, file_tuple, type_files=self.windowTitle(), self=self)
            if flag == False:
                QMessageBox.warning(self, 'Отправка на печать',
                                    f"Не выбран принтер для {'Глянцевой' if self.windowTitle() == 'Глянцевые' else 'Матовой'} печати")
            else:
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


class Dialog2(QDialog):
    def __init__(self, button_names, files):
        super(Dialog2, self).__init__()
        self.button_names = button_names
        self.files = files
        self.initUI()
        self.dialogs = []

    def initUI(self):
        self.setWindowTitle("Выберите принтер для печати стикеров")

        # Создаем контейнер и устанавливаем для него компоновку
        container = QWidget(self)
        layout = QVBoxLayout(container)

        for button_name in self.button_names:
            button = QPushButton(button_name, self)
            button.clicked.connect(self.buttonClicked)
            button.setStyleSheet("QPushButton { font-size: 18px; height: 50px; }")
            layout.addWidget(button)

        # Добавляем прогресс бар и надпись в контейнер
        self.progress_label = QLabel(self)
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        # Устанавливаем контейнер как главный виджет диалогового окна
        self.setLayout(layout)
        self.setFixedWidth(400)

    def buttonClicked(self):
        sender = self.sender()
        print(f"Нажата кнопка: {sender.text()}")
        try:
            file_tuple = create_file_list(orders=self.files, directory=stiker_path, self=self)
            self.progress_label.setText("Выполняется печать...")
            self.progress_bar.setValue(0)
            self.progress_bar.setMaximum(len(file_tuple))
            self.show()
            queue_sticker(printer_list=[sender.text()], file_list=file_tuple, self=self)
            self.reject()

        except Exception as ex:
            logger.error(ex)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_dir = Path.cwd()

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, 10, 100, 25)
        self.progress_bar.setMaximum(100)
        self.statusbar.addWidget(self.progress_bar, 1)

        self.pushButton.clicked.connect(self.evt_btn_open_file_clicked)
        self.pushButton_2.clicked.connect(self.evt_btn_create_queue)
        self.pushButton_3.clicked.connect(self.evt_btn_update_db)
        self.pushButton_4.clicked.connect(self.evt_btn_print_stikers)

        try:
            printers_list = enum_printers()
            for printer in printers_list:
                self.addPrinterCheckbox(printer)
                self.addPrinterCheckbox(printer, is_matte=True)

        except Exception as ex:
            logger.debug(ex)

        self.dialogs = []

    def update_progress(self, current_value, total_value):
        progress = int(current_value / total_value * 100)
        self.progress_bar.setValue(progress)
        QApplication.processEvents()

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
        res, _ = QFileDialog.getOpenFileName(self, 'Загрузить файл', str(self.current_dir), 'Лист XLSX (*.xlsx)')
        if res:
            try:
                self.lineEdit.setText(res)
                counts_art = read_excel_file(self.lineEdit.text())
                values = [f"{item.name} - {item.art}: {item.count} шт." for item in counts_art]
                self.update_list_view(values)
            except Exception as ex:
                logger.error(f'ошибка чтения xlsx {ex}')
                QMessageBox.information(self, 'Инфо', f'ошибка чтения xlsx {ex}')

    def evt_btn_create_queue(self):
        """Ивент на кнопку Сформировать очереди"""
        if self.lineEdit.text():
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
                if not checked_checkboxes:
                    QMessageBox.information(self, 'Инфо', 'Не выбран ни один принтер')
                else:
                    try:
                        if len(art_list) > 0:
                            dialog = QueueDialog(art_list, checked_checkboxes, 'Глянцевые')
                            self.dialogs.append(dialog)
                            dialog.show()
                        if len(art_list_mat) > 0:
                            dialog2 = QueueDialog(art_list_mat, checked_checkboxes, 'Матовые')
                            self.dialogs.append(dialog2)
                            dialog2.show()
                    except Exception as ex:
                        logger.error(f'Ошибка формирования списков печати (мат, глянец) {ex}')
            except Exception as ex:
                logger.error(ex)
        else:
            QMessageBox.information(self, 'Инфо', 'Загрузите заказ')

    def evt_btn_update_db(self):
        """Ивент на кнопку проверить базу"""

        def on_yes_clicked():
            print("Нажата кнопка 'Да'")
            dialog.reject()

            list_new_atrs = new_arts('Пути к артикулам.xlsx', self)
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Загрузка')
            msg_box.setText('Найдены новые артикула: \n{}'.format('\n'.join(list_new_atrs)))
            font = QFont()
            font.setPointSize(14)
            msg_box.setFont(font)
            if len(list_new_atrs) != 0:
                download_button = QPushButton('Скачать')
                skip_button = QPushButton('Пропустить')

                button_font = download_button.font()
                button_font.setPointSize(button_font.pointSize() + 8)
                download_button.setFont(button_font)
                skip_button.setFont(button_font)

                # Добавляем кнопки в QMessageBox
                msg_box.addButton(download_button, QMessageBox.AcceptRole)
                msg_box.addButton(skip_button, QMessageBox.RejectRole)

                # Отображаем QMessageBox и получаем результат
                result = msg_box.exec_()

                # Обработка результата
                if result == QMessageBox.AcceptRole:
                    if len(list_new_atrs) != 0:
                        logger.info(f'Нажата кнопка скачать. Список файлов: {list_new_atrs}')
                        self.progress_bar.setValue(90)
                        dowloads_files(df_new='Пути к артикулам.xlsx', self=self)
                        QMessageBox.information(self, 'Инфо', 'Все файлы скачены')
                        unions_arts(self, new_arts=list_new_atrs)
                        QMessageBox.information(self, 'Инфо', 'Файлы соединены')

                elif result == QMessageBox.RejectRole:
                    logger.info(f'Нажата кнопка Пропустить. Список файлов: {list_new_atrs}')
            else:
                QMessageBox.information(self, 'Инфо', 'Не найдено новых артикулов')

        def on_no_clicked():
            print("Нажата кнопка 'Нет'")
            dialog.reject()

        def on_skip_clicked():
            print("Нажата кнопка 'Пропустить сканирование Я.диска'")
            dialog.reject()

            list_new_atrs = missing_arts('Пути к артикулам.xlsx')
            dowloads_files(df_new='Пути к артикулам.xlsx', self=self)
            self.progress_bar.setValue(100)
            QMessageBox.information(self, 'Инфо', 'Все файлы скачены')
            unions_arts(self, new_arts=list_new_atrs)
            QMessageBox.information(self, 'Инфо', 'Файлы соединены')
            self.progress_bar.setValue(100)

        def dowloads_stikers():
            print("Нажата кнопка 'Скачать стикеры'")
            dialog.reject()
            dowload_srikers(self)

        dialog = QDialog()
        dialog.setWindowTitle('Загрузка')

        main_layout = QVBoxLayout(dialog)

        label_layout = QVBoxLayout()
        label = QLabel('Продолжить?', dialog)
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        label_layout.addWidget(label)

        button_layout = QHBoxLayout()
        button_layout2 = QVBoxLayout()

        yes_button = QPushButton('Да', dialog)
        yes_button.setFixedSize(yes_button.sizeHint().width() * 2, yes_button.sizeHint().height() * 2)
        yes_button.clicked.connect(on_yes_clicked)
        button_layout.addWidget(yes_button)

        no_button = QPushButton('Нет', dialog)
        no_button.setFixedSize(no_button.sizeHint().width() * 2, no_button.sizeHint().height() * 2)
        no_button.clicked.connect(on_no_clicked)
        button_layout.addWidget(no_button)

        stiker_button = QPushButton('Скачать стикеры', dialog)
        stiker_button.setFixedSize(stiker_button.sizeHint().width() * 2, stiker_button.sizeHint().height() * 2)
        stiker_button.clicked.connect(dowloads_stikers)
        button_layout2.addWidget(stiker_button)

        skip_button = QPushButton('Пропустить сканирования Я.диска', dialog)
        skip_button.setFixedSize(skip_button.sizeHint().width() * 2, skip_button.sizeHint().height() * 2)
        skip_button.clicked.connect(on_skip_clicked)
        button_layout2.addWidget(skip_button)

        button_layout.addStretch()
        button_layout2.addStretch()

        main_layout.addLayout(label_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(button_layout2)

        dialog.exec_()

    def evt_btn_print_stikers(self):
        """Ивент на кнопку напечатать стикеры"""
        logger.info(self.lineEdit.text())
        if self.lineEdit.text() != '':
            directory = stiker_path
            counts_art = read_excel_file(self.lineEdit.text())
            for item in counts_art:
                status = search_file(filename=f"{item.art}.pdf", directory=directory)
                if status:
                    item.status = '✅'
            logger.debug(counts_art)
            button_names = enum_printers('стикеры')
            dialog = Dialog2(button_names=button_names, files=counts_art)
            dialog.exec_()
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
