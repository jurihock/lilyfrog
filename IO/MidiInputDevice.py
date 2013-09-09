from PyQt4 import QtCore
from PyQt4.QtCore import QObject

import rtmidi_python as rtmidi

class MidiInputDevice(QObject):

    device = None
    callback = QtCore.pyqtSignal(int)

    def isConnected(self):
        return self.device is not None

    def __init__(self):
        
        QObject.__init__(self)

        print 'Open MIDI input device.'
        self.device = rtmidi.MidiIn()
        self.device.callback = self.deviceCallback

    def start(self, midiPort=0):

        print 'Start MIDI input device.'
        self.device.open_port(midiPort)

    def stop(self):

        if self.isConnected():
            print 'Close MIDI input device.'
            self.device.close_port()
            self.device = None

    def deviceCallback(self, message, velocity):

        isValidMessage = \
            (message[0] >> 4 == 0x9) and \
            (message[2] > 0)

        if isValidMessage:
            notenum = message[1]
            self.callback.emit(notenum)
