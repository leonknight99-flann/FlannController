from ast import main
from re import M
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

class MenuWindow(QtWidgets.QWidget):
    '''Settings window for the 024'''
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Menu")
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\FlannMicrowave.ico"))))
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setFixedSize(QtCore.QSize(150, 220))

        self.serialAttenuator = None
        self.parser = ConfigParser()
        self.parser.read(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\settings.ini")))
        self.config = self.parser['GENERAL']

        '''User Interface'''

        self.layoutMain = QtWidgets.QVBoxLayout()

        self.layoutCOM = QtWidgets.QHBoxLayout()
        self.layoutCOM.addWidget(QtWidgets.QLabel("Serial Port:"))
        self.COMcomboBox = QtWidgets.QSpinBox(value=int(self.config['port']))
        self.COMcomboBox.setMinimum(1)
        self.COMcomboBox.setMaximum(99)
        self.layoutCOM.addWidget(self.COMcomboBox)
        self.layoutMain.addLayout(self.layoutCOM)

        self.layoutBaudRate = QtWidgets.QHBoxLayout()
        self.layoutBaudRate.addWidget(QtWidgets.QLabel("Baud Rate:"))
        self.baudRateLineEdit = QtWidgets.QLineEdit()
        self.baudRateLineEdit.setText(str(self.config['baudrate']))
        self.layoutBaudRate.addWidget(self.baudRateLineEdit)
        self.layoutMain.addLayout(self.layoutBaudRate)

        self.layoutTimeout = QtWidgets.QHBoxLayout()
        self.layoutTimeout.addWidget(QtWidgets.QLabel("Timeout:"))
        self.timeoutLineEdit = QtWidgets.QLineEdit()
        self.timeoutLineEdit.setText(str(self.config['timeout']))
        self.layoutTimeout.addWidget(self.timeoutLineEdit)
        self.layoutMain.addLayout(self.layoutTimeout)

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
        try:
            if self.serialAttenuator is None:
                self.serialAttenuator = serial.Serial(f'COM{self.COMcomboBox.value()}', self.baudRateLineEdit.text(), timeout=float(self.timeoutLineEdit.text()))
                self.serialAttenuator.write('CL_IDENTITY?#'.encode())
                name = self.serialAttenuator.readline().decode()
                self.nameLineEdit.setText(name)
                self.update_parser()
        except:
            print('Connection Error')

    def disconnect_from_serial(self):
        if self.serialAttenuator is not None:
            self.serialAttenuator.close()
            self.serialAttenuator = None
            self.nameLineEdit.clear()
            self.update_parser()

    def update_parser(self):
        new_parser = ConfigParser()
        new_parser.read(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\settings.ini")))
        update_file = open(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\settings.ini")), 'w')
        new_parser['GENERAL']['port'] = str(self.COMcomboBox.value())
        new_parser['GENERAL']['baudrate'] = str(self.baudRateLineEdit.text())
        new_parser['GENERAL']['timeout'] = str(self.timeoutLineEdit.text())
        new_parser.write(update_file)
        update_file.close()
        

class MainWindow(QtWidgets.QMainWindow):
    '''Main 024 control window insprired by the Flann 625'''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Flann 024")
        self.setFixedSize(QtCore.QSize(260, 300))

        self.attenuator = None
        self.mWindow = MenuWindow()
        self.config = self.mWindow.config

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
        self.attenEnterLineEdit.setText(self.read_attenuation_entry() + text)
        self.attenEnterLineEdit.setFocus()

    def read_attenuation_entry(self):
        return self.attenEnterLineEdit.text()
    
    def clear_attenuation_entry(self):
        self.attenEnterLineEdit.clear()

    def get_current_attenuation(self):
        time.sleep(float(self.config['sleep']))
        self.attenuator.write('CL_VALUE?#'.encode())
        current_val = self.attenuator.readline().split(b'\x00')[0] .decode()# removes the \x00 from the end of the string "3.0\x00"
        print(current_val)
        try:
            current_val = current_val.split(' ')[-1].strip()  # readline returns "Vane is at 20.0dB"
            print(current_val)
            current_val = current_val.rsplit('dB')[0]  # removes the dB from the end of the string "3.0dB"
            print(current_val)
            current_val = float(current_val)
            print(current_val)
        except ValueError:
            current_val = '0'
            print("Error reading current attenuation value")
        
        return current_val

    def go_to_attenuation(self):
        newAttenuation = self.read_attenuation_entry()
        print(f"New attenuation: {newAttenuation}")
        self.clear_attenuation_entry()

        if self.attenuator == None:
            self.attenReadLineEdit.setText('Connection Error')
            print("Serial port not connected")
            return
        if self.mWindow.positionToggle.isChecked():
            try:
                if len(newAttenuation) < 4:
                    zeroString = '0' * (4 - len(newAttenuation))
                    newAttenuation = zeroString + newAttenuation
                self.attenuator.write(f'CL_STEPS_SET {newAttenuation}#'.encode())
                self.attenuator.readline().decode()
                self.attenReadLineEdit.setText(f'Position {newAttenuation}')
            except:
                print("Error setting position")
                self.attenReadLineEdit.setText('Position Error')
        else:
            try:
                self.attenuator.write(f'CL_VALUE_SET {newAttenuation}#'.encode())
                self.attenuator.readline().decode()
                self.attenReadLineEdit.setText(str(self.get_current_attenuation()))
            except:
                print("Error setting attenuation")
                self.attenReadLineEdit.setText('dB Error')

    def increment_attenuation(self):
        increment = self.read_attenuation_entry()
        current_val = self.get_current_attenuation()
        print(f"Increment: {increment}")
        try:
            if float(increment) + current_val < float(self.config['max_attenuation']):
                self.attenuator.write(f'CL_INCR_SET {increment}#'.encode())
                self.attenuator.readline().decode()
                self.attenuator.write(f'CL_INCREMENT#'.encode())
                self.attenuator.readline().decode()
                self.attenReadLineEdit.setText(str(self.get_current_attenuation()))
        except:
            print("Error incrementing attenuation")
            self.attenReadLineEdit.setText('dB Error')

    def decrement_attenuation(self):
        decrement = self.read_attenuation_entry()
        current_val = self.get_current_attenuation()
        print(f"Decrement: {decrement}")
        try:
            if -float(decrement) + current_val > float(self.config['min_attenuation']):
                self.attenuator.write(f'CL_INCR_SET {decrement}#'.encode())
                self.attenuator.readline().decode()
                self.attenuator.write(f'CL_DECREMENT#'.encode())
                self.attenuator.readline().decode()
                self.attenReadLineEdit.setText(str(self.get_current_attenuation()))
        except:
            print("Error decrementing attenuation")
            self.attenReadLineEdit.setText('dB Error')
            

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\FlannMicrowave.ico"))))
    window = MainWindow()
    window.show()

    app.exec()
