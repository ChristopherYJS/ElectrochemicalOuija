from PySide6.QtCore import Signal

class PSTech():
    nameChanged = Signal(str)
    def __init__(self):
        self.loop = []

class MPTech():
    pass