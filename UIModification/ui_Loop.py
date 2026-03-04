from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from UIFiles.qt_Loop import Ui_Form
from UIModification.misc_BaseTech import MOTech


class Loop(QWidget, Ui_Form, MOTech):
    tech="Loop"
    def __init__(self, *, _i_ranges: list[str] = None):
        QWidget.__init__(self)
        MOTech.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        # Model defaults
        self.name: str = "Loop"
        self.iterations: int = 5

        # Validators
        self.lineEditIter.setValidator(QIntValidator(1, 100, self))  # 1 to 100 iterations

        # Bind signals
        self.bindSignalSlot()

    def bindSignalSlot(self):
        self.lineEditIter.editingFinished.connect(self._pullFields)

    def _pullFields(self):
        """Pull current UI values into the model (with light parsing)."""
        try:
            self.name = self.lineEditName.text()
            self.iterations = int(self.lineEditIter.text())
        except ValueError as e:
            QMessageBox.warning(self, "Parse error", str(e))
            return
        
    def outputParam(self) -> dict:
        return {
            'technique': self.tech.lower(),
            'name': self.name,
            'iterations': self.iterations,

            'loop': self.loop # Loop count for this technique (from base class)
        }