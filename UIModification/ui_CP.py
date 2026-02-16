from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from misc_BaseTech import PSTech
from UIFiles.qt_CP import Ui_Form

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class CP(QWidget, Ui_Form, PSTech):
    tech="CP"

    def __init__(self, *, i_ranges: list[str] = None):
        super().__init__()
        self.setupUi(self)

        # 2) Model defaults
        self.name: str = "CP"
        self.current: float | int | None = None
        self.duration: int | float = 0
        self.sampleTime: int | float = 0
        self.sampleCurrent: int | float = 0
        self.repeat: int = 1
        self.CR: str | None = None       # current range

        # 3) Load combobox options from main UI
        if i_ranges:
            self._populate_current_ranges(i_ranges)

        # 4) Validators on edits (optional but makes UX nicer)
        self.lineEditCurrent.setValidator(QDoubleValidator(self))
        self.lineEditDuration.setValidator(QDoubleValidator(self))
        self.lineEditSampleTime.setValidator(QDoubleValidator(self))
        self.lineEditSampleCurrent.setValidator(QDoubleValidator(self))
        self.lineEditSampleRepeat.setValidator(QIntValidator(1, 50, self))

        # 5) Bind signals → model updates
        self.bindSignalSlot()

    # ---------------- Binding & helpers ----------------

    def bindSignalSlot(self):
        # Name
        self.lineEditName.editingFinished.connect(self._setName)

        # Scalar fields
        self.lineEditCurrent.editingFinished.connect(self._pullFields)
        self.lineEditDuration.editingFinished.connect(self._pullFields)
        self.lineEditSampleTime.editingFinished.connect(self._pullFields)
        self.lineEditSampleCurrent.editingFinished.connect(self._pullFields)
        self.lineEditSampleRepeat.editingFinished.connect(self._pullFields)

        # ComboBoxs
        self.comboBoxCR.currentTextChanged.connect(self._pullFields)
    def _populate_current_ranges(self, i_ranges):
        self.comboBoxCR.clear()
        for item in i_ranges:
            label = getattr(item, "name", str(item))
            self.comboBoxCR.addItem(label, item)



    def _setName(self):
        self._pullFields()
        
        suffix = (self.name or "").strip()
        label = self.tech if suffix == "" else f"{self.tech}_{suffix}"
        self.nameChanged.emit(label)

    def _pullFields(self):
        """Pull current UI values into the model (with light parsing)."""
        try:
            self.name = self.lineEditName.text()
            self.current = _float_or_none(self.lineEditCurrent.text())
            self.duration = float(self.lineEditDuration.text() or 0)
            self.sampleTime = float(self.lineEditSampleTime.text() or 0)
            self.sampleCurrent = float(self.lineEditSampleCurrent.text() or 0)
            self.repeat = int(self.lineEditSampleRepeat.text() or 1)
            current_data = self.comboBoxCR.currentData()
            self.CR = current_data if current_data is not None else (self.comboBoxCR.currentText() or None)
        except ValueError as e:
            QMessageBox.warning(self, "Parse error", str(e))
            return

    def _validate_before_output(self) -> bool:
        checks = [
            ("Current", self.lineEditCurrent.text().strip(), float),
            ("Duration", self.lineEditDuration.text().strip(), float),
            ("Sample Time", self.lineEditSampleTime.text().strip(), float),
            ("Sample Potential", self.lineEditSampleCurrent.text().strip(), float),
            ("Repeat", self.lineEditSampleRepeat.text().strip(), int),
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
        cp_settings = {
            'technique': 'cp',
            'current': self.current,
            'duration': self.duration,
            'vs_init': False,
            'repeat_count': self.repeat,
            'record_dt': self.sampleTime,
            'record_dE': self.sampleCurrent,
            'i_range': self.CR,
            'timebase': 0.000026,
        }
        return cp_settings
