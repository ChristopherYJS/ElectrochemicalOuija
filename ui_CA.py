from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from qt_CA import Ui_Form
from misc_BaseTech import PSTech

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class CA(QWidget, Ui_Form, PSTech):
    tech = "CA"
    
    def __init__(self, *, i_ranges: list[str] = None):
        super().__init__()
        self.setupUi(self)

        # 2) Model defaults
        self.name: str = "CA"
        self.potential: float | int | None = None
        self.duration: int | float = 0

        self.sampleTime: int | float = 0
        self.sampleCurrent: int | float = 0
        self.repeat: int = 1
        self.CR: str | None = None  # current range

        # 3) Load combobox options from main UI
        if i_ranges:   self.comboBoxCR.addItems(i_ranges)

        # 4) Validators on edits (optional but makes UX nicer)
        self.lineEditPotential.setValidator(QDoubleValidator(self))
        self.lineEditDuration.setValidator(QDoubleValidator(self))
        self.lineEditSampleTime.setValidator(QDoubleValidator(self))
        self.lineEditSampleCurrent.setValidator(QDoubleValidator(self))
        self.lineEditRepeat.setValidator(QIntValidator(1, 50, self))  # >=1

        # 5) Bind signals → model updates
        self.bindSignalSlot()

    # ---------------- Binding & helpers ----------------

    def bindSignalSlot(self):
        # Name
        self.lineEditName.editingFinished.connect(self._setName)

        # Scalar fields
        self.lineEditPotential.editingFinished.connect(self._pullFields)
        self.lineEditDuration.editingFinished.connect(self._pullFields)
        self.lineEditSampleTime.editingFinished.connect(self._pullFields)
        self.lineEditSampleCurrent.editingFinished.connect(self._pullFields)
        self.lineEditRepeat.editingFinished.connect(self._pullFields)

        # ComboBoxs
        self.comboBoxCR.currentTextChanged.connect(self._pullFields)

    def _setName(self):
        self._pullFields()
        suffix = (self.name or "").strip()
        label = self.tech if suffix == "" else f"{self.tech}_{suffix}"
        self.nameChanged.emit(label)


    def _pullFields(self):
        """Pull current UI values into the model (with light parsing)."""
        try:
            self.name = self.lineEditName.text()
            self.potential = _float_or_none(self.lineEditPotential.text())
            self.duration = float(self.lineEditDuration.text() or 0)
            self.sampleTime = float(self.lineEditSampleTime.text() or 0)
            self.sampleCurrent = float(self.lineEditSampleCurrent.text() or 0)
            self.repeat = int(self.lineEditRepeat.text() or 1)
            self.CR = self.comboBoxCR.currentText() or None

        except ValueError as e:
            QMessageBox.warning(self, "Parse error", str(e))
            return

    def _validate_before_output(self) -> bool:
        checks = [
            ("Potential", self.lineEditPotential.text().strip(), float),
            ("Duration", self.lineEditDuration.text().strip(), float),
            ("Sample Time", self.lineEditSampleTime.text().strip(), float),
            ("Sample Current", self.lineEditSampleCurrent.text().strip(), float),
            ("Repeat", self.lineEditRepeat.text().strip(), int),
        ]

        for field_name, raw_value, expected_type in checks:
            if raw_value == "":
                QMessageBox.warning(self, "Missing field", f"{field_name} cannot be empty.")
                return False
            try:
                if expected_type is float:
                    float(raw_value)
                elif expected_type is int:
                    int(raw_value)
            except ValueError:
                QMessageBox.warning(self, "Invalid type", f"{field_name} must be {expected_type.__name__}.")
                return False

        return True

    def outputParam(self) -> dict:
        self._pullFields()  # Ensure model is up-to-date with UI
        if not self._validate_before_output():
            return {}
        """Return current parameters as a dict."""
        ca_settings= { 'technique': 'ca', # Technique identifier
                'voltage': self.potential, # Voltage applied in V vs ref
                'duration': self.duration, # Duration of CA measurement in s
                'vs_init': False, # Voltage step vs initial one
                'repeat_count': self.repeat, # Repetition of measurement
                'record_dt': self.sampleTime, # Record potential at each time increment in s
                'record_dI': self.sampleCurrent, # Record potential at each potential increment in A
                'i_range': self.CR, # Current range for CA measurement
                'charge': 64, # Record total charge
                'timebase': 0.000026
                   }
        return ca_settings