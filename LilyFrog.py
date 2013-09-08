import sys
from PyQt4 import QtGui

from GUI import *

def main():

    application = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()