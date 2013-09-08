from PyQt4 import QtCore
from evdev.ecodes import *

from IO import *

class IOController:

    keyboardOutput = None
    keypadInput    = None
    midiInput      = None

    isEnabled = True

    noteDuration          = 5
    isDotRequested        = False
    isOctaveDownRequested = False
    isOctaveUpRequested   = False
    isSharpRequested      = False
    isFlatRequested       = False

    def __init__(self):

        self.keyboardOutput = KeyboardOutputDevice()
        self.keypadInput = KeypadInputDevice()
        self.midiInput = MidiInputDevice()

        self.keypadInput.callback.connect(self.keypadInputCallback)
        self.midiInput.callback.connect(self.midiInputCallback)

    def startPolling(self):

        if not self.keyboardOutput.isConnected():
            print 'Keyboard output device could not be connected!'

        if self.keypadInput.isConnected():
            self.keypadInput.start()
        else:
            print 'Keypad input device could not be connected!'

        if self.midiInput.isConnected():
            self.midiInput.start()
        else:
            print 'MIDI input device could not be connected!'

    def stopPolling(self):

        self.keyboardOutput.close()
        self.keypadInput.stop()
        self.midiInput.stop()

    @QtCore.pyqtSlot(int)
    def keypadInputCallback(self, scancode):

        # print scancode

        keys = []

        if scancode == KEY_NUMLOCK:
            pass # TODO
        elif scancode == KEY_BACKSPACE:
            keys.extend([KEY_BACKSPACE])
        elif scancode == KEY_KPENTER:
            keys.extend([[KEY_BACKSLASH], KEY_ENTER])
        elif scancode == KEY_KP0:
            keys.extend([KEY_R, KEY_SPACE])

        self.keyboardOutput.pressKeys(keys)

    @QtCore.pyqtSlot(int)
    def midiInputCallback(self, notenum):

        # print notenum % 12, notenum / 12

        note = notenum % 12
        octave = notenum / 12

        keys = []

        if note == 0:
            keys.extend([KEY_C])
        elif note == 1:
            keys.extend([KEY_C, KEY_I, KEY_S])
        elif note == 2:
            keys.extend([KEY_D])
        elif note == 3:
            keys.extend([KEY_D, KEY_I, KEY_S])
        elif note == 4:
            keys.extend([KEY_E])
        elif note == 5:
            keys.extend([KEY_F])
        elif note == 6:
            keys.extend([KEY_F, KEY_I, KEY_S])
        elif note == 7:
            keys.extend([KEY_G])
        elif note == 8:
            keys.extend([KEY_G, KEY_I, KEY_S])
        elif note == 9:
            keys.extend([KEY_A])
        elif note == 10:
            keys.extend([KEY_A, KEY_I, KEY_S])
        elif note == 11:
            keys.extend([KEY_B])

        keys.extend([KEY_SPACE])

        self.keyboardOutput.pressKeys(keys)
