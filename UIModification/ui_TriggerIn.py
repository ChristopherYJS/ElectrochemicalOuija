from __future__ import annotations

from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtGui import QIntValidator

from UIFiles.qt_TriggerIn import Ui_Form
from UIModification.misc_BaseTech import PSTech


class TriggerIn(QWidget, Ui_Form, PSTech):
    tech = "Trigger"
    trigger_type = "in"

    def __init__(self, *, _i_ranges: list[str] | None = None):
        QWidget.__init__(self)
        PSTech.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        self.name: str = "TriggerIn"
        self.logic: int = 1

        self.lineEditName.setText(self.name)
        self.lineEditIter.setText(str(self.logic))
        self.lineEditIter.setValidator(QIntValidator(0, 1, self))
        self.lineEditIter.setToolTip("Trigger input logic level: 0 for low, 1 for high")

        self.bindSignalSlot()
        self._pullFields()

    def bindSignalSlot(self):
        self.lineEditName.editingFinished.connect(self._setName)
        self.lineEditIter.editingFinished.connect(self._pullFields)

    def _setName(self):
        self._pullFields()
        suffix = (self.name or "").strip()
        label = "TriggerIn" if suffix == "" else f"TriggerIn_{suffix}"
        self.nameChanged.emit(label)

    def _pullFields(self):
        try:
            self.name = self.lineEditName.text()
            self.logic = int(self.lineEditIter.text() or 0)
        except ValueError as e:
            self.validated = False
            QMessageBox.warning(self, "Parse error", str(e))
            return

    def _validateParams(self) -> bool:
        self.validated = False
        raw_logic = self.lineEditIter.text().strip()

        if raw_logic == "":
            QMessageBox.warning(self, "Missing field", f"TriggerIn_{self.name}: Logic cannot be empty.")
            return False

        try:
            logic = int(raw_logic)
        except ValueError:
            QMessageBox.warning(self, "Invalid type", f"TriggerIn_{self.name}: Logic must be int.")
            return False

        if logic not in (0, 1):
            QMessageBox.warning(self, "Invalid value", f"TriggerIn_{self.name}: Logic must be 0 or 1.")
            return False

        self.validated = True
        return True

    def outputParam(self) -> dict | None:
        self._pullFields()
        self._validateParams()
        if not self.validated:
            return None

        return {
            "technique": "trigger",
            "name": self.name,
            "type": self.trigger_type,
            "logic": self.logic,
            "loop": self.loop,
        }