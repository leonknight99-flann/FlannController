import sys
import os

from configparser import ConfigParser

from qtpy import QtCore, QtWidgets, QtGui

from flann.vi.switch import Switch337
from flann.vi.attenuator import Attenuator024, Attenuator625


class MenuWindow(QtWidgets.QWidget):
    '''Settings window for the 024'''
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Menu")
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\FlannMicrowave.ico"))))
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setFixedSize(QtCore.QSize(200, 300))

        self.switches = []
        self.switches_names = []
        self.parser = ConfigParser()
        self.parser.read(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\imsSwitchSettings.ini")))
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
        self.disconnectButton.clicked.connect(lambda: self.disconnect_from_switches())
        self.layoutMain.addWidget(self.disconnectButton)

        self.positionToggle = QtWidgets.QCheckBox()
        self.positionToggle.setText("Set Position")
        self.layoutMain.addWidget(self.positionToggle)
        
        self.setLayout(self.layoutMain)

    def connect_to_com_switches(self):
        try:
            switchPortList = self.addressLineEdit.text().split(',')
            print(switchPortList)
            for address in switchPortList:
                print(address)
                if address.lower().startswith('com'):
                    print('com')
                    switch = Switch337(switch=1,
                                       address=address, 
                                       timeout=float(self.timeoutLineEdit.text()), 
                                       baudrate=int(self.baudRateLineEdit.text()), 
                                       timedelay=float(self.appDelayLineEdit.text()))
                    print(switch.id())
                    self.switches.append(switch)
                    self.switches_names.append(switch.id())
                    
                else:
                    print('ethernet not supported')
            self.nameLineEdit.setText(str(self.switches_names)[1:-1])
            self.update_parser()
        except:
            print('Connection Error')

    def disconnect_from_switches(self):
        if self.switches:
            self.switches = []
            self.switches_names = []
            self.update_parser()
        self.nameLineEdit.clear()

    def update_parser(self):
        new_parser = ConfigParser()
        new_parser.read(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\imsSwitchSettings.ini")))
        update_file = open(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\imsSwitchSettings.ini")), 'w')
        new_parser['GENERAL']['port'] = str(self.addressLineEdit.text())
        new_parser['GENERAL']['baudrate'] = str(self.baudRateLineEdit.text())
        new_parser['GENERAL']['timeout'] = str(self.timeoutLineEdit.text())
        new_parser.write(update_file)
        update_file.close()


class MainWindow(QtWidgets.QMainWindow):
    '''Switch Counter Main Window'''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Switch Demo")
        self.setFixedWidth(400)

        self.mWindow = MenuWindow()
        self.config = self.mWindow.config
        self.switches = self.mWindow.switches
        self.switches_names = self.mWindow.switches_names

        self.layoutMain = QtWidgets.QVBoxLayout()

        self.disableButtonGroup = QtWidgets.QButtonGroup()

        '''User Interface'''

        # Layout 1
        self.layout1 = QtWidgets.QHBoxLayout()

        self.menuButton = QtWidgets.QPushButton("Menu", self, checkable=True)
        self.menuButton.setFixedSize(QtCore.QSize(50, 50))
        self.menuButton.setStyleSheet("QPushButton {background-color:lightgray; color:black;}")
        self.menuButton.clicked.connect(lambda: self.toggle_menu_window())
        
        self.toggleAllSwitchesButton = QtWidgets.QPushButton("Toggle All")
        self.toggleAllSwitchesButton.setFixedSize(QtCore.QSize(100, 50))
        self.toggleAllSwitchesButton.setStyleSheet("QPushButton {background-color:lightgray; color:black;}")
        self.disableButtonGroup.addButton(self.toggleAllSwitchesButton)
        self.toggleAllSwitchesButton.clicked.connect(lambda: self.toggle_all_switches())

        self.connectToAttenuatorButton = QtWidgets.QPushButton("Connect\nAttenuators")
        self.connectToAttenuatorButton.setFixedSize(QtCore.QSize(100, 50))
        self.connectToAttenuatorButton.setStyleSheet("QPushButton {background-color:rgb(0,58,34); color:lightgray;}")

        self.demoButton = QtWidgets.QPushButton("Demo", self, checkable=True)
        self.demoButton.setFixedSize(QtCore.QSize(50, 50))
        self.demoButton.setStyleSheet("QPushButton {background-color:rgb(0,58,34); color:lightgray;}")
        self.demoButton.clicked.connect(lambda: self.demo())

        ## Layout 2
        self.layout2 = QtWidgets.QGridLayout()
        self.switchButtonMap = {}

        '''Layout'''

        self.layout1.addWidget(self.menuButton)
        self.layout1.addWidget(self.toggleAllSwitchesButton)
        self.layout1.addWidget(self.connectToAttenuatorButton)
        self.layout1.addWidget(self.demoButton)

        self.layoutMain.addLayout(self.layout1)
        self.layoutMain.addLayout(self.layout2)

        self.widgetMain = QtWidgets.QWidget(self)
        self.widgetMain.setAutoFillBackground(True)
        self.widgetMain.setLayout(self.layoutMain)
        self.widgetMain.setStyleSheet("background-color: rgb(132,181,141);")
        self.setCentralWidget(self.widgetMain)
    
    def toggle_menu_window(self):  # Currently this limits the main window interactions due to an inheritance coding error where the self.attenuator does not update when the settings are changed in the menu window
        if self.mWindow.isVisible():
            self.mWindow.hide()
            self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
            self.show()
            self.switches = self.mWindow.switches
            self.switches_names = self.mWindow.switches_names

            switchButtonLabels = [['Toggle\n1', 'Toggle\n2', 'Toggle\nBoth'],] * len(self.switches)

            for s in range(len(self.switches)):
                switchLabel = QtWidgets.QTextEdit(f'{self.switches_names[s]}')
                switchLabel.setReadOnly(True)  # Read-only
                switchLabel.setStyleSheet("QTextEdit {background-color:white; color:black;}")
                switchLabel.setFixedHeight(50)
                switchLabel.setFixedWidth(100)
                switchLabel.setAlignment(QtCore.Qt.AlignCenter)
                self.layout2.addWidget(switchLabel, s, 0)

            for row, keys in enumerate(switchButtonLabels):
                for col, key in enumerate(keys):
                    self.switchButtonMap[f'{row}'+key] = QtWidgets.QPushButton(f'{key}')
                    self.switchButtonMap[f'{row}'+key].setFixedSize(QtCore.QSize(75, 50))
                    self.switchButtonMap[f'{row}'+key].setStyleSheet("QPushButton {background-color:lightgray; color:black;}")
                    if key == 'Toggle\n1':
                        self.switchButtonMap[f'{row}'+key].clicked.connect(lambda: self.toggle_selected_switch(row, 1))
                    elif key == 'Toggle\n2':
                        self.switchButtonMap[f'{row}'+key].clicked.connect(lambda: self.toggle_selected_switch(row, 2))
                    elif key == 'Toggle\nBoth':
                        self.switchButtonMap[f'{row}'+key].clicked.connect(lambda: self.switches[row].toggle_all())
                    self.layout2.addWidget(self.switchButtonMap[f'{row}'+key], row, col+1)
        else:
            self.mWindow.show()
            self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
            self.show()
            self.remove_switch_buttons()

    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()

    def toggle_selected_switch(self, switch, switch_number):
        if self.switches:
            selected_switch = self.switches[switch]
            selected_switch.switch = switch_number
            selected_switch.toggle()
        else:
            print('No switches connected.')

    def toggle_all_switches(self):
        if self.switches:
            print('Toggling all switches')
            for switch in self.switches:
                switch.toggle_all()
        else:
            print('No switches connected.')

    def remove_switch_buttons(self):
        while self.layout2.count():
            item = self.layout2.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

    def demo(self):
        if self.demoButton.isChecked():
            self.start_demo()
            self.demoButton.setText("Stop")
        else:
            self.stop_demo()
            self.demoButton.setText("Demo")

    def start_demo(self):
        print('Starting demo')

    def stop_demo(self):
        print('Stopping demo')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\FlannMicrowave.ico"))))
    window = MainWindow()
    window.show()

    app.exec()