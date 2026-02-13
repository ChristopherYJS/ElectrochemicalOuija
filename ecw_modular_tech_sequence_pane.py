from PySide6.QtWidgets import QVBoxLayout, QWidget


class TechSequencePane(QWidget):
    def __init__(self, host):
        super().__init__()
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        root_layout.addWidget(host.splitter)
        root_layout.addWidget(host.frame)
