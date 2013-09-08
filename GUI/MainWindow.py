from PyQt4 import QtCore
from PyQt4.QtGui import QMainWindow

from MainWindowUI import Ui_MainWindow as MainWindowUI
from IOController import IOController

class MainWindow(QMainWindow, MainWindowUI):

    ioController = None

    def __init__(self):

        QMainWindow.__init__(self)

        self.setupUi(self)
        self.setFixedSize(self.size())

        self.ioController = IOController()
        self.ioController.startPolling()

    def closeEvent(self, event):

        self.ioController.stopPolling()
        event.accept()
