from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import datetime
import os
import re   

from misc_PrintException import print_ex

class ECOuija(QMainWindow):
    def __init__(self):
        super().__init__()
        self.LoadUI()
        self.showMaximized()

    def LoadUI(self):
        self.ui=uic.loadUi('qt_EC.ui',self)




if __name__ =='__main__':
    try:
        Qapp=QApplication(sys.argv)
        app=ECOuija()
        sys.exit(Qapp.exec_())
    except Exception as ex:
        print_ex(ex)