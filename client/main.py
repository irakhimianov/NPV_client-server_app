import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem
from main_window import Ui_MainWindow
from datetime import datetime


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('NPV counter')
        self.ui.btn_close.clicked.connect(self.on_close)
        self.ui.input_year.setPlaceholderText('2050')
        self.ui.input_discount_rate.setPlaceholderText('0.2')
        self.ui.btn_count.clicked.connect(self.npv_count)


    def npv_count(self):
        input_year = int(self.ui.input_year.text())
        input_discount_rate = float(self.ui.input_discount_rate.text())
        print(f"{input_year=}\n{input_discount_rate=}")
        url = 'http://127.0.0.1:8800/npv'
        r = requests.post(url, json={'year': input_year, 'discount_rate': input_discount_rate, 'income': 1000, 'expense': 500, 'prev_NPV': 0})
        response = r.json()
        table = {'year': '',
                 'income': '',
                 'expense': '',
                 'net_cash_flow': '',
                 'NPV': ''}
        self.ui.tableWidget.setRowCount(5)
        self.ui.tableWidget.setColumnCount(len(response))
        year = str(datetime.now().year)
        for col, val in enumerate(response):
            self.ui.tableWidget.setItem(0, col, QTableWidgetItem(year))
            self.ui.tableWidget.setItem(1, col, QTableWidgetItem('1000'))
            self.ui.tableWidget.setItem(2, col, QTableWidgetItem('500'))
            self.ui.tableWidget.setItem(3, col, QTableWidgetItem(str(response[col])))
            year = str(int(year) + 1)


    def on_close(self):
        self.close()


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec_())