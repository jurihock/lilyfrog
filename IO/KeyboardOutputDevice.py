from evdev import UInput
from evdev.events import KeyEvent
from evdev.ecodes import *

class KeyboardOutputDevice:

    device = None

    def isConnected(self):
        return self.device is not None

    def __init__(self, deviceName='LilyFrog'):

        print 'Open keyboard output device.'
        self.device = UInput(name=deviceName)

    def stop(self):

        if self.isConnected():
            print 'Close keyboard output device.'
            self.device.close()
            self.device = None
            
    def pressKeyString(self, keystr):
        
        # print 'pressKeyString => %s' % keystr

        if not len(keystr): return

        scancodes = []
        
        for keychr in keystr:
            
            if keychr == 'r':   scancodes.extend([KEY_R])

            elif keychr == 'c': scancodes.extend([KEY_C])
            elif keychr == 'd': scancodes.extend([KEY_D])
            elif keychr == 'e': scancodes.extend([KEY_E])
            elif keychr == 'f': scancodes.extend([KEY_F])
            elif keychr == 'g': scancodes.extend([KEY_G])
            elif keychr == 'a': scancodes.extend([KEY_A])
            elif keychr == 'b': scancodes.extend([KEY_B])
            elif keychr == 'i': scancodes.extend([KEY_I])
            elif keychr == 's': scancodes.extend([KEY_S])

            elif keychr == ',': scancodes.extend([KEY_COMMA])
            elif keychr == '\'': scancodes.extend([KEY_APOSTROPHE, KEY_SPACE]) # consider the dead key
            
            elif keychr == '\\': scancodes.extend([KEY_BACKSLASH])
            elif keychr == 'l': scancodes.extend([KEY_L])
            elif keychr == 'o': scancodes.extend([KEY_O])
            elif keychr == 'n': scancodes.extend([KEY_N])
            elif keychr == 'v': scancodes.extend([KEY_V])
            elif keychr == '1': scancodes.extend([KEY_1])
            elif keychr == '2': scancodes.extend([KEY_2])
            elif keychr == '3': scancodes.extend([KEY_3])
            elif keychr == '4': scancodes.extend([KEY_4])
            elif keychr == '6': scancodes.extend([KEY_6])
            elif keychr == '8': scancodes.extend([KEY_8])
            elif keychr == '.': scancodes.extend([KEY_DOT])
            
            elif keychr == '~': scancodes.extend([[KEY_GRAVE], KEY_SPACE]) # consider the dead key
            elif keychr == '|': scancodes.extend([[KEY_BACKSLASH]])
            elif keychr == '\b': scancodes.extend([KEY_BACKSPACE])
            elif keychr == '\n': scancodes.extend([KEY_ENTER])

            elif keychr == ' ': scancodes.extend([KEY_SPACE])

            else: raise ValueError('Invalid key string value \'%s\'!' % keychr)

        self.pressKeys(scancodes)

    def pressKeys(self, scancodes):

        if not len(scancodes): return

        for scancode in scancodes:

            isShiftRequired = isinstance(scancode, list)

            if not isShiftRequired:

                self.device.write(EV_KEY, scancode, KeyEvent.key_down)
                self.device.write(EV_KEY, scancode, KeyEvent.key_up)

            else:

                self.device.write(EV_KEY, KEY_LEFTSHIFT, KeyEvent.key_down)
                self.device.write(EV_KEY, scancode[0],   KeyEvent.key_down)
                self.device.write(EV_KEY, scancode[0],   KeyEvent.key_up)
                self.device.write(EV_KEY, KEY_LEFTSHIFT, KeyEvent.key_up)

        self.device.syn()