from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from UIModification.misc_BaseTech import PSTech
from UIFiles.qt_CV import Ui_Form


def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)


class CV(QWidget, Ui_Form, PSTech):

    tech = "CV"

    def __init__(self):
        QWidget.__init__(self)
        PSTech.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        # 2) Model defaults
        self.name: str = "CV"
        self.ei: float | int | None = None
        self.e1: float | int | None = None
        self.e2: float | int | None = None
        self.ef: float | int | None = None
        self.scan_rate: int | float = 0
        self.scan_number: int = 2
        self.sample_potential: int | float = 0
        self.repeat: int = 1
        self.average: bool = False
        self.step_begin: int | float = 0
        self.step_end: int | float = 1

        # 3) Validators on edits
        self.lineEditPotentialInit.setValidator(QDoubleValidator(self))
        self.lineEditPotentialFirst.setValidator(QDoubleValidator(self))
        self.lineEditPotentialSecond.setValidator(QDoubleValidator(self))
        self.lineEditPotentialFin.setValidator(QDoubleValidator(self))
        self.lineEditRate.setValidator(QDoubleValidator(self))
        self.lineEditSamplePotential.setValidator(QDoubleValidator(self))
        self.lineEditSamplePotential.setToolTip('potential step per point (ΔE in V): smaller value = more points')
        self.lineEditRepeat.setValidator(QIntValidator(1, 999, self))
        self.lineEditStepBegin.setValidator(QDoubleValidator(0.0, 1.0, 2, self))
        self.lineEditStepEnd.setValidator(QDoubleValidator(0.0, 1.0, 2, self))

        # 4) Bind signals -> model updates
        self.bindSignalSlot()

    # ---------------- Binding & helpers ----------------

    def bindSignalSlot(self):
        # Name
        self.lineEditName.editingFinished.connect(self._setName)

        # Scalar fields
        self.lineEditPotentialInit.editingFinished.connect(self._pullFields)
        self.lineEditPotentialFirst.editingFinished.connect(self._pullFields)
        self.lineEditPotentialSecond.editingFinished.connect(self._pullFields)
        self.lineEditPotentialFin.editingFinished.connect(self._pullFields)
        self.lineEditRate.editingFinished.connect(self._pullFields)
        self.lineEditSamplePotential.editingFinished.connect(self._pullFields)
        self.lineEditRepeat.editingFinished.connect(self._pullFields)
        self.lineEditStepBegin.editingFinished.connect(self._pullFields)
        self.lineEditStepEnd.editingFinished.connect(self._pullFields)
        self.checkBoxAverage.toggled.connect(self._pullFields)

    def _setName(self):
        self._pullFields()
        suffix = (self.name or "").strip()
        label = self.tech if suffix == "" else f"{self.tech}_{suffix}"
        self.nameChanged.emit(label)

    def _pullFields(self):
        """Pull current UI values into the model (with light parsing)."""
        try:
            self.name = self.lineEditName.text()
            self.ei = _float_or_none(self.lineEditPotentialInit.text())
            self.e1 = _float_or_none(self.lineEditPotentialFirst.text())
            self.e2 = _float_or_none(self.lineEditPotentialSecond.text())
            self.ef = _float_or_none(self.lineEditPotentialFin.text())
            self.scan_rate = float(self.lineEditRate.text() or 0)
            self.sample_potential = float(self.lineEditSamplePotential.text() or 0)
            self.repeat = int(self.lineEditRepeat.text() or 1)
            self.average = self.checkBoxAverage.isChecked()
            self.step_begin = float(self.lineEditStepBegin.text() or 0)
            self.step_end = float(self.lineEditStepEnd.text() or 1)
        except ValueError as e:
            QMessageBox.warning(self, "Parse error", str(e))
            return

    def _validateParams(self) -> bool:
        checks = [
            ("Initial Potential", self.lineEditPotentialInit.text().strip(), float),
            ("First Vertex", self.lineEditPotentialFirst.text().strip(), float),
            ("Second Vertex", self.lineEditPotentialSecond.text().strip(), float),
            ("Final Potential", self.lineEditPotentialFin.text().strip(), float),
            ("Scan Rate", self.lineEditRate.text().strip(), float),
            ("Sample Potential", self.lineEditSamplePotential.text().strip(), float),
            ("Repeat", self.lineEditRepeat.text().strip(), int),
            ("Begin Step", self.lineEditStepBegin.text().strip(), float),
            ("End Step", self.lineEditStepEnd.text().strip(), float),
        ]

        for field_name, raw_value, expected_type in checks:
            if raw_value == "":
                QMessageBox.warning(self, "Missing field", f"{self.tech}_{self.name}: {field_name} cannot be empty.")
                return False
            try:
                if expected_type is float:
                    float(raw_value)
                elif expected_type is int:
                    int(raw_value)
            except ValueError:
                QMessageBox.warning(self, "Invalid type", f"{self.tech}_{self.name}: {field_name} must be {expected_type.__name__}.")
                return False

        return True

    def outputParam(self) -> dict:
        self._pullFields()  # Ensure model is up-to-date with UI
        if not self._validateParams():
            return {}
        cv_settings = {
            "technique": "cv",
            "name": self.name,
            "Ei": self.ei,
            "E1": self.e1,
            "E2": self.e2,
            "Ef": self.ef,
            "scan_rate": self.scan_rate,
            "scan_number": self.scan_number,
            "record_dE": self.sample_potential,
            "N_cycles": self.repeat,
            "average_dE": self.average,
            "begin_step": self.step_begin,
            "end_step": self.step_end,

            "loop": self.loop # Loop count for this technique (from base class)
        }
        return cv_settings
