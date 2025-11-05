from qt_CA import Ui_Form
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal


class CA(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #get current range and bandwidth options from the main UI and load them into the comboboxes
        self.nameSignal=Signal(str)
    def SignalSlotBinding(self):
        self.lineEditName.editingFinished.connect(lambda: self.nameSignal.emit(self.lineEditName.text()))