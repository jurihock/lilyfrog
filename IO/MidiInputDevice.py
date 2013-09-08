from PyQt4 import QtCore
from PyQt4.QtCore import QThread

import rtmidi_python as rtmidi

class MidiInputDevice(QThread):

    device = None
    callback = QtCore.pyqtSignal(int)

    def isConnected(self):
        return self.device is not None

    def __init__(self, midiPort=0):

        QThread.__init__(self)

        print 'Open MIDI input device.'
        self.device = rtmidi.MidiIn()
        self.device.open_port(midiPort)

    def run(self):

        print 'Start MIDI input thread.'

        try:

            # Wait for the next note on message
            # and callback the note number
            while True:

                message, velocity = self.device.get_message()

                isValidMessage = \
                    (message is not None) and \
                    (message[0] >> 4 == 0x9) and \
                    (message[2] > 0)

                if isValidMessage:
                    notenum = message[1]
                    self.callback.emit(notenum)

        except: pass

        print 'Finish MIDI input thread.'

    def stop(self):

        if self.isConnected():
            print 'Close MIDI input device.'
            self.device.close_port()
            self.device = None

        if self.isRunning():
            if not self.wait(1000):
                print 'Terminate MIDI input thread.'
                self.terminate()
                self.wait()
