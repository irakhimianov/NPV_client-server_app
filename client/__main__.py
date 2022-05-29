import os, sys
import requests
from datetime import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QLineEdit
from requests import ConnectionError
from src import Ui_MainWindow


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from config import config


class MainWindow(QtWidgets.QMainWindow):
    NUM_ONLY_VALIDATOR = QRegExpValidator(QRegExp(r'[0-9]+'))
    FLOAT_NUM_VALIDATOR = QRegExpValidator(QRegExp(r'(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'))
    NUM_WITH_DOT_VALIDATOR = QRegExpValidator(QRegExp(r'([0-9]+\.?)+'))
    ROW_NAMES = ['year', 'discount_rate', 'income', 'expense', 'npv']
    TABLE_HEADER_NAMES = ["Год", "Ставка", "Доход*", "Расход*", "NPV"]


    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()


    def init_ui(self) -> None:
        self.setWindowTitle('NPV counter')
        self.setWindowIcon(QIcon('src/icon'))
        self.setFixedSize(800, 370)
        self.set_table_headers()
        self.ui.tableWidget.horizontalHeader().hide()
        self.ui.input_host.setPlaceholderText('127.0.0.1')
        self.ui.input_port.setPlaceholderText('8080')
        self.ui.input_year.setPlaceholderText('2036')
        self.ui.input_discount_rate.setPlaceholderText('0.2')
        self.statusBar().showMessage('🔴 Ответ от сервера отсутсвует')
        self.ui.input_host.setText(self.get_server_info()[0])
        self.ui.input_port.setText(self.get_server_info()[1])
        self.ui.input_host.setValidator(self.NUM_WITH_DOT_VALIDATOR)
        self.ui.input_port.setValidator(self.NUM_ONLY_VALIDATOR)
        self.ui.input_year.setValidator(self.NUM_ONLY_VALIDATOR)
        self.ui.input_discount_rate.setValidator(self.FLOAT_NUM_VALIDATOR)
        self.ui.btn_count.clicked.connect(self.npv_count)
        self.ui.btn_clear.clicked.connect(self.on_clear)
        self.ui.btn_close.clicked.connect(self.on_close)


    def set_table_headers(self) -> None:
        self.ui.tableWidget.setRowCount(5)
        self.ui.tableWidget.setColumnCount(0)
        for row, val in enumerate(self.TABLE_HEADER_NAMES):
            item = QtWidgets.QTableWidgetItem(val)
            self.ui.tableWidget.setVerticalHeaderItem(row, item)


    def set_table_items(self, items: list) -> None:
        for col_index, col_items in enumerate(items):
            for row_index, row_item in enumerate(col_items):
                item = QTableWidgetItem(str(col_items[row_item]))
                self.ui.tableWidget.setItem(row_index, col_index, item)
                item.setTextAlignment(Qt.AlignCenter)
                if row_index not in (2, 3):
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.tableWidget.itemChanged.connect(self.on_cell_change)


    def npv_count(self) -> None:
        try:
            self.ui.tableWidget.itemChanged.disconnect()
        except:
            pass
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowIcon(QIcon('./icon'))
        try:
            year = str(datetime.now().year)
            input_year = int(self.ui.input_year.text())
            input_discount_rate = float(self.ui.input_discount_rate.text())
            url = f'http://{self.ui.input_host.text()}:{self.ui.input_port.text()}/npv'
            r = requests.post(url, json={'year': input_year,
                                         'discount_rate': input_discount_rate,
                                         'income': 1000,
                                         'expense': 500,
                                         'prev_NPV': 0})
            response = r.json()
            if response:
                self.statusBar().showMessage('🟢 Ответ от сервера получен')
                self.ui.tableWidget.setColumnCount(len(response))
                self.set_table_items(items=response)
        except Exception as e:
            self.on_error(e)


    def on_cell_change(self, item: QTableWidgetItem) -> None:
        self.ui.tableWidget.itemChanged.disconnect()
        all_items = []
        url = f'http://{self.ui.input_host.text()}:{self.ui.input_port.text()}/npv_on_change'
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowIcon(QIcon('./icon'))
        try:
            for i_col in range(self.ui.tableWidget.columnCount()):
                row_items = {}
                for j_row in range(self.ui.tableWidget.rowCount()):
                    row_items.update({self.ROW_NAMES[j_row]: self.ui.tableWidget.item(j_row, i_col).text()})
                all_items.append(row_items)

            if item.row() == 2:
                params = {'col_changed': item.column(),
                          'income': float(item.text()),
                          'expense': float(all_items[item.column()]['expense'])}
            else:
                params = {'col_changed': item.column(),
                          'income': float(all_items[item.column()]['income']),
                          'expense': float(item.text())}

            r = requests.post(url, params=params, json=all_items)
            response = r.json()
            if response:
                self.statusBar().showMessage('🟢 Ответ от сервера получен')
                self.ui.tableWidget.setColumnCount(len(response))
                self.set_table_items(items=response)
        except Exception as e:
            self.on_error(e)


    def get_server_info(self) -> tuple[str]:
        try:
            return (str(config.host), str(config.port))
        except:
            return ('127.0.0.1', '8080')


    def on_clear(self) -> None:
        for edit in self.findChildren(QLineEdit):
            edit.clear()
        self.ui.tableWidget.clear()
        self.set_table_headers()


    def on_close(self) -> None:
        self.close()


    def on_error(self, error: Exception) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowIcon(QIcon('src/icon'))
        msg.setWindowTitle('Ошибка')
        if isinstance(error, ValueError):
            msg.setText('Ошибка ввода данных')
            msg.setInformativeText('Некорректные данные или незаполнены обязательные поля для ввода')
        elif isinstance(error, ConnectionError):
            msg.setText('Ошибка подключения к серверу')
            msg.setInformativeText('Проверьте корректность ввода данных подключения к серверу')
            self.statusBar().showMessage('🔴 Ответ от сервера отсутсвует')
        else:
            msg.setText('Неизвестная ошибка')
            msg.setInformativeText('Попробуйте еще раз')
        msg.exec_()


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec_())
