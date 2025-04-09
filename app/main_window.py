import sys
import os
import serial
import time

from configparser import ConfigParser

from qtpy.QtCore import (QByteArray, QFile, QFileInfo, QSettings,
                            QSaveFile, QTextStream, Qt, Slot)

from qtpy.QtGui import QAction, QIcon, QKeySequence, QPalette, QColor

from qtpy.QtWidgets import (QApplication, QFileDialog, QMainWindow,
                               QMdiArea, QMessageBox, QTextEdit, QWidget)

class Color(QWidget):
    def __init__(self, r,g,b):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(r,g,b))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Flann Programmable")

        self._mdi_area = QMdiArea()
        self._mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setCentralWidget(self._mdi_area)

        self.create_actions()
        self.create_menus()
        # self.update_menus()


    def closeEvent(self, event):
        self._mdi_area.closeAllSubWindows()
        if self._mdi_area.currentSubWindow():
            event.ignore()
        else:
            self.write_settings()
            event.accept()

    def create_status_bar(self):
        self.statusBar().showMessage("Ready")

    def create_actions(self):

        icon = QIcon.fromTheme(QIcon.ThemeIcon.WindowNew)
        self.new_attenuator = QAction(icon, "&New Attenuator", self, shortcut=QKeySequence.StandardKey.New,
                                statusTip="Open a new attenuator window")

        icon = QIcon.fromTheme(QIcon.ThemeIcon.WindowNew)
        self.new_switch = QAction(icon, "&New Switch", self, shortcut=QKeySequence.StandardKey.Open,
                                 statusTip="Open a new switch window")

        icon = QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave)
        self._save_act = QAction(icon, "&Save", self,
                                 shortcut=QKeySequence.StandardKey.Save,
                                 statusTip="Save the document to disk")

        self._save_as_act = QAction("Save &As...", self,
                                    shortcut=QKeySequence.StandardKey.SaveAs,
                                    statusTip="Save the document under a new name")

        icon = QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit)
        self.exit = QAction(icon, "E&xit", self, shortcut=QKeySequence.StandardKey.Quit,
                                 statusTip="Exit the application",
                                 triggered=QApplication.instance().closeAllWindows)

        icon = QIcon.fromTheme(QIcon.ThemeIcon.EditCut)
        self._cut_act = QAction(icon, "Cu&t", self,
                                shortcut=QKeySequence.StandardKey.Cut,
                                statusTip="Cut the current selection's contents to the clipboard")

        icon = QIcon.fromTheme(QIcon.ThemeIcon.EditCopy)
        self._copy_act = QAction(icon, "&Copy", self,
                                 shortcut=QKeySequence.StandardKey.Copy,
                                 statusTip="Copy the current selection's contents to the clipboard")

        icon = QIcon.fromTheme(QIcon.ThemeIcon.EditPaste)
        self._paste_act = QAction(icon, "&Paste", self,
                                  shortcut=QKeySequence.StandardKey.Paste,
                                  statusTip="Paste the clipboard's contents into the current "
                                            "selection")

        self._close_act = QAction("Cl&ose", self,
                                  statusTip="Close the active window",
                                  triggered=self._mdi_area.closeActiveSubWindow)

        self._close_all_act = QAction("Close &All", self,
                                      statusTip="Close all the windows",
                                      triggered=self._mdi_area.closeAllSubWindows)

        self._tile_act = QAction("&Tile", self, statusTip="Tile the windows",
                                 triggered=self._mdi_area.tileSubWindows)

        self._cascade_act = QAction("&Cascade", self,
                                    statusTip="Cascade the windows",
                                    triggered=self._mdi_area.cascadeSubWindows)

        self._next_act = QAction("Ne&xt", self, shortcut=QKeySequence.StandardKey.NextChild,
                                 statusTip="Move the focus to the next window",
                                 triggered=self._mdi_area.activateNextSubWindow)

        self._previous_act = QAction("Pre&vious", self,
                                     shortcut=QKeySequence.StandardKey.PreviousChild,
                                     statusTip="Move the focus to the previous window",
                                     triggered=self._mdi_area.activatePreviousSubWindow)

        self._separator_act = QAction(self)
        self._separator_act.setSeparator(True)

        icon = QIcon.fromTheme(QIcon.ThemeIcon.HelpAbout)
        self._about_act = QAction(icon, "&About", self,
                                  statusTip="Show the application's About box")

        self._about_qt_act = QAction("About &Qt", self,
                                     statusTip="Show the Qt library's About box")

    def create_menus(self):
        self._file_menu = self.menuBar().addMenu("&File")
        self._file_menu.addAction(self.new_attenuator)
        self._file_menu.addAction(self.new_switch)
        self._file_menu.addSeparator()
        self._file_menu.addAction(self.exit)

        self._edit_menu = self.menuBar().addMenu("&Edit")
        self._edit_menu.addAction(self._cut_act)
        self._edit_menu.addAction(self._copy_act)
        self._edit_menu.addAction(self._paste_act)

        self._window_menu = self.menuBar().addMenu("&Window")

        self.menuBar().addSeparator()

        self._help_menu = self.menuBar().addMenu("&Help")
        self._help_menu.addAction(self._about_act)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\FlannMicrowave.ico"))))
    window = MainWindow()
    window.show()

    app.exec()