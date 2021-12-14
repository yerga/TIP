# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QSettings
from tips.ui.ui_mainwindow import Ui_MainWindow
from tips.ui.ui_utils import getFileName
from tips.datareading.read_settings import get_exp_settings

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
        self.actionQuit = self.ui.actionQuit
        self.actionQuit.triggered.connect(self.quitApp)

        ###################
        #  Top tabwidget  #
        ###################
        self.topTabWidget = self.ui.tabWidget
        self.topTabWidget.setCurrentIndex(0)

        ###################
        #  Data Info tab  #
        ###################
        self.selectFileButton = self.ui.selectFileButton
        self.selectFileButton.clicked.connect(self.selectFile)

        self.filenameLE = self.ui.filenameLE
        self.xwidthLE = self.ui.xwidthLE
        self.ywidthLE = self.ui.ywidthLE
        self.hopdistanceLE = self.ui.hopdistanceLE
        self.nchannelsLE = self.ui.nchannelsLE
        self.cyclesLE = self.ui.cyclesLE
        self.labviewprogramCBox = self.ui.labviewprogramCBox
        self.acqrateLE = self.ui.acqtimeLE

        self.localsettingsTE = self.ui.localSettingsTE
        self.globalsettingsTE = self.ui.globalSettingsTE
        self.channelsTE = self.ui.channelsTE

        self.XchannelLE = self.ui.XCN_LE
        self.YchannelLE = self.ui.YCN_LE
        self.ZchannelLE = self.ui.ZCN_LE
        self.C1channelLE = self.ui.C1CN_LE
        self.V1channelLE = self.ui.V1CN_LE
        self.LNchannelLE = self.ui.LNCN_LE
        self.DTchannelLE = self.ui.DTCN_LE


    def quitApp(self):
        """
        Quit application
        """
        app = QApplication.instance()
        app.quit()

    def selectFile(self):
        self.filename = getFileName(self, path=self.lastpath)
        if self.filename:
            self.lastpath = os.path.dirname(self.filename)
            self.settings.setValue("lastpath", self.lastpath)
            self.set_settings_to_gui()


    def set_settings_to_gui(self):
        self.filenameLE.setText(self.filename)
        allsettings, datasettings = get_exp_settings(self.filename)
        localsettings, globalsettings, savedchannels = allsettings
        
        self.xwidthLE.setText(datasettings["xwidth"])
        self.ywidthLE.setText(datasettings["ywidth"])
        self.hopdistanceLE.setText(datasettings["hopdistance"])
        self.nchannelsLE.setText(str(datasettings["nchannels"]))
        self.cyclesLE.setText(datasettings["ncycles"])
        self.labviewprogramCBox.setCurrentText(datasettings["labvprogram"])
        self.acquisition_rate = int(datasettings["sampletime"]) * (int(datasettings["samplespdp"]) + 1) #in us
        self.acqrateLE.setText(str(self.acquisition_rate))

        self.localsettingsTE.setText(localsettings)
        self.globalsettingsTE.setText(globalsettings)
        self.channelsTE.setText(savedchannels)

