from PySide6.QtWidgets import QGridLayout, QLayout, QWidget

from ecw_modular_log_pane import LogPane
from ecw_modular_micropositioner_pane import MicropositionerPane
from ecw_modular_plotting_pane import PlottingPane
from ecw_modular_potentiostat_pane import PotentiostatPane
from ecw_modular_tech_sequence_pane import TechSequencePane


def _clear_layout(layout: QLayout):
    while layout.count():
        item = layout.takeAt(0)
        child_widget = item.widget()
        child_layout = item.layout()
        if child_widget is not None:
            child_widget.setParent(None)
        elif child_layout is not None:
            _clear_layout(child_layout)


def apply_four_panel_restyle(host):
    _clear_layout(host.horizontalLayoutMain)

    grid_host = QWidget(host.centralwidget)
    grid = QGridLayout(grid_host)
    grid.setContentsMargins(0, 0, 0, 0)

    grid.addWidget(TechSequencePane(host), 0, 0, 2, 1)
    grid.addWidget(PotentiostatPane(host), 0, 1, 1, 1)
    grid.addWidget(MicropositionerPane(), 1, 1, 1, 1)
    grid.addWidget(PlottingPane(host), 0, 2, 1, 1)
    grid.addWidget(LogPane(host), 1, 2, 1, 1)

    grid.setColumnStretch(0, 2)
    grid.setColumnStretch(1, 3)
    grid.setColumnStretch(2, 3)
    grid.setRowStretch(0, 3)
    grid.setRowStretch(1, 2)

    host.horizontalLayoutMain.addWidget(grid_host)
    host._four_panel_main_widget = grid_host
