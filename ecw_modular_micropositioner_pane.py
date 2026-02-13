from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class MicropositionerPane(QWidget):
    def __init__(self):
        super().__init__()
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(8, 8, 8, 8)

        title = QLabel("Micropositioner")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.addWidget(title)

        placeholder = QLabel("Restyle preview only")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.addWidget(placeholder)
