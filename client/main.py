import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QStatusBar
from main_window import Ui_MainWindow
from datetime import datetime
from settings import settings


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
        self.statusBar().showMessage('🔴 Ответ от сервера отсутсвует')
        self.ui.input_ip.setText(self.get_server_info()[0])
        self.ui.input_port.setText(self.get_server_info()[1])


    def npv_count(self):
        input_year = int(self.ui.input_year.text())
        input_discount_rate = float(self.ui.input_discount_rate.text())
        print(f"{input_year=}\n{input_discount_rate=}")
        url = f'http://{self.ui.input_ip.text()}:{self.ui.input_port.text()}/npv'
        r = requests.post(url, json={'year': input_year, 'discount_rate': input_discount_rate, 'income': 1000, 'expense': 500, 'prev_NPV': 0})
        response = r.json()
        if response:
            self.statusBar().showMessage('🟢 Ответ от сервера получен')
        # self.ui.tableWidget.setRowCount(4)
        self.ui.tableWidget.setColumnCount(len(response))
        year = str(datetime.now().year)
        for col, val in enumerate(response):
            self.ui.tableWidget.setItem(0, col, QTableWidgetItem(year))
            self.ui.tableWidget.setItem(1, col, QTableWidgetItem('1000'))
            self.ui.tableWidget.setItem(2, col, QTableWidgetItem('500'))
            self.ui.tableWidget.setItem(3, col, QTableWidgetItem(str(response[col])))
            year = str(int(year) + 1)


    def get_server_info(self) -> tuple[str]:
        return (str(settings.host), str(settings.port))


    def on_close(self):
        self.close()


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec_())