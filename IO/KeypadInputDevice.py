from PyQt4 import QtCore
from PyQt4.QtCore import QThread

from evdev import InputDevice, list_devices, ecodes
from evdev.events import KeyEvent

class KeypadInputDevice(QThread):

    device = None
    callback = QtCore.pyqtSignal(int)

    def isConnected(self):
        return self.device is not None

    def __init__(self, deviceVendor, deviceProduct):

        QThread.__init__(self)

        # Get list of available devices
        devices = map(InputDevice, list_devices())

        # Try to find the desired device
        for device in devices:

            # If multiple devices of same type available,
            # select the first, e.g. phys ".../input0"
            isDesiredDevice = \
                (device.info.vendor == deviceVendor) and \
                (device.info.product == deviceProduct) and \
                (device.phys.endswith('0'))

            if isDesiredDevice:
                self.device = device
                break

        # Get exclusive access to the device
        if self.isConnected():
            print 'Grab keypad input device.'
            self.device.grab()
    
    def setLed(self, value):

        if self.isConnected():
            self.device.set_led( \
                ecodes.LED_NUML, int(value))

    def stop(self):

        if self.isConnected():
            print 'Ungrab and close keypad input device.'
            self.device.ungrab()
            self.device.close()
            self.device = None

        if self.isRunning():
            if not self.wait(1000):
                print 'Terminate keypad input thread.'
                self.terminate()
                self.wait()

    def run(self):

        print 'Start keypad input thread.'

        try:

            # Wait for the next key down event
            # and callback the scan code
            for rawEvent in self.device.read_loop():

                isValidEvent = \
                    (rawEvent.type == ecodes.EV_KEY) and \
                    (rawEvent.value == KeyEvent.key_down)

                if isValidEvent:
                    event = KeyEvent(rawEvent)
                    self.callback.emit(event.scancode)

        except: pass

        print 'Finish keypad input thread.'
