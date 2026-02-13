import os
from typing import Optional, Tuple

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


def get_potentiostat_info_from_dialog(
    parent: QWidget,
    current_address: str,
    current_channel: int,
    current_binary_path: str,
) -> Optional[Tuple[str, int, str]]:
    default_address = "192.168.2.2"
    default_channel = 1
    default_binary_path = os.environ.get("ECLIB_DIR", f"C:{os.sep}EC-Lab Development Package{os.sep}lib")
    dialog = QDialog(parent)
    dialog.setWindowTitle("Potentiostat Info")

    root_layout = QVBoxLayout(dialog)
    form_layout = QFormLayout()

    line_edit_address = QLineEdit(current_address or default_address, dialog)

    spin_box_channel = QSpinBox(dialog)
    spin_box_channel.setRange(0, 64)
    spin_box_channel.setValue(current_channel)

    line_edit_binary_path = QLineEdit(current_binary_path or default_binary_path, dialog)
    push_button_browse = QPushButton("Browse", dialog)

    path_row = QWidget(dialog)
    path_layout = QHBoxLayout(path_row)
    path_layout.setContentsMargins(0, 0, 0, 0)
    path_layout.addWidget(line_edit_binary_path)
    path_layout.addWidget(push_button_browse)

    def choose_binary_path():
        selected_dir = QFileDialog.getExistingDirectory(
            dialog,
            "Select EC-Lab Binary Directory",
            line_edit_binary_path.text() or default_binary_path,
        )
        if selected_dir:
            line_edit_binary_path.setText(selected_dir)

    push_button_browse.clicked.connect(choose_binary_path)

    form_layout.addRow("Address", line_edit_address)
    form_layout.addRow("Channel", spin_box_channel)
    form_layout.addRow("Binary Path", path_row)
    root_layout.addLayout(form_layout)

    button_box = QDialogButtonBox(
        QDialogButtonBox.StandardButton.Ok
        | QDialogButtonBox.StandardButton.Cancel
        | QDialogButtonBox.StandardButton.RestoreDefaults,
        parent=dialog,
    )

    def restore_defaults():
        line_edit_address.setText(default_address)
        spin_box_channel.setValue(default_channel)
        line_edit_binary_path.setText(default_binary_path)

    button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(restore_defaults)
    button_box.accepted.connect(dialog.accept)
    button_box.rejected.connect(dialog.reject)
    root_layout.addWidget(button_box)

    if dialog.exec() == QDialog.DialogCode.Accepted:
        return (
            line_edit_address.text().strip() or default_address,
            spin_box_channel.value(),
            line_edit_binary_path.text().strip() or default_binary_path,
        )

    return None
