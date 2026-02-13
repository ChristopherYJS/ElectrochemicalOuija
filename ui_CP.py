from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from misc_BaseTech import PSTech
from qt_CP import Ui_Form

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class CP(QWidget, Ui_Form, PSTech):
    tech = "CP"

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
        self.CR: str | None = None  # current range

        # 3) Load combobox options from main UI
        if i_ranges:   self.comboBoxCR.addItems(i_ranges)

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

    def _setName(self):
        self._pullFields()
        self.nameChanged.emit(f'{self.tech}_{self.name}')

    def _pullFields(self):
        """Pull current UI values into the model (with light parsing)."""
        try:
            self.name = self.lineEditName.text()
            self.current = _float_or_none(self.lineEditCurrent.text())
            self.duration = float(self.lineEditDuration.text() or 0)
            self.sampleTime = float(self.lineEditSampleTime.text() or 0)
            self.sampleCurrent = float(self.lineEditSampleCurrent.text() or 0)
            self.repeat = int(self.lineEditSampleRepeat.text() or 1)
            self.CR = self.comboBoxCR.currentText() or None
        except ValueError as e:
            QMessageBox.warning(self, "Parse error", str(e))
            return

    def outputParam(self) -> dict:
        self._pullFields()  # Ensure model is up-to-date with UI
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
