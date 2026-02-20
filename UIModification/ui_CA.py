from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from UIFiles.qt_CA import Ui_Form
from misc_BaseTech import PSTech

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class CA(QWidget, Ui_Form, PSTech):
    tech="CA"
    def __init__(self, *,i_ranges: list[str] = None):
        super().__init__()
        self.setupUi(self)

        # 2) Model defaults
        self.name: str = "CA"
        self.potential: float | int | None = None
        self.duration: int | float = 0

        self.sampleTime: int | float = 0
        self.sampleCurrent: int | float = 0
        self.repeat: int = 1
        self.CR: str | None = None       # current range


        # 3) Load combobox options from main UI
        if i_ranges:   self.comboBoxCR.addItems(i_ranges)

        # 4) Validators on edits (optional but makes UX nicer)
        if i_ranges:
            self.setCR(i_ranges)
        self.lineEditDuration.setValidator(QDoubleValidator(self))
        self.lineEditSampleTime.setValidator(QDoubleValidator(self))
        self.lineEditSampleCurrent.setValidator(QDoubleValidator(self))
        self.lineEditRepeat.setValidator(QIntValidator(1, 50, self))        # >=1

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
        self.nameChanged.emit(f'{self.tech}_{self.name}')


    def _pullFields(self):
        """Pull current UI values into the model (with light parsing)."""
        try:
            self.name=self.lineEditName.text()
            self.potential = _float_or_none(self.lineEditPotential.text())
            self.duration = float(self.lineEditDuration.text() or 0)
            self.sampleTime = float(self.lineEditSampleTime.text() or 0)
            self.sampleCurrent = float(self.lineEditSampleCurrent.text() or 0)
            self.repeat = int(self.lineEditRepeat.text() or 1)
            current_data = self.comboBoxCR.currentData()
            self.CR = current_data if current_data is not None else (self.comboBoxCR.currentText() or None)

        except ValueError as e:
            QMessageBox.warning(self, "Parse error", str(e))
            return

    def outputParam(self) -> dict:
        self._pullFields()  # Ensure model is up-to-date with UI
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
    
    def setCR(self,i_ranges):
        self.comboBoxCR.clear()
        for item in i_ranges:
            label = getattr(item, "name", str(item))
            self.comboBoxCR.addItem(label, item)