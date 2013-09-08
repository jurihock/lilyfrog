from PyQt4 import QtCore
from evdev.ecodes import *

from IO import *

class IOController:

    keyboardOutput = None
    keypadInput    = None
    midiInput      = None

    isEnabled = True

    noteDuration          = []
    isDotRequested        = False
    isOctaveDownRequested = False
    isOctaveUpRequested   = False
    isFlatRequested       = False
    isSharpRequested      = False

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

        # State variables
        if scancode == KEY_NUMLOCK:
            self.isEnabled = not self.isEnabled
        elif scancode == KEY_KPDOT:
            self.isDotRequested = not self.isDotRequested
        elif scancode == KEY_KPMINUS:
            self.isOctaveDownRequested = not self.isOctaveDownRequested
        elif scancode == KEY_KPPLUS:
            self.isOctaveUpRequested = not self.isOctaveUpRequested
        elif scancode == KEY_KPSLASH:
            self.isFlatRequested = not self.isFlatRequested
        elif scancode == KEY_KPASTERISK:
            self.isSharpRequested = not self.isSharpRequested
        # Note duration
        elif scancode == KEY_KP1:
            self.noteDuration = [KEY_6, KEY_4]
        elif scancode == KEY_KP2:
            self.noteDuration = [KEY_3, KEY_2]
        elif scancode == KEY_KP3:
            self.noteDuration = [KEY_1, KEY_6]
        elif scancode == KEY_KP4:
            self.noteDuration = [KEY_8]
        elif scancode == KEY_KP5:
            self.noteDuration = [KEY_4]
        elif scancode == KEY_KP6:
            self.noteDuration = [KEY_2]
        elif scancode == KEY_KP7:
            self.noteDuration = [KEY_1]
        elif scancode == KEY_KP8:
            self.noteDuration = [KEY_BACKSLASH, KEY_B, KEY_R, KEY_E, KEY_V, KEY_E]
        elif scancode == KEY_KP9:
            self.noteDuration = [KEY_BACKSLASH, KEY_L, KEY_O, KEY_N, KEY_G, KEY_A]
        # Special keys
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
        # octave = notenum / 12

        keys = []

        if self.isFlatRequested:

            if note == 0:
                keys.extend([KEY_C])
            elif note == 1:
                keys.extend([KEY_D, KEY_E, KEY_S])
            elif note == 2:
                keys.extend([KEY_D])
            elif note == 3:
                keys.extend([KEY_E, KEY_S])
            elif note == 4:
                keys.extend([KEY_F, KEY_E, KEY_S])
            elif note == 5:
                keys.extend([KEY_F])
            elif note == 6:
                keys.extend([KEY_G, KEY_E, KEY_S])
            elif note == 7:
                keys.extend([KEY_G])
            elif note == 8:
                keys.extend([KEY_A, KEY_S])
            elif note == 9:
                keys.extend([KEY_A])
            elif note == 10:
                keys.extend([KEY_B, KEY_E, KEY_S])
            elif note == 11:
                keys.extend([KEY_C, KEY_E, KEY_S])

            self.isFlatRequested = not self.isFlatRequested

        elif self.isSharpRequested:

            if note == 0:
                keys.extend([KEY_H, KEY_I, KEY_S])
            elif note == 1:
                keys.extend([KEY_C, KEY_I, KEY_S])
            elif note == 2:
                keys.extend([KEY_D])
            elif note == 3:
                keys.extend([KEY_D, KEY_I, KEY_S])
            elif note == 4:
                keys.extend([KEY_E])
            elif note == 5:
                keys.extend([KEY_E, KEY_I, KEY_S])
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

            self.isSharpRequested = not self.isSharpRequested

        else:

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
        
        if self.isOctaveDownRequested:
            keys.extend([KEY_COMMA])
            self.isOctaveDownRequested = not self.isOctaveDownRequested
        elif self.isOctaveUpRequested:
            keys.extend([KEY_APOSTROPHE])
            keys.extend([KEY_SPACE]) # US international layout
            self.isOctaveUpRequested = not self.isOctaveUpRequested

        keys.extend(self.noteDuration)
        self.noteDuration = []

        if self.isDotRequested:
            keys.extend([KEY_DOT])
            self.isDotRequested = not self.isDotRequested

        keys.extend([KEY_SPACE])

        self.keyboardOutput.pressKeys(keys)
