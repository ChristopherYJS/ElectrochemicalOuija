from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from UIFiles.qt_EIS import Ui_Form
from misc_BaseTech import PSTech

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class EIS(QWidget, Ui_Form, PSTech):
    tech = "EIS"
    
    def __init__(self, *, i_ranges: list[str] = None, e_ranges: list[str] = None):
        super().__init__()
        self.setupUi(self)

        # 2) Model defaults
        self.name: str = "EIS"
        self.potential: float | None = None
        self.duration: int | float = 0
        self.sampleTime: int | float = 0
        self.sampleCurrent: int | float = 0
        self.freqInit: float = 100000  # Initial frequency in Hz
        self.freqFin: float = 0.01  # Final frequency in Hz
        self.sweepLinear: bool = False  # False = logarithmic, True = linear
        self.amplitude: float = 0.01  # AC amplitude in V
        self.number: int = 50  # Number of frequencies
        self.average: int = 1  # Number of averages
        self.correct: bool = False  # Non-stationary correction
        self.correctNum: int = 3  # Number of periods for correction
        self.CR: str | None = None  # current range
        self.ER: str | None = None  # potential range

        # 3) Load combobox options from main UI (if comboboxes exist in future)
        # if i_ranges:   self.comboBoxCR.addItems(i_ranges)
        # if e_ranges:   self.comboBoxER.addItems(e_ranges)

        # 4) Validators on edits
        self.lineEditPotential.setValidator(QDoubleValidator(self))
        self.lineEditDuration.setValidator(QDoubleValidator(self))
        self.lineEditSampleTime.setValidator(QDoubleValidator(self))
        self.lineEditSampleCurrent.setValidator(QDoubleValidator(self))
        self.lineEditFreqInit.setValidator(QDoubleValidator(self))
        self.lineEditFreqFin.setValidator(QDoubleValidator(self))
        self.lineEditAmp.setValidator(QDoubleValidator(self))
        self.lineEditNumber.setValidator(QIntValidator(1, 1000, self))
        self.lineEditAverage.setValidator(QIntValidator(1, 100, self))
        self.lineEditCorrectNum.setValidator(QIntValidator(1, 10, self))

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
        self.lineEditFreqInit.editingFinished.connect(self._pullFields)
        self.lineEditFreqFin.editingFinished.connect(self._pullFields)
        self.lineEditAmp.editingFinished.connect(self._pullFields)
        self.lineEditNumber.editingFinished.connect(self._pullFields)
        self.lineEditAverage.editingFinished.connect(self._pullFields)
        self.lineEditCorrectNum.editingFinished.connect(self._pullFields)

        # Checkboxes
        self.checkBoxSweep.toggled.connect(self._pullFields)
        self.checkBoxCorrect.toggled.connect(self._pullFields)

        # ComboBoxs (if added later)
        # self.comboBoxCR.currentTextChanged.connect(self._pullFields)
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
            self.potential = _float_or_none(self.lineEditPotential.text())
            self.duration = float(self.lineEditDuration.text() or 0)
            self.sampleTime = float(self.lineEditSampleTime.text() or 0)
            self.sampleCurrent = float(self.lineEditSampleCurrent.text() or 0)
            self.freqInit = float(self.lineEditFreqInit.text() or 100000)
            self.freqFin = float(self.lineEditFreqFin.text() or 0.01)
            self.amplitude = float(self.lineEditAmp.text() or 0.01)
            self.number = int(self.lineEditNumber.text() or 50)
            self.average = int(self.lineEditAverage.text() or 1)
            self.correctNum = int(self.lineEditCorrectNum.text() or 3)
            self.sweepLinear = self.checkBoxSweep.isChecked()
            self.correct = self.checkBoxCorrect.isChecked()
            # self.CR = self.comboBoxCR.currentText() or None
            # self.ER = self.comboBoxER.currentText() or None
            # Default ranges if no combobox
            self.CR = "I_RANGE_AUTO"
            self.ER = "E_RANGE_AUTO"

        except ValueError as e:
            QMessageBox.warning(self, "Parse error", str(e))
            return

    def _validate_before_output(self) -> bool:
        checks = [
            ("Potential", self.lineEditPotential.text().strip(), float),
            ("Duration", self.lineEditDuration.text().strip(), float),
            ("Sample Time", self.lineEditSampleTime.text().strip(), float),
            ("Sample Current", self.lineEditSampleCurrent.text().strip(), float),
            ("Initial Frequency", self.lineEditFreqInit.text().strip(), float),
            ("Final Frequency", self.lineEditFreqFin.text().strip(), float),
            ("Amplitude", self.lineEditAmp.text().strip(), float),
            ("Frequency Points", self.lineEditNumber.text().strip(), int),
            ("Average", self.lineEditAverage.text().strip(), int),
            ("Correction Periods", self.lineEditCorrectNum.text().strip(), int),
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
        eis_settings = {
            'technique': 'eis',  # Technique identifier
            'potential': self.potential,  # DC potential in V vs ref
            'duration': self.duration,  # Duration before EIS in s
            'record_dt': self.sampleTime,  # Record at each time increment in s
            'record_dI': self.sampleCurrent,  # Record at each current increment in A
            'freq_init': self.freqInit,  # Initial frequency in Hz
            'freq_final': self.freqFin,  # Final frequency in Hz
            'sweep_linear': self.sweepLinear,  # Linear (True) or logarithmic (False) sweep
            'amplitude': self.amplitude,  # AC amplitude in V
            'freq_number': self.number,  # Number of frequency points
            'average': self.average,  # Number of measurements to average
            'correction': self.correct,  # Enable non-stationary correction
            'correction_periods': self.correctNum,  # Number of periods for correction
            'i_range': self.CR,  # Current range
            'e_range': self.ER,  # Potential range
            'timebase': 0.000026
        }
        return eis_settings
