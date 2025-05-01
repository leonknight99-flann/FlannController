import sys
import os

from configparser import ConfigParser

from qtpy import QtCore, QtWidgets, QtGui

class MainWindow(QtWidgets.QMainWindow):
    '''Switch Counter Main Window'''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Switch Counter")

        self.layoutMain = QtWidgets.QVBoxLayout()

        self.disableButtonGroup = QtWidgets.QButtonGroup()

        self.parser = ConfigParser()
        self.parser.read(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\switchCount.ini")))
        self.config = self.parser['GENERAL']
        self.counter = self.parser['COUNTER']['count']

        '''User Interface'''

        # Layout 1

        self.layout1 = QtWidgets.QHBoxLayout()

        self.connectButton = QtWidgets.QPushButton("Connect")
        self.connectButton.setFixedSize(QtCore.QSize(100, 50))
        self.connectButton.setStyleSheet("color: white; background-color: lightgray")
        self.connectButton.clicked.connect(lambda: self.connect_switch())

        self.startButton = QtWidgets.QPushButton("Start")
        self.startButton.setFixedSize(QtCore.QSize(100, 50))
        self.startButton.setStyleSheet("color: white; background-color: rgb(132,181,141)")
        self.startButton.clicked.connect(lambda: self.inc_counter())
        self.startButton.setEnabled(False)
        self.disableButtonGroup.addButton(self.startButton)

        self.stopButton = QtWidgets.QPushButton("Stop")
        self.stopButton.setFixedSize(QtCore.QSize(100, 50))
        self.stopButton.setStyleSheet("color: white; background-color: rgb(132,181,141)")
        self.stopButton.clicked.connect(lambda: self.inc_counter())
        self.stopButton.setEnabled(False)
        self.disableButtonGroup.addButton(self.stopButton)

        self.disconnectButton = QtWidgets.QPushButton("Disconnect")
        self.disconnectButton.setFixedSize(QtCore.QSize(100, 50))
        self.disconnectButton.setStyleSheet("color: white; background-color: lightgray")
        self.disconnectButton.clicked.connect(lambda: self.disconnect_switch())
        
        # LCD Display Layout

        self.lcdDisplay = QtWidgets.QLCDNumber(self.centralWidget())
        self.lcdDisplay.setDigitCount(len(str(self.counter)))
        self.lcdDisplay.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdDisplay.setStyleSheet("color: white; font-size: 50px; border: 0px;")
        self.lcdDisplay.display(int(self.counter))

        '''Layout'''
        self.layout1.addWidget(self.connectButton)
        self.layout1.addWidget(self.startButton)
        self.layout1.addWidget(self.stopButton)
        self.layout1.addWidget(self.disconnectButton)

        self.layoutMain.addLayout(self.layout1)
        self.layoutMain.addWidget(self.lcdDisplay)

        self.widgetMain = QtWidgets.QWidget(self)
        self.widgetMain.setAutoFillBackground(True)
        self.widgetMain.setStyleSheet("background-color: rgb(0,122,78);")
        self.widgetMain.setLayout(self.layoutMain)
        self.setCentralWidget(self.widgetMain)

    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()

    def connect_switch(self):
        for button in self.disableButtonGroup.buttons():
            button.setEnabled(True)

    def disconnect_switch(self):
        for button in self.disableButtonGroup.buttons():
            button.setEnabled(False)

    def inc_counter(self):
        self.counter = int(self.counter) + 1
        self.update_parser()
        print(self.counter)
        self.lcdDisplay.setDigitCount(len(str(self.counter)))  # Auto expand the display size
        self.lcdDisplay.display(int(self.counter))

    def update_parser(self):
        new_parser = ConfigParser()
        new_parser.read(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\switchCount.ini")))
        update_file = open(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\switchCount.ini")), 'w')
        new_parser['COUNTER']['count'] = str(self.counter)
        new_parser.write(update_file)
        update_file.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\FlannMicrowave.ico"))))
    window = MainWindow()
    window.show()

    app.exec()
