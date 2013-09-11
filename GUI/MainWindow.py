from PyQt4 import QtCore
from PyQt4.QtGui import QMainWindow

from MainWindowUI import Ui_MainWindow as MainWindowUI
from IOController import IOController

class MainWindow(QMainWindow, MainWindowUI):

    isInitialized = False
    ioController = None

    def __init__(self):

        QMainWindow.__init__(self)

        self.setupUi(self)
        self.setFixedSize(self.size())
        self.connectControlSignals()

    def showEvent(self, event):

        if not self.isInitialized:

            self.isInitialized = True

            self.ioController = IOController()
            self.ioController.isEnabled = False
            self.ioController.start()

            self.ioController.isEnabledCallback.connect(self.onEnableChanged)
            self.ioController.noteParamCallback.connect(self.onNoteParamChanged)

            self.ctrlKeyboardOutput.setChecked( \
                self.ioController.keyboardOutput.isConnected())
            self.ctrlKeypadInput.setChecked( \
                self.ioController.keypadInput.isConnected())
            self.ctrlMidiInput.setChecked( \
                self.ioController.midiInput.isConnected())

    def closeEvent(self, event):

        self.ioController.stop()
        event.accept()

    def connectControlSignals(self):
        
        self.ctrlDefaultAccidentalFlat.toggled.connect(self.onDefaultAccidentalToggled)
        self.ctrlDefaultAccidentalSharp.toggled.connect(self.onDefaultAccidentalToggled)

        self.ctrlEnable.toggled.connect(self.onEnableToggled)

    @QtCore.pyqtSlot(bool)
    def onDefaultAccidentalToggled(self, checked):
        if checked:
            if self.ctrlDefaultAccidentalFlat.isChecked():
                self.ioController.defaultAccidental = -1
            elif self.ctrlDefaultAccidentalSharp.isChecked():
                self.ioController.defaultAccidental = 1

    @QtCore.pyqtSlot(bool)
    def onEnableToggled(self, checked):
        self.ioController.isEnabled = checked

    @QtCore.pyqtSlot(bool)
    def onEnableChanged(self, checked):
        self.ctrlEnable.setChecked(checked)
        
    @QtCore.pyqtSlot()
    def onNoteParamChanged(self):

        if self.ioController.noteDuration == 1/4.:
            self.ctrlDurationLonga.setChecked(True)
        elif self.ioController.noteDuration == 1/2.:
            self.ctrlDurationBreve.setChecked(True)
        elif self.ioController.noteDuration == 1:
            self.ctrlDuration1.setChecked(True)
        elif self.ioController.noteDuration == 2:
            self.ctrlDuration2.setChecked(True)
        elif self.ioController.noteDuration == 4:
            self.ctrlDuration4.setChecked(True)
        elif self.ioController.noteDuration == 8:
            self.ctrlDuration8.setChecked(True)
        elif self.ioController.noteDuration == 16:
            self.ctrlDuration16.setChecked(True)
        elif self.ioController.noteDuration == 32:
            self.ctrlDuration32.setChecked(True)
        elif self.ioController.noteDuration == 64:
            self.ctrlDuration64.setChecked(True)
        else:
            self.ctrlDurationNone.setChecked(True)
            
        self.ctrlDurationDot.setChecked( \
            self.ioController.noteDot)

        if self.ioController.noteOctave == -1:
            self.ctrlOctaveDown.setChecked(True)
        elif self.ioController.noteOctave == 1:
            self.ctrlOctaveUp.setChecked(True)
        else:
            self.ctrlOctaveNone.setChecked(True)

        if self.ioController.noteAccidental == -1:
            self.ctrlAccidentalFlat.setChecked(True)
        elif self.ioController.noteAccidental == 1:
            self.ctrlAccidentalSharp.setChecked(True)
        else:
            self.ctrlAccidentalNone.setChecked(True)
