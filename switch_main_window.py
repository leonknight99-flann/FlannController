import sys
import os

from configparser import ConfigParser

from qtpy import QtCore, QtWidgets, QtGui

from flann.vi.switch import Switch337


class MenuWindow(QtWidgets.QWidget):
    '''Settings window for the 024'''
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Menu")
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\FlannMicrowave.ico"))))
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setFixedSize(QtCore.QSize(200, 300))

        self.switch = None
        self.attenuator_series = 'Attenuator'
        self.parser = ConfigParser()
        self.parser.read(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\switchSettings.ini")))
        self.config = self.parser['GENERAL']

        '''User Interface'''

        self.layoutMain = QtWidgets.QVBoxLayout()

        self.layoutAddress = QtWidgets.QHBoxLayout()
        self.layoutAddress.addWidget(QtWidgets.QLabel("Address:"))
        self.addressLineEdit = QtWidgets.QLineEdit()
        self.addressLineEdit.setText(self.config['address'])
        self.layoutAddress.addWidget(self.addressLineEdit)
        self.layoutMain.addLayout(self.layoutAddress)

        self.layoutBaudRate = QtWidgets.QHBoxLayout()
        self.layoutBaudRate.addWidget(QtWidgets.QLabel("Baud Rate:"))
        self.baudRateLineEdit = QtWidgets.QLineEdit()
        self.baudRateLineEdit.setText(str(self.config['baudrate']))
        self.layoutBaudRate.addWidget(self.baudRateLineEdit)
        self.layoutMain.addLayout(self.layoutBaudRate)

        self.layoutTimeout = QtWidgets.QHBoxLayout()
        self.layoutTimeout.addWidget(QtWidgets.QLabel("Serial Timeout:"))
        self.timeoutLineEdit = QtWidgets.QLineEdit()
        self.timeoutLineEdit.setText(str(self.config['timeout']))
        self.layoutTimeout.addWidget(self.timeoutLineEdit)
        self.layoutMain.addLayout(self.layoutTimeout)

        self.layoutTcpPort = QtWidgets.QHBoxLayout()
        self.layoutTcpPort.addWidget(QtWidgets.QLabel("TCP Port:"))
        self.tcpPortLineEdit = QtWidgets.QLineEdit()
        self.tcpPortLineEdit.setText(str(self.config['tcp_port']))
        self.layoutTcpPort.addWidget(self.tcpPortLineEdit)
        self.layoutMain.addLayout(self.layoutTcpPort)

        self.layoutAppDelay = QtWidgets.QHBoxLayout()
        self.layoutAppDelay.addWidget(QtWidgets.QLabel("App Delay:"))
        self.appDelayLineEdit = QtWidgets.QLineEdit()
        self.appDelayLineEdit.setText(str(self.config['sleep']))
        self.layoutAppDelay.addWidget(self.appDelayLineEdit)
        self.layoutMain.addLayout(self.layoutAppDelay)

        self.connectButton = QtWidgets.QPushButton("Connect")
        self.connectButton.clicked.connect(lambda: self.connect_to_com_switches())
        self.layoutMain.addWidget(self.connectButton)

        self.nameLineEdit = QtWidgets.QTextEdit()
        self.nameLineEdit.setReadOnly(True)  # Read-only
        self.nameLineEdit.setFixedHeight(40)
        self.layoutMain.addWidget(self.nameLineEdit)
        
        self.disconnectButton = QtWidgets.QPushButton("Disconnect")
        self.disconnectButton.clicked.connect(lambda: self.disconnect_from_atten())
        self.layoutMain.addWidget(self.disconnectButton)

        self.positionToggle = QtWidgets.QCheckBox()
        self.positionToggle.setText("Set Position")
        self.layoutMain.addWidget(self.positionToggle)
        
        self.setLayout(self.layoutMain)

    def connect_to_com_switches(self):
        try:
            switchList = self.addressLineEdit.text().split(',')
            print(switchList)
            for switch in switchList:
                print(switch)
                if switch.lower().startswith('com'):
                    print('com')
                    self.attenuator_series = '337'
                else:
                    print('ethernet')
                    self.attenuator_series = '338'
            name = self.switch.id()
            self.nameLineEdit.setText(name)
            self.update_parser()
        except:
            print('Connection Error')

    def disconnect_from_atten(self):
        if self.switch is not None:
            self.switch.close()
            self.switch = None
            self.nameLineEdit.clear()
            self.update_parser()

    def update_parser(self):
        new_parser = ConfigParser()
        new_parser.read(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\attenuatorSettings.ini")))
        update_file = open(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\attenuatorSettings.ini")), 'w')
        new_parser['GENERAL']['port'] = str(self.addressLineEdit.text())
        new_parser['GENERAL']['baudrate'] = str(self.baudRateLineEdit.text())
        new_parser['GENERAL']['timeout'] = str(self.timeoutLineEdit.text())
        new_parser.write(update_file)
        update_file.close()


class MainWindow(QtWidgets.QMainWindow):
    '''Switch Counter Main Window'''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Switch Counter")

        self.layoutMain = QtWidgets.QVBoxLayout()

        self.mWindow = MenuWindow()
        self.config = self.mWindow.config
        self.attenuator = self.mWindow.switch

        '''User Interface'''

        # Layout 1
        self.layout1 = QtWidgets.QHBoxLayout()

        self.menuButton = QtWidgets.QPushButton("Menu")
        self.menuButton.setFixedSize(QtCore.QSize(50, 50))
        self.menuButton.clicked.connect(lambda: self.toggle_menu_window())


        '''Layout'''

        self.layout1.addWidget(self.menuButton)

        self.layoutMain.addLayout(self.layout1)

        self.widgetMain = QtWidgets.QWidget(self)
        self.widgetMain.setAutoFillBackground(True)
        self.widgetMain.setStyleSheet("background-color: rgb(132,181,141);")
        self.widgetMain.setLayout(self.layoutMain)
        self.setCentralWidget(self.widgetMain)
    
    def toggle_menu_window(self):  # Currently this limits the main window interactions due to an inheritance coding error where the self.attenuator does not update when the settings are changed in the menu window
        if self.mWindow.isVisible():
            self.mWindow.hide()
        else:
            self.mWindow.show()
        self.attenuator = self.mWindow.switch
        self.setWindowTitle(f'Flann {self.mWindow.attenuator_series}')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\FlannMicrowave.ico"))))
    window = MainWindow()
    window.show()

    app.exec()