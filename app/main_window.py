import sys
import os
import serial
import time

from configparser import ConfigParser

from qtpy import QtCore, QtWidgets, QtGui

class Color(QtWidgets.QWidget):
    def __init__(self, r,g,b):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(r,g,b))
        self.setPalette(palette)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Flann Programmable")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\FlannMicrowave.ico"))))
    window = MainWindow()
    window.show()

    app.exec()