from PyQt4 import QtCore
from PyQt4.QtGui import QApplication
import sys

from GUI import MainWindow

if __name__ == '__main__':

    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec_())
