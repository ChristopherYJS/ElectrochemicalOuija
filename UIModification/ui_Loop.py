from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from UIFiles.qt_Loop import Ui_Form
from misc_BaseTech import PSTech

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class Loop(QWidget, Ui_Form):
    tech="Loop"
    def __init__(self, *,i_ranges: list[str] = None):
        super().__init__()
        self.setupUi(self)

        # Model defaults
        self.name: str = "Loop"
        self.iterations: int = 5

        # Validators
        self.lineEdit.setValidator(QIntValidator(1, 100, self))  # 1 to 100 iterations

        # Bind signals
        self.bindSignalSlot()

    def bindSignalSlot(self):
        self.lineEdit.editingFinished.connect(self._setIterations)

    def _setIterations(self):
        try:
            self.iterations = int(self.lineEdit.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for iterations.")
            self.lineEdit.setText(str(self.iterations))

    def outputParam(self) -> dict:
        return {
            'technique': self.tech.lower(),
            'name': self.name,
            'iterations': self.iterations
        }