from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget


class PlottingPane(QWidget):
    def __init__(self, host):
        super().__init__()
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        root_layout.addWidget(host.graphicsView)

        controls = QWidget(self)
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)

        controls_layout.addWidget(host.labelPlotTech)
        controls_layout.addWidget(host.comboBoxPlotTech)
        controls_layout.addWidget(host.line)
        controls_layout.addWidget(host.labelPlotRepeat)
        controls_layout.addWidget(host.comboBoxPlotRepeat)
        controls_layout.addWidget(host.line_2)
        controls_layout.addWidget(host.labelPlotX)
        controls_layout.addWidget(host.comboBoxPlotX)
        controls_layout.addWidget(host.line_3)
        controls_layout.addWidget(host.labelPlotY)
        controls_layout.addWidget(host.comboBoxPlotY)
        controls_layout.addWidget(host.line_5)
        controls_layout.addWidget(host.labelPlotColor)
        controls_layout.addWidget(host.comboPlotColor)
        controls_layout.addWidget(host.line_4)
        controls_layout.addWidget(host.labelPlotLine)
        controls_layout.addWidget(host.comboBoxPlotLine)
        controls_layout.addWidget(host.line_6)
        controls_layout.addWidget(host.labelPlotScatter)
        controls_layout.addWidget(host.comboBoxPlotScatter)

        root_layout.addWidget(controls)
