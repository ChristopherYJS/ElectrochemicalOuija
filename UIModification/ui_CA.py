from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from UIFiles.qt_CA import Ui_Form
from UIModification.misc_BaseTech import PSTech

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class CA(QWidget, Ui_Form, PSTech):
    tech="CA"
    def __init__(self, *,i_ranges: list[str] | None = None):
        PSTech.__init__(self)
        QWidget.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        # 2) Model defaults
        self.name: str = "CA"
        self.potential: float | int | None = None
        self.duration: int | float = 0

        self.sample_time: int | float = 0
        self.sample_current: int | float = 0
        self.repeat: int = 1
        self.current_range: str | None = None       # current range

        self.lineEditPotential.setText('0.5')
        self.lineEditDuration.setText('10')
        self.lineEditSampleTime.setText('1')
        self.lineEditSampleCurrent.setText('999')
        self.lineEditRepeat.setText('0')
        self.comboBoxCR.setCurrentIndex(12)
        self._pullFields()
        self.lineEditSampleCurrent.setToolTip('set a large value to omit current-based sampling and only sample by time')
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
            self.sample_time = float(self.lineEditSampleTime.text() or 0)
            self.sample_current = float(self.lineEditSampleCurrent.text() or 0)
            self.repeat = int(self.lineEditRepeat.text() or 1)
            current_data = self.comboBoxCR.currentData()
            self.current_range = current_data if current_data is not None else (self.comboBoxCR.currentText() or None)

        except ValueError as e:
            self.validated = False
            QMessageBox.warning(self, "Parse error", str(e))
            return

    def _validateParams(self) -> bool:
        self.validated = False
        checks = [
            ("Potential", self.lineEditPotential.text().strip(), float),
            ("Duration", self.lineEditDuration.text().strip(), float),
            ("Sample Time", self.lineEditSampleTime.text().strip(), float),
            ("Sample Current", self.lineEditSampleCurrent.text().strip(), float),
            ("Repeat", self.lineEditRepeat.text().strip(), int),
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

        self.validated = True
        return True

    def outputParam(self) -> dict | None:
        self._pullFields()  # Ensure model is up-to-date with UI
        self._validateParams()
        if not self.validated:
            return
        """Return current parameters as a dict."""
        ca_settings= { 
            'technique': 'ca', # Technique identifier
            'name': self.name, # User-defined name for this CA step
            'voltage': self.potential, # Voltage applied in V vs ref
            'duration': self.duration, # Duration of CA measurement in s
            'vs_init': False, # Voltage step vs initial one
            'repeat_count': self.repeat, # Repetition of measurement
            'record_dt': self.sample_time, # Record potential at each time increment in s
            'record_dI': self.sample_current, # Record potential at each potential increment in A
            'i_range': self.current_range, # Current range for CA measurement
            'charge': 64, # Record total charge
            'timebase': 0.000026,

            'loop': self.loop # Loop count for this technique (from base class)
        }
        return ca_settings
    
    def setCR(self,i_ranges):
        self.comboBoxCR.clear()
        for item in i_ranges:
            label = getattr(item, "name", str(item))
            self.comboBoxCR.addItem(label, item)
        self.comboBoxCR.setCurrentIndex(len(i_ranges)-1) # Default auto range