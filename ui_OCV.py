from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from qt_OCV import Ui_Form
from misc_BaseTech import PSTech

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class OCV(QWidget, Ui_Form, PSTech):
    tech = "OCV"
    
    def __init__(self, *, e_ranges: list[str] = None):
        super().__init__()
        self.setupUi(self)

        # 2) Model defaults
        self.name: str = "OCV"
        self.duration: int | float = 0
        self.sampleTime: int | float = 0
        self.samplePotential: int | float = 0
        self.ER: str | None = None  # potential range (E_RANGE)

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
        self.nameChanged.emit(f'{self.tech}_{self.name}')

    def _pullFields(self):
        """Pull current UI values into the model (with light parsing)."""
        try:
            self.name = self.lineEditName.text()
            self.duration = float(self.lineEditDuration.text() or 0)
            self.sampleTime = float(self.lineEditSampleTime.text() or 0)
            self.samplePotential = float(self.lineEditSampleCurrent.text() or 0)
            # self.ER = self.comboBoxER.currentText() or None
            # Default to E_RANGE_AUTO if no combobox
            self.ER = "E_RANGE_AUTO"

        except ValueError as e:
            QMessageBox.warning(self, "Parse error", str(e))
            return

    def outputParam(self) -> dict:
        self._pullFields()  # Ensure model is up-to-date with UI
        """Return current parameters as a dict."""
        ocv_settings = {
            'technique': 'ocv',  # Technique identifier
            'duration': self.duration,  # Duration of OCV measurement in s
            'record_dt': self.sampleTime,  # Record potential at each time increment in s
            'record_dE': self.samplePotential,  # Record potential at each potential increment in V
            'e_range': self.ER,  # Potential range for OCV measurement
            'timebase': 0.000026
        }
        return ocv_settings
