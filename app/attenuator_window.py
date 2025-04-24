import time

from qtpy.QtCore import (QByteArray, QFile, QFileInfo, QSettings,
                            QSaveFile, QTextStream, Qt, Slot, QSize)

from qtpy.QtGui import QAction, QIcon, QKeySequence, QPalette, QColor

from qtpy.QtWidgets import (QApplication, QFileDialog, QMdiSubWindow,
                               QMdiArea, QMessageBox, QTextEdit, QWidget,
                               QVBoxLayout, QHBoxLayout, QGridLayout,
                               QPushButton, QLineEdit, QLabel, QButtonGroup)

class Color(QWidget):
    def __init__(self, r,g,b):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(r,g,b))
        self.setPalette(palette)

class AttenuatorWindow(QMdiSubWindow):
    '''Main 024 control window insprired by the Flann 625'''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Flann 024")
        self.setFixedSize(QSize(260, 300))

        self.attenuator = None
        # self.mWindow = MenuWindow() 
        # self.config = self.mWindow.config

        self.layoutMain = QVBoxLayout()

        self.disableButtonGroup = QButtonGroup()

        '''User Interface'''

        # Layout 1
        self.layout1 = QHBoxLayout()

        self.menuButton = QPushButton("Menu")
        self.menuButton.setFixedSize(QSize(50, 50))
        # self.menuButton.clicked.connect(lambda: self.toggle_menu_window())

        # Layout 1a
        self.layout1a = QGridLayout()

        self.layout1a.addWidget(QLabel("Actual:"), 0,0)
        self.attenReadLineEdit = QLineEdit()
        self.attenReadLineEdit.setReadOnly(True)    # Read-only
        self.attenReadLineEdit.setFixedWidth(120)
        self.attenReadLineEdit.setStyleSheet("background-color: white")
        self.layout1a.addWidget(self.attenReadLineEdit, 0,1)
        self.layout1a.addWidget(QLabel("dB"), 0,2)

        self.layout1a.addWidget(QLabel("Entry:"), 1,0)
        self.attenEnterLineEdit = QLineEdit()
        self.attenEnterLineEdit.returnPressed.connect(lambda: self.go_to_attenuation())
        self.attenEnterLineEdit.setFixedWidth(120)
        self.attenEnterLineEdit.setStyleSheet("background-color: white")
        self.layout1a.addWidget(self.attenEnterLineEdit, 1,1)
        self.layout1a.addWidget(QLabel("dB"), 1,2)
        
        # Layout 2
        self.layout2 = QHBoxLayout()
        
        # Layout 2a
        self.layout2a = QGridLayout()
        self.keyboardButtonMap = {}
        keyboard = [['7', '8', '9'],
                    ['4', '5', '6'],
                    ['1', '2', '3'],
                    ['C', '0', '.']]
        for row, keys in enumerate(keyboard):
            for col, key in enumerate(keys):
                self.keyboardButtonMap[key] = QPushButton(key)
                self.keyboardButtonMap[key].setFixedSize(QSize(50, 50))
                self.keyboardButtonMap[key].setStyleSheet("background-color: lightgray")
                if key == 'C':
                    self.keyboardButtonMap[key].clicked.connect(self.clear_attenuation_entry)
                else:
                    self.keyboardButtonMap[key].clicked.connect(lambda _, key=key: self.append_attenuation_entry(key))
                self.layout2a.addWidget(self.keyboardButtonMap[key], row, col)

        # Layout 2b
        self.layout2b = QVBoxLayout()

        self.incrementButton = QPushButton("Inc +")
        self.incrementButton.clicked.connect(lambda: self.increment_attenuation())
        self.disableButtonGroup.addButton(self.incrementButton)
        self.incrementButton.setFixedHeight(76)
        self.layout2b.addWidget(self.incrementButton)
        self.decrementButton = QPushButton("Dec -")
        self.decrementButton.clicked.connect(lambda: self.decrement_attenuation())
        self.disableButtonGroup.addButton(self.decrementButton)
        self.decrementButton.setFixedHeight(76)
        self.layout2b.addWidget(self.decrementButton)
        self.enterButton = QPushButton("Goto")
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
        self.setLayout(self.widgetMain)

    # def toggle_menu_window(self):  # Currently this limits the main window interactions due to an inheritance coding error where the self.attenuator does not update when the settings are changed in the menu window
    #     if self.mWindow.isVisible():
    #         self.mWindow.hide()
    #         for button in self.disableButtonGroup.buttons():
    #             button.setEnabled(True)
    #         self.attenEnterLineEdit.setReadOnly(False)
    #     else:
    #         self.mWindow.show()
    #         for button in self.disableButtonGroup.buttons():
    #             button.setEnabled(False)
    #         self.attenEnterLineEdit.setReadOnly(True)
    #     self.attenuator = self.mWindow.serialAttenuator

    def closeEvent(self, event):
        QApplication.closeAllWindows()

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

    def go_to_attenuation(self, positionToggle=False):
        newAttenuation = self.read_attenuation_entry()
        print(f"New attenuation: {newAttenuation}")
        self.clear_attenuation_entry()

        if self.attenuator == None:
            self.attenReadLineEdit.setText('Connection Error')
            print("Serial port not connected")
            return
        if positionToggle:
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