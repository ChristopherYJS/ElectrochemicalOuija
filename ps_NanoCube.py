from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from pipython import GCSDevice
from misc_PrintException import print_ex

import numpy as np
import time

class NanoCube(QThread):
    sig_loginfo=pyqtSignal(str) 
    def __init__(self):
        super().__init__()
        self.mpDeviceDic={}
    def run(self):
    #make connection
        self.sig_loginfo.emit('Connecting...')
        self.devz=GCSDevice('P-611.3S')
        self.devz.OpenRS232DaisyChain(comport=10, baudrate=9600)
        chainid=self.devz.dcid
        self.devz.ConnectDaisyChainDevice(3, chainid)
        self.devy=GCSDevice('P-611.3S')
        self.devy.ConnectDaisyChainDevice(2, chainid)
        self.devx=GCSDevice('P-611.3S')
        self.devx.ConnectDaisyChainDevice(1, chainid)
        self.mpDeviceDic={0:self.devx,1:self.devy,2:self.devz}