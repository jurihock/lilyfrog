from PyQt4 import QtCore
from PyQt4.QtGui import QWidget

from IOController import IOController

class MainWindow(QWidget):

    ioController = None

    def __init__(self):

        super(MainWindow, self).__init__()
        self.initUI()

        self.ioController = IOController()
        self.ioController.startPolling()

    def initUI(self):

        self.setWindowTitle('LilyFrog')
        self.setGeometry(10, 10, 640, 480)

    def closeEvent(self, event):

        self.ioController.stopPolling()
        event.accept()
