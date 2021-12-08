# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QSettings
from tips.ui.ui_mainwindow import Ui_MainWindow

APPVERSION = "0.1.0"
APPNAME = "Tips - Electrochemical Imaging Analysis"

def run_gui():
    """
    Creates and run the GUI application
    :return:
    """

    app = QApplication(sys.argv)
    app.setApplicationName(APPNAME)
    app.setApplicationVersion(APPVERSION)

    window = MainWindow()
    window.setWindowTitle(APPNAME)
    window.show()

    sys.exit(app.exec_())


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # Initializing some variables
        self.filename = ""
        self.settings = QSettings('org.weig', 'tips')
        self.lastpath = str(self.settings.value("lastpath"))
        self.cvdir = 'CVdir'

        # Creating and setting up the GUI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupMainWindow()


    def setupMainWindow(self):
        """
        Read widgets from UI file, and connect signals and initial properties
        :return:
        """
        pass