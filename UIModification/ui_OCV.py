from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from UIFiles.qt_OCV import Ui_Form
from UIModification.misc_BaseTech import PSTech

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class OCV(QWidget, Ui_Form, PSTech):
    tech = "OCV"
    
    def __init__(self, *, e_ranges: list[str] | None = None):
        QWidget.__init__(self)
        PSTech.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        # 2) Model defaults
        self.name: str = "OCV"
        self.duration: int | float = 0
        self.sample_time: int | float = 0
        self.sample_potential: int | float = 0
        self.potential_range: str | None = None  # potential range (E_RANGE)

        self.lineEditSampleCurrent.setToolTip('set a large value to omit potential-based sampling and only sample by time')

        # 3) Load combobox options from main UI (if combobox exists in future)
        # if e_ranges:   self.comboBoxER.addItems(e_ranges)

        # 4) Validators on edits (optional but makes UX nicer)
        self.lineEditDuration.setValidator(QDoubleValidator(self))
        self.lineEditSampleTime.setValidator(QDoubleValidator(self))
        self.lineEditSampleCurrent.setValidator(QDoubleValidator(self))

        # 5) Bind signals → model updates
        self.bindSignalSlot()

    # ---------------- Binding & helpers ----------------

    def bindSignalSlot(self):
        # Name
        self.lineEditName.editingFinished.connect(self._setName)

        # Scalar fields
        self.lineEditDuration.editingFinished.connect(self._pullFields)
        self.lineEditSampleTime.editingFinished.connect(self._pullFields)
        self.lineEditSampleCurrent.editingFinished.connect(self._pullFields)

        # ComboBoxs (if added later)
        # self.comboBoxER.currentTextChanged.connect(self._pullFields)

    def _setName(self):
        self._pullFields()
        suffix = (self.name or "").strip()
        label = self.tech if suffix == "" else f"{self.tech}_{suffix}"
        self.nameChanged.emit(label)

    def _pullFields(self):
        """Pull current UI values into the model (with light parsing)."""
        try:
            self.name = self.lineEditName.text()
            self.duration = float(self.lineEditDuration.text() or 0)
            self.sample_time = float(self.lineEditSampleTime.text() or 0)
            self.sample_potential = float(self.lineEditSampleCurrent.text() or 0)
            # self.ER = self.comboBoxER.currentText() or None
            # Default to E_RANGE_AUTO if no combobox
            self.potential_range = "E_RANGE_AUTO"

        except ValueError as e:
            QMessageBox.warning(self, "Parse error", str(e))
            return

    def _validateParams(self) -> bool:
        checks = [
            ("Duration", self.lineEditDuration.text().strip(), float),
            ("Sample Time", self.lineEditSampleTime.text().strip(), float),
            ("Sample Potential", self.lineEditSampleCurrent.text().strip(), float),
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
        """Return current parameters as a dict."""
        ocv_settings = {
            'technique': 'ocv',  # Technique identifier
            'name': self.name,  # User-defined name for this OCV step
            'duration': self.duration,  # Duration of OCV measurement in s
            'record_dt': self.sample_time,  # Record potential at each time increment in s
            'record_dE': self.sample_potential,  # Record potential at each potential increment in V
            'e_range': self.potential_range,  # Potential range for OCV measurement
            'timebase': 0.000026,

            'loop': self.loop # Loop count for this technique (from base class)
        }
        return ocv_settings
