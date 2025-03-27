import sys
from tkinter import N

from qtpy import QtCore, QtWidgets, QtGui

class Color(QtWidgets.QWidget):
    def __init__(self, r,g,b):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(r,g,b))
        self.setPalette(palette)

class MenuWindow(QtWidgets.QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu")
        self.setWindowIcon(QtGui.QIcon("FlannMicrowave.ico"))

        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("feature not implemented yet")
        layout.addWidget(self.label)
        self.setLayout(layout)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Flann 024")
        self.setWindowIcon(QtGui.QIcon("FlannMicrowave.ico"))
        self.setFixedSize(QtCore.QSize(260, 300))
        # self.setFixedSize()

        self.mWindow = None

        self.layoutMain = QtWidgets.QVBoxLayout()

        '''User Interface'''

        # Layout 1
        self.layout1 = QtWidgets.QHBoxLayout()

        self.menuButton = QtWidgets.QPushButton("Menu")
        self.menuButton.setFixedSize(QtCore.QSize(50, 50))
        self.menuButton.clicked.connect(self.show_menu_window)

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
        self.incrementButton.setFixedHeight(76)
        self.layout2b.addWidget(self.incrementButton)
        self.decrementButton = QtWidgets.QPushButton("Dec -")
        self.decrementButton.clicked.connect(lambda: self.decrement_attenuation())
        self.decrementButton.setFixedHeight(76)
        self.layout2b.addWidget(self.decrementButton)
        self.enterButton = QtWidgets.QPushButton("Goto")
        self.enterButton.clicked.connect(lambda: self.go_to_attenuation())
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


    def show_menu_window(self):  # Currently casues a click twice to open bug
        if self.mWindow is None:
            self.mWindow = MenuWindow()
            self.mWindow.show()
        else:
            self.mWindow.close()
            self.mWindow = None

    def append_attenuation_entry(self, text):
        self.attenEnterLineEdit.setText(self.attenEnterLineEdit.text() + text)
        self.attenEnterLineEdit.setFocus()

    def read_attenuation_entry(self):
        return self.attenEnterLineEdit.text()
    
    def clear_attenuation_entry(self):
        self.attenEnterLineEdit.clear()

    def go_to_attenuation(self):
        newAttenuation = self.read_attenuation_entry()
        self.clear_attenuation_entry()
        self.attenReadLineEdit.setText('Goto')
        pass  # Placeholder for future implementation

    def increment_attenuation(self):
        self.attenReadLineEdit.setText('Inc +')
        pass  # placeholder for future implementation

    def decrement_attenuation(self):
        self.attenReadLineEdit.setText('Dec -')
        pass  # placeholder for future implementation
            

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()

if __name__ == '__main__':
    main()