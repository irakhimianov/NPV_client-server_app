import sys
import requests
from requests import ConnectionError
from PyQt5.QtCore import Qt, QRegExp
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QStatusBar, QMessageBox, QLineEdit
from main_window import Ui_MainWindow
from datetime import datetime
from config import config


class MainWindow(QtWidgets.QMainWindow):
    num_only_validator = QRegExpValidator(QRegExp(r'[0-9]+'))
    float_num_validator = QRegExpValidator(QRegExp(r'(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'))
    num_with_dot_validator = QRegExpValidator(QRegExp(r'([0-9]+\.?)+'))
    xxx = ['year', 'discount_rate', 'income', 'expense', 'npv']


    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('NPV counter')
        self.setWindowIcon(QIcon('./icon'))
        self.setFixedSize(800, 370)
        self.set_table_headers()
        self.ui.input_host.setPlaceholderText('127.0.0.1')
        self.ui.input_port.setPlaceholderText('8080')
        self.ui.input_year.setPlaceholderText('2036')
        self.ui.input_discount_rate.setPlaceholderText('0.2')
        self.statusBar().showMessage('🔴 Ответ от сервера отсутсвует')
        self.ui.input_host.setText(self.get_server_info()[0])
        self.ui.input_port.setText(self.get_server_info()[1])
        self.ui.input_host.setValidator(self.num_with_dot_validator)
        self.ui.input_port.setValidator(self.num_only_validator)
        self.ui.input_year.setValidator(self.num_only_validator)
        self.ui.input_discount_rate.setValidator(self.float_num_validator)
        self.ui.btn_count.clicked.connect(self.npv_count)
        self.ui.btn_clear.clicked.connect(self.on_clear)
        self.ui.btn_close.clicked.connect(self.on_close)


    def on_cell_change(self, item):
        self.ui.tableWidget.itemChanged.disconnect()

        all_items = []
        for i_col in range(self.ui.tableWidget.columnCount()):
            row_items = {}
            for j_row in range(self.ui.tableWidget.rowCount()):
                row_items.update({self.xxx[j_row]: self.ui.tableWidget.item(j_row, i_col).text()})
            all_items.append(row_items)

        url = f'http://{self.ui.input_host.text()}:{self.ui.input_port.text()}/npv_on_change'
        if item.row() == 2:
            print(f'if {item.row()=}')
            r_json = {'col_changed': item.column(),
                      'income': float(item.text()),
                      'expense': float(all_items[item.column()]['expense'])}
        else:
            print(f'if {item.row()=}')
            r_json = {'col_changed': item.column(),
                      'income': float(all_items[item.column()]['income']),
                      'expense': float(item.text())}

        r = requests.post(url, params=r_json, json=all_items)
        response = r.json()
        print(response)
        response = r.json()

        if response:
            self.statusBar().showMessage('🟢 Ответ от сервера получен')
            self.ui.tableWidget.setColumnCount(len(response))

        for col_index, col_items in enumerate(response):
            for row_index, row_item in enumerate(col_items):
                item = QTableWidgetItem(str(col_items[row_item]))
                self.ui.tableWidget.setItem(row_index, col_index, item)
                item.setTextAlignment(Qt.AlignCenter)
                if row_index not in (2, 3):
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

        self.ui.tableWidget.itemChanged.connect(self.on_cell_change)


    def set_table_headers(self):
        self.ui.tableWidget.setRowCount(5)
        self.ui.tableWidget.setColumnCount(0)
        for row, val in enumerate(["Год", "Ставка", "Доход", "Расход", "NPV"]):
            item = QtWidgets.QTableWidgetItem(val)
            self.ui.tableWidget.setVerticalHeaderItem(row, item)


    def npv_count(self):
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

            for col_index, col_items in enumerate(response):
                for row_index, row_item in enumerate(col_items):
                    item = QTableWidgetItem(str(col_items[row_item]))
                    self.ui.tableWidget.setItem(row_index, col_index, item)
                    item.setTextAlignment(Qt.AlignCenter)
                    if row_index not in (2, 3):
                        item.setFlags(QtCore.Qt.ItemIsEnabled)

            self.ui.tableWidget.itemChanged.connect(self.on_cell_change)


        except ValueError:
            msg.setText('Ошибка ввода данных')
            msg.setInformativeText('Некорректные данные или незаполнены обязательные поля для ввода')
            msg.setWindowTitle('Ошибка')
            msg.exec_()
        except (ConnectionRefusedError, ConnectionError):
            msg.setText('Ошибка подключения к серверу')
            msg.setInformativeText('Проверьте корректность ввода данных подключения к серверу')
            msg.setWindowTitle('Ошибка')
            msg.exec_()


    def get_server_info(self) -> tuple[str]:
        return (str(config.host), str(config.port))


    def on_clear(self) -> None:
        for edit in self.findChildren(QLineEdit):
            edit.clear()
        self.ui.tableWidget.clear()
        self.set_table_headers()


    def on_close(self) -> None:
        self.close()


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec_())