from PyQt4 import QtCore
from PyQt4.QtGui import QMainWindow

from MainWindowUI import Ui_MainWindow as MainWindowUI
from IOController import IOController

class MainWindow(QMainWindow, MainWindowUI):

    ioController = None
    isInitialized = False

    def __init__(self):

        QMainWindow.__init__(self)

        self.setupUi(self)
        self.setFixedSize(self.size())
        self.connectControlSignals()

    def showEvent(self, event):

        if not self.isInitialized:

            self.ioController = IOController()
            self.ioController.start()
            self.isInitialized = True

    def closeEvent(self, event):

        self.ioController.stop()
        event.accept()

    def connectControlSignals(self):

        self.ctrlAccidentalNone.toggled.connect(self.onAccidentalToggled)
        self.ctrlAccidentalFlat.toggled.connect(self.onAccidentalToggled)
        self.ctrlAccidentalSharp.toggled.connect(self.onAccidentalToggled)
        
        self.ctrlOctaveNone.toggled.connect(self.onOctaveToggled)
        self.ctrlOctaveDown.toggled.connect(self.onOctaveToggled)
        self.ctrlOctaveUp.toggled.connect(self.onOctaveToggled)

        self.ctrlDurationNone.toggled.connect(self.onDurationToggled)
        self.ctrlDuration64.toggled.connect(self.onDurationToggled)
        self.ctrlDuration32.toggled.connect(self.onDurationToggled)
        self.ctrlDuration16.toggled.connect(self.onDurationToggled)
        self.ctrlDuration8.toggled.connect(self.onDurationToggled)
        self.ctrlDuration4.toggled.connect(self.onDurationToggled)
        self.ctrlDuration2.toggled.connect(self.onDurationToggled)
        self.ctrlDuration1.toggled.connect(self.onDurationToggled)
        self.ctrlDurationBreve.toggled.connect(self.onDurationToggled)
        self.ctrlDurationLonga.toggled.connect(self.onDurationToggled)

        self.ctrlDurationDot.toggled.connect(self.onDurationDotToggled)

        self.ctrlEnable.toggled.connect(self.onEnableToggled)

    @QtCore.pyqtSlot(bool)
    def onAccidentalToggled(self, checked):
        if checked:
            print 'onAccidentalToggled'

    @QtCore.pyqtSlot(bool)
    def onOctaveToggled(self, checked):
        if checked:
            print 'onOctaveToggled'

    @QtCore.pyqtSlot(bool)
    def onDurationToggled(self, checked):
        if checked:
            print 'onDurationToggled'
    
    @QtCore.pyqtSlot(bool)
    def onDurationDotToggled(self, checked):
        print 'onDurationDotToggled'

    @QtCore.pyqtSlot(bool)
    def onEnableToggled(self, checked):
        print 'onEnableToggled'