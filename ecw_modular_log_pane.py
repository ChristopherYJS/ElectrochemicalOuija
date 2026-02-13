from PySide6.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget


class LogPane(QWidget):
    def __init__(self, host):
        super().__init__()
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        if not hasattr(host, "Log") or host.Log is None:
            host.Log = QPlainTextEdit()
            host.Log.setReadOnly(True)

        root_layout.addWidget(host.Log)
