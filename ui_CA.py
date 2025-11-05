from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from qt_CA import Ui_Form

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class CA(QWidget, Ui_Form):
    # 1) Signals 
    nameChanged = Signal(str)
    tech="CA"

    def __init__(self, *, i_ranges: list[str] = None, e_ranges: list[str] = None, bandwidths: list[str] = None):
        super().__init__()
        self.setupUi(self)

        # 2) Model defaults
        self.name: str = "CA"
        self.potential: float | int | None = None
        self.ref: str = "RE"
        self.duration: int | float = 0
        self.rate: int | float = 0
        self.ARBegin: int | float = 0
        self.AREnd: int | float = 1
        self.average: int = 1
        self.limitUp: int | float | None = None
        self.limitDown: int | float | None = None
        self.CR: str | None = None       # current range
        self.BW: str | None = None       # bandwidth
        self.PR: str | None = None       # E range 

        # 3) Load combobox options from main UI
        if i_ranges:   self.comboBoxCR.addItems(i_ranges)
        if e_ranges:   self.comboBoxPR.addItems(e_ranges)
        if bandwidths: self.comboBoxBW.addItems(bandwidths)

        # 4) Validators on edits (optional but makes UX nicer)
        self.lineEditDuration.setValidator(QDoubleValidator(self))
        self.lineEditSampleRate.setValidator(QDoubleValidator(self))
        self.lineEditARBegin.setValidator(QDoubleValidator(0.0, 1.0, 2, self))  # 0..1
        self.lineEditAREnd.setValidator(QDoubleValidator(0.0, 1.0, 2, self))    # 0..1
        self.lineEditAverage.setValidator(QIntValidator(1, 10**6, self))        # >=1

        # 5) Bind signals → model updates
        self._bind()

    # ---------------- Binding & helpers ----------------

    def _bind(self):
        # Name
        self.lineEditName.editingFinished.connect(
            lambda: self._set_name(self.lineEditName.text())
        )

        # Scalar fields
        self.lineEditPotential.editingFinished.connect(self._pull_fields)
        self.lineEditDuration.editingFinished.connect(self._pull_fields)
        self.lineEditSampleRate.editingFinished.connect(self._pull_fields)
        self.lineEditARBegin.editingFinished.connect(self._pull_fields)
        self.lineEditAREnd.editingFinished.connect(self._pull_fields)
        self.lineEditAverage.editingFinished.connect(self._pull_fields)
        self.lineEditUpperLimit.editingFinished.connect(self._pull_fields)
        self.lineEditLowerLimit.editingFinished.connect(self._pull_fields)

        # ComboBoxs
        self.comboBoxCR.currentTextChanged.connect(self._pull_fields)
        self.comboBoxPR.currentTextChanged.connect(self._pull_fields)
        self.comboBoxBW.currentTextChanged.connect(self._pull_fields)


    def _set_name(self, new_name: str):
        if new_name and new_name != self.name:
            self.name = new_name
            self.nameChanged.emit(self.name)
            self._emit_payload()

    def _pull_fields(self):
        """Pull current UI values into the model (with light parsing)."""
        try:
            self.potential = _float_or_none(self.lineEditPotential.text())
            self.duration = float(self.lineEditDuration.text() or 0)
            self.rate = float(self.lineEditRate.text() or 0)
            self.ARBegin = float(self.lineEditARBegin.text() or 0)
            self.AREnd = float(self.lineEditAREnd.text() or 1)
            self.average = int(self.lineEditAverage.text() or 1)
            self.limitUp = _float_or_none(self.lineEditUpperLimit.text())
            self.limitDown = _float_or_none(self.lineEditLowerLimit.text())
            self.CR = self.comboBoxCR.currentText() or None
            self.PR = self.comboBoxPR.currentText() or None
            self.BW = self.comboBoxBW.currentText() or None
        except ValueError as e:
            QMessageBox.warning(self, "Parse error", str(e))
            return
        self._emit_payload()

