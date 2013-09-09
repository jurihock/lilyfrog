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

    def pressKeys(self, scancodes):

        if len(scancodes) == 0: return

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