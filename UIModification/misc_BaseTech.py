from PySide6.QtCore import Signal


class MOTech():
    def __init__(self):
        self.loop = [1]

class PSTech(MOTech):
    nameChanged = Signal(str)
    def __init__(self):
        super().__init__()

class MPTech(MOTech):
    def __init__(self):
        super().__init__()