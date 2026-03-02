from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from UIFiles.qt_Move import Ui_Form
from UIModification.misc_BaseTech import MPTech, PSTech

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class Move(QWidget, Ui_Form, PSTech, MPTech):
    tech="Move"
    def __init__(self, *,i_ranges: list[str] = None):
        QWidget.__init__(self)
        PSTech.__init__(self)
        MPTech.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        # Model defaults
        self.name: str = "Move"
        self.delta_x: bool = False
        self.delta_y: bool = False
        self.delta_z: bool = False
        self.absolute: bool = False
        self.x_pos: float | None = None
        self.y_pos: float | None = None
        self.z_pos: float | None = None

        # Validators
        self.lineEdit.setValidator(QDoubleValidator(self))  # X
        self.lineEdit_2.setValidator(QDoubleValidator(self))  # Y
        self.lineEdit_3.setValidator(QDoubleValidator(self))  # Z
        self.lineEdit_4.setValidator(QDoubleValidator(self))  # ? maybe speed or something
        self.lineEdit_5.setValidator(QDoubleValidator(self))
        self.lineEdit_6.setValidator(QDoubleValidator(self))

        # Bind signals
        self.bindSignalSlot()

    def bindSignalSlot(self):
        self.checkBox.stateChanged.connect(self._setDeltaX)  # Delta X
        self.checkBox_2.stateChanged.connect(self._setDeltaY)  # Delta Y
        self.checkBox_3.stateChanged.connect(self._setDeltaZ)  # Delta Z
        self.checkBox_4.stateChanged.connect(self._setAbsolute)  # Absolute
        self.lineEdit.editingFinished.connect(self._setX)
        self.lineEdit_2.editingFinished.connect(self._setY)
        self.lineEdit_3.editingFinished.connect(self._setZ)

    def _setDeltaX(self, state):
        self.delta_x = state == 2  # Checked

    def _setDeltaY(self, state):
        self.delta_y = state == 2

    def _setDeltaZ(self, state):
        self.delta_z = state == 2

    def _setAbsolute(self, state):
        self.absolute = state == 2

    def _setX(self):
        self.x_pos = _float_or_none(self.lineEdit.text())

    def _setY(self):
        self.y_pos = _float_or_none(self.lineEdit_2.text())

    def _setZ(self):
        self.z_pos = _float_or_none(self.lineEdit_3.text())

    def outputParam(self) -> dict:
        return {
            'technique': self.tech.lower(),
            'name': self.name,
            'delta_x': self.delta_x,
            'delta_y': self.delta_y,
            'delta_z': self.delta_z,
            'absolute': self.absolute,
            'x_pos': self.x_pos,
            'y_pos': self.y_pos,
            'z_pos': self.z_pos,

            'loop': self.loop # Loop count for this technique (from base class)
        }