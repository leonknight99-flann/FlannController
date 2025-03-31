from ast import main
from re import M
import sys
import os
import serial

from configparser import ConfigParser

from qtpy import QtCore, QtWidgets, QtGui

class Color(QtWidgets.QWidget):
    def __init__(self, r,g,b):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(r,g,b))
        self.setPalette(palette)

class MenuWindow(QtWidgets.QWidget):
    '''Settings window for the 024'''
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Menu")
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\FlannMicrowave.ico"))))
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setFixedSize(QtCore.QSize(150, 200))

        self.serialAttenuator = None

        self.layoutMain = QtWidgets.QVBoxLayout()

        self.layoutCOM = QtWidgets.QHBoxLayout()
        self.layoutCOM.addWidget(QtWidgets.QLabel("Serial Port:"))
        self.COMcomboBox = QtWidgets.QSpinBox(value=3)
        self.COMcomboBox.setMinimum(1)
        self.COMcomboBox.setMaximum(99)
        self.layoutCOM.addWidget(self.COMcomboBox)
        self.layoutMain.addLayout(self.layoutCOM)

        self.layoutBaudRate = QtWidgets.QHBoxLayout()
        self.layoutBaudRate.addWidget(QtWidgets.QLabel("Baud Rate:"))
        self.baudRateLineEdit = QtWidgets.QLineEdit()
        self.baudRateLineEdit.setText("31250")
        self.layoutBaudRate.addWidget(self.baudRateLineEdit)
        self.layoutMain.addLayout(self.layoutBaudRate)

        self.connectButton = QtWidgets.QPushButton("Connect")
        self.connectButton.clicked.connect(lambda: self.connect_to_serial())
        self.layoutMain.addWidget(self.connectButton)

        self.nameLineEdit = QtWidgets.QLineEdit()
        self.nameLineEdit.setReadOnly(True)    # Read-only
        self.layoutMain.addWidget(self.nameLineEdit)
        
        self.disconnectButton = QtWidgets.QPushButton("Disconnect")
        self.disconnectButton.clicked.connect(lambda: self.disconnect_from_serial())
        self.layoutMain.addWidget(self.disconnectButton)

        self.positionToggle = QtWidgets.QCheckBox()
        self.positionToggle.setText("Set Position")
        self.layoutMain.addWidget(self.positionToggle)
        
        self.setLayout(self.layoutMain)

    def connect_to_serial(self):
        if self.serialAttenuator is None:
            self.serialAttenuator = serial.Serial(f'COM{self.COMcomboBox.value()}', self.baudRateLineEdit.text(), timeout=2)
            print(self.serialAttenuator.name)
            self.serialAttenuator.write('CL_IDENTITY?#'.encode())
            name = self.serialAttenuator.readline().decode()
            self.nameLineEdit.setText(name)
            print(name)

    def disconnect_from_serial(self):
        if self.serialAttenuator is not None:
            self.serialAttenuator.close()
            self.serialAttenuator = None
            self.nameLineEdit.clear()
            print("Disconnected from serial port")
        

class MainWindow(QtWidgets.QMainWindow):
    '''Main 024 control window insprired by the Flann 625'''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Flann 024")
        self.setFixedSize(QtCore.QSize(260, 300))

        self.attenuator = None
        self.mWindow = MenuWindow()

        self.layoutMain = QtWidgets.QVBoxLayout()

        self.disableButtonGroup = QtWidgets.QButtonGroup()

        '''User Interface'''

        # Layout 1
        self.layout1 = QtWidgets.QHBoxLayout()

        self.menuButton = QtWidgets.QPushButton("Menu")
        self.menuButton.setFixedSize(QtCore.QSize(50, 50))
        self.menuButton.clicked.connect(lambda: self.toggle_menu_window())

        # Layout 1a
        self.layout1a = QtWidgets.QGridLayout()

        self.layout1a.addWidget(QtWidgets.QLabel("Actual:"), 0,0)
        self.attenReadLineEdit = QtWidgets.QLineEdit()
        self.attenReadLineEdit.setReadOnly(True)    # Read-only
        self.attenReadLineEdit.setFixedWidth(120)
        self.attenReadLineEdit.setStyleSheet("background-color: white")
        self.layout1a.addWidget(self.attenReadLineEdit, 0,1)
        self.layout1a.addWidget(QtWidgets.QLabel("dB"), 0,2)

        self.layout1a.addWidget(QtWidgets.QLabel("Entry:"), 1,0)
        self.attenEnterLineEdit = QtWidgets.QLineEdit()
        self.attenEnterLineEdit.returnPressed.connect(lambda: self.go_to_attenuation())
        self.attenEnterLineEdit.setFixedWidth(120)
        self.attenEnterLineEdit.setStyleSheet("background-color: white")
        self.layout1a.addWidget(self.attenEnterLineEdit, 1,1)
        self.layout1a.addWidget(QtWidgets.QLabel("dB"), 1,2)
        
        # Layout 2
        self.layout2 = QtWidgets.QHBoxLayout()
        
        # Layout 2a
        self.layout2a = QtWidgets.QGridLayout()
        self.keyboardButtonMap = {}
        keyboard = [['7', '8', '9'],
                    ['4', '5', '6'],
                    ['1', '2', '3'],
                    ['C', '0', '.']]
        for row, keys in enumerate(keyboard):
            for col, key in enumerate(keys):
                self.keyboardButtonMap[key] = QtWidgets.QPushButton(key)
                self.keyboardButtonMap[key].setFixedSize(QtCore.QSize(50, 50))
                self.keyboardButtonMap[key].setStyleSheet("background-color: lightgray")
                if key == 'C':
                    self.keyboardButtonMap[key].clicked.connect(self.clear_attenuation_entry)
                else:
                    self.keyboardButtonMap[key].clicked.connect(lambda _, key=key: self.append_attenuation_entry(key))
                self.layout2a.addWidget(self.keyboardButtonMap[key], row, col)

        # Layout 2b
        self.layout2b = QtWidgets.QVBoxLayout()

        self.incrementButton = QtWidgets.QPushButton("Inc +")
        self.incrementButton.clicked.connect(lambda: self.increment_attenuation())
        self.disableButtonGroup.addButton(self.incrementButton)
        self.incrementButton.setFixedHeight(76)
        self.layout2b.addWidget(self.incrementButton)
        self.decrementButton = QtWidgets.QPushButton("Dec -")
        self.decrementButton.clicked.connect(lambda: self.decrement_attenuation())
        self.disableButtonGroup.addButton(self.decrementButton)
        self.decrementButton.setFixedHeight(76)
        self.layout2b.addWidget(self.decrementButton)
        self.enterButton = QtWidgets.QPushButton("Goto")
        self.enterButton.clicked.connect(lambda: self.go_to_attenuation())
        self.disableButtonGroup.addButton(self.enterButton)
        self.enterButton.setFixedHeight(50)
        self.layout2b.addWidget(self.enterButton)

        '''Layout'''

        self.layout1.addWidget(self.menuButton)
        self.layout1.addLayout(self.layout1a)

        self.layout2.addLayout(self.layout2a)
        self.layout2.addLayout(self.layout2b)   

        self.layoutMain.addLayout(self.layout1)
        self.layoutMain.addLayout(self.layout2) 

        self.widgetMain = Color(132,181,141)
        self.widgetMain.setLayout(self.layoutMain)
        self.setCentralWidget(self.widgetMain)

    def toggle_menu_window(self):  # Currently this limits the main window interactions due to an inheritance coding error where the self.attenuator does not update when the settings are changed in the menu window
        if self.mWindow.isVisible():
            self.mWindow.hide()
            for button in self.disableButtonGroup.buttons():
                button.setEnabled(True)
            self.attenEnterLineEdit.setReadOnly(False)
        else:
            self.mWindow.show()
            for button in self.disableButtonGroup.buttons():
                button.setEnabled(False)
            self.attenEnterLineEdit.setReadOnly(True)
        self.attenuator = self.mWindow.serialAttenuator

    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()

    def append_attenuation_entry(self, text):
        self.attenEnterLineEdit.setText(self.attenEnterLineEdit.text() + text)
        self.attenEnterLineEdit.setFocus()

    def read_attenuation_entry(self):
        return self.attenEnterLineEdit.text()
    
    def clear_attenuation_entry(self):
        self.attenEnterLineEdit.clear()

    def go_to_attenuation(self):
        newAttenuation = self.read_attenuation_entry()
        print(f"New attenuation: {newAttenuation}")

        if self.attenuator == None:
            self.attenReadLineEdit.setText('Connection Error')
            print("Serial port not connected")
            return
        if self.mWindow.positionToggle.isChecked():
            if len(newAttenuation) < 4:
                zeroString = '0' * (4 - len(newAttenuation))
                newAttenuation = zeroString + newAttenuation
            self.attenuator.write(f'CL_STEPS_SET {newAttenuation}#'.encode())
            self.clear_attenuation_entry()
            self.attenReadLineEdit.setText(f'Position {newAttenuation}')
        else:
            self.attenuator.write(f'CL_VALUE_SET {newAttenuation}#'.encode())
            self.clear_attenuation_entry()
            self.attenuator.write('CL_VALUE?#'.encode())
            self.attenReadLineEdit.setText(self.attenuator.readline().decode())

    def increment_attenuation(self):
        self.attenReadLineEdit.setText('Inc +')
        pass  # placeholder for future implementation

    def decrement_attenuation(self):
        self.attenReadLineEdit.setText('Dec -')
        pass  # placeholder for future implementation
            

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\FlannMicrowave.ico"))))
    window = MainWindow()
    window.show()

    app.exec()
