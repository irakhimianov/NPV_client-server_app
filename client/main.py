import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem
from main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('NPV counter')
        self.ui.btn_close.clicked.connect(self.on_close)


    def on_close(self):
        self.close()


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec_())