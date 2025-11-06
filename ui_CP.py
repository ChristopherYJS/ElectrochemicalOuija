from __future__ import annotations
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from qt_CP import Ui_Form

def _float_or_none(text: str) -> float | None:
    t = text.strip()
    if t == "" or t.lower() == "none":
        return None
    return float(t)

class CP(QWidget, Ui_Form):
    # 1) Signals 
    nameChanged = Signal(str)
    tech="CP"

    def __init__(self, *, i_ranges: list[str] = None, e_ranges: list[str] = None, bandwidths: list[str] = None):
        super().__init__()
        self.setupUi(self)

        # 2) Model defaults
        self.name: str = "CP"
        self.current: float | int | None = None
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
        self.bindSignalSlot()

    # ---------------- Binding & helpers ----------------

    def bindSignalSlot(self):
        # Name
        self.lineEditName.editingFinished.connect(self._setName)

        # Scalar fields
        self.lineEditCurrent.editingFinished.connect(self._pullFields)
        self.lineEditDuration.editingFinished.connect(self._pullFields)
        self.lineEditSampleRate.editingFinished.connect(self._pullFields)
        self.lineEditARBegin.editingFinished.connect(self._pullFields)
        self.lineEditAREnd.editingFinished.connect(self._pullFields)
        self.lineEditAverage.editingFinished.connect(self._pullFields)
        self.lineEditUpperLimit.editingFinished.connect(self._pullFields)
        self.lineEditLowerLimit.editingFinished.connect(self._pullFields)

        # ComboBoxs
        self.comboBoxCR.currentTextChanged.connect(self._pullFields)
        self.comboBoxPR.currentTextChanged.connect(self._pullFields)
        self.comboBoxBW.currentTextChanged.connect(self._pullFields)


    def _setName(self):
        self._pullFields()
        
        self.nameChanged.emit(f'{self.tech}_{self.name}')


    def _pullFields(self):
        """Pull current UI values into the model (with light parsing)."""
        try:
            self.name=self.lineEditName.text()
            self.current = _float_or_none(self.lineEditCurrent.text())
            self.duration = float(self.lineEditDuration.text() or 0)
            self.rate = float(self.lineEditSampleRate.text() or 0)
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
