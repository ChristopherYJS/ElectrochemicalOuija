from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class PotentiostatPane(QWidget):
    def __init__(self, host):
        super().__init__()
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Potentiostat")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.addWidget(title)

        host.potentiostatPanel = QWidget(self)
        host.potentiostatPanel.setObjectName("potentiostatPanel")
        panel_layout = QVBoxLayout(host.potentiostatPanel)
        panel_layout.setContentsMargins(0, 0, 0, 0)

        root_layout.addWidget(host.potentiostatPanel)
