from PyQt4 import QtCore
from PyQt4.QtCore import QObject
from evdev.ecodes import *

from IO import *

class IOController(QObject):

    # Controller state

    __isEnabled = False

    def isEnabled(self):
        return self.__isEnabled

    def setEnabled(self, value):
        self.__isEnabled = value
        self.keypadInput.setLed(value)
        self.reset()

    isEnabled = property(isEnabled, setEnabled)
    isEnabledCallback = QtCore.pyqtSignal(bool)

    # IO devices
    keyboardOutput = None
    keypadInput    = None
    midiInput      = None

    # Note parameters and possible values
    noteDuration      = 0     # 0 (none) 1/4. (longa) 1/2. (breve) 1 2 4 8 16 32 64
    noteDot           = False # True or False
    noteOctave        = 0     # -1 (down) 0 (none) +1 (up)
    noteAccidental    = 0     # -1 (flat) 0 (none) +1 (sharp)
    defaultAccidental = -1    # -1 (flat) +1 (sharp)
    
    noteParamCallback = QtCore.pyqtSignal()

    def __init__(self):

        QObject.__init__(self)

        self.keyboardOutput = KeyboardOutputDevice()
        self.keypadInput = KeypadInputDevice()
        self.midiInput = MidiInputDevice()

        self.keypadInput.callback.connect(self.keypadInputCallback)
        self.midiInput.callback.connect(self.midiInputCallback)
        
    def reset(self):
        
        self.noteDuration   = 0
        self.noteDot        = False
        self.noteOctave     = 0
        self.noteAccidental = 0
        
        self.noteParamCallback.emit()

    def start(self):

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

    def stop(self):

        self.keyboardOutput.stop()
        self.keypadInput.stop()
        self.midiInput.stop()

    @QtCore.pyqtSlot(int)
    def keypadInputCallback(self, scancode):

        # print 'keypadInputCallback => %i' % scancode

        if scancode == KEY_NUMLOCK:

            self.isEnabled = not self.isEnabled
            self.isEnabledCallback.emit(self.isEnabled)
            return

        elif not self.isEnabled: return

        # Note parameters
        if scancode == KEY_KP1:
            self.noteDuration = 64 if self.noteDuration != 64 else 0
        elif scancode == KEY_KP2:
            self.noteDuration = 32 if self.noteDuration != 32 else 0
        elif scancode == KEY_KP3:
            self.noteDuration = 16 if self.noteDuration != 16 else 0
        elif scancode == KEY_KP4:
            self.noteDuration = 8 if self.noteDuration != 8 else 0
        elif scancode == KEY_KP5:
            self.noteDuration = 4 if self.noteDuration != 4 else 0
        elif scancode == KEY_KP6:
            self.noteDuration = 2 if self.noteDuration != 2 else 0
        elif scancode == KEY_KP7:
            self.noteDuration = 1 if self.noteDuration != 1 else 0
        elif scancode == KEY_KP8:
            self.noteDuration = 1/2. if self.noteDuration != 1/2. else 0
        elif scancode == KEY_KP9:
            self.noteDuration = 1/4. if self.noteDuration != 1/4. else 0
        elif scancode == KEY_KPDOT:
            self.noteDot = not self.noteDot
        elif scancode == KEY_KPMINUS:
            self.noteOctave = -1 if self.noteOctave >= 0 else 0
        elif scancode == KEY_KPPLUS:
            self.noteOctave = +1 if self.noteOctave <= 0 else 0
        elif scancode == KEY_KPSLASH:
            self.noteAccidental = -1 if self.noteAccidental >= 0 else 0
        elif scancode == KEY_KPASTERISK:
            self.noteAccidental = +1 if self.noteAccidental <= 0 else 0

        self.noteParamCallback.emit()

        notestr = ''

        # Special keys
        if scancode == KEY_BACKSPACE:
            notestr = '\b'
        elif scancode == KEY_KP0:
            notestr = self.getNoteString(-1)
            self.reset()
        elif scancode == KEY_SPACE:
            notestr = '~ '
        elif scancode == KEY_KPENTER:
            notestr = '|\n'

        self.keyboardOutput.pressKeyString(notestr)

    @QtCore.pyqtSlot(int)
    def midiInputCallback(self, scancode):

        # print 'midiInputCallback => %i' % scancode

        if not self.isEnabled: return

        notenum = scancode % 12
        # octavenum = scancode / 12

        notestr = self.getNoteString(notenum)
        self.reset()

        self.keyboardOutput.pressKeyString(notestr)

    def getNoteString(self, notenum):
        
        notestr = []
        
        # if rest, not note
        if notenum == -1:
            notestr.append('r')

        # if flat was requested
        if notenum >= 0 and self.noteAccidental < 0:

            if notenum == 0:    notestr.append('c')
            elif notenum == 1:  notestr.append('des')
            elif notenum == 2:  notestr.append('d')
            elif notenum == 3:  notestr.append('es')
            elif notenum == 4:  notestr.append('fes')
            elif notenum == 5:  notestr.append('f')
            elif notenum == 6:  notestr.append('ges')
            elif notenum == 7:  notestr.append('g')
            elif notenum == 8:  notestr.append('as')
            elif notenum == 9:  notestr.append('a')
            elif notenum == 10: notestr.append('bes')
            elif notenum == 11: notestr.append('ces')

        # if sharp was requested
        elif notenum >= 0 and self.noteAccidental > 0:

            if notenum == 0:    notestr.append('bis')
            elif notenum == 1:  notestr.append('cis')
            elif notenum == 2:  notestr.append('d')
            elif notenum == 3:  notestr.append('dis')
            elif notenum == 4:  notestr.append('e')
            elif notenum == 5:  notestr.append('eis')
            elif notenum == 6:  notestr.append('fis')
            elif notenum == 7:  notestr.append('g')
            elif notenum == 8:  notestr.append('gis')
            elif notenum == 9:  notestr.append('a')
            elif notenum == 10: notestr.append('ais')
            elif notenum == 11: notestr.append('b')
        
        # if flat is default
        elif notenum >= 0 and self.defaultAccidental < 0:
            
            if notenum == 0:    notestr.append('c')
            elif notenum == 1:  notestr.append('des')
            elif notenum == 2:  notestr.append('d')
            elif notenum == 3:  notestr.append('es')
            elif notenum == 4:  notestr.append('e')
            elif notenum == 5:  notestr.append('f')
            elif notenum == 6:  notestr.append('ges')
            elif notenum == 7:  notestr.append('g')
            elif notenum == 8:  notestr.append('as')
            elif notenum == 9:  notestr.append('a')
            elif notenum == 10: notestr.append('bes')
            elif notenum == 11: notestr.append('b')

        # if sharp is default
        elif notenum >= 0 and self.defaultAccidental > 0:

            if notenum == 0:    notestr.append('c')
            elif notenum == 1:  notestr.append('cis')
            elif notenum == 2:  notestr.append('d')
            elif notenum == 3:  notestr.append('dis')
            elif notenum == 4:  notestr.append('e')
            elif notenum == 5:  notestr.append('f')
            elif notenum == 6:  notestr.append('fis')
            elif notenum == 7:  notestr.append('g')
            elif notenum == 8:  notestr.append('gis')
            elif notenum == 9:  notestr.append('a')
            elif notenum == 10: notestr.append('ais')
            elif notenum == 11: notestr.append('b')

        # if octave was requested
        if notenum >= 0 and self.noteOctave < 0:
            notestr.append(',')
        elif notenum >= 0 and self.noteOctave > 0:
            notestr.append('\'')

        # if duration was requested
        if self.noteDuration:
            if self.noteDuration == 1/4.:
                notestr.append('\\longa')
            elif self.noteDuration == 1/2.:
                notestr.append('\\breve')
            else:
                notestr.append(str(self.noteDuration))
        
        # if dot was requested
        if self.noteDot:
            notestr.append('.')

        # note delimiter
        notestr.append(' ')

        return ''.join(notestr)
