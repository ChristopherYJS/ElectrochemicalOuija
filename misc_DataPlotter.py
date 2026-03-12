import csv
import os

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPen, QPolygonF, QWheelEvent
from PySide6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class SimpleLinePlot(QWidget):
    cursorChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._segments = []
        self._x_label = ""
        self._y_label = ""
        self._message = "Select a data file to plot."
        self._data_bounds = None
        self._view_bounds = None
        self._plot_rect = QRectF()
        self._hover_info = None
        self._last_pan_pos = None
        self._pan_mode = False
        self._cursor_enabled = True

        self.setMouseTracking(True)
        self.setMinimumHeight(360)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def clearPlot(self, message: str = "No data available."):
        self._segments = []
        self._x_label = ""
        self._y_label = ""
        self._message = message
        self._data_bounds = None
        self._view_bounds = None
        self._hover_info = None
        self.cursorChanged.emit("Cursor: idle")
        self.update()

    def setPlotData(self, segments, x_label: str, y_label: str, reset_view: bool = False):
        self._segments = list(segments)
        self._x_label = x_label
        self._y_label = y_label
        self._message = ""
        self._data_bounds = self._computeDataBounds()

        if self._data_bounds is None:
            self._view_bounds = None
        elif reset_view or self._view_bounds is None:
            self._view_bounds = list(self._data_bounds)

        self._hover_info = None
        self.cursorChanged.emit("Cursor: hover over a trace")
        self.update()

    def setPanMode(self, enabled: bool):
        self._pan_mode = enabled
        self._last_pan_pos = None
        self.setCursor(Qt.CursorShape.OpenHandCursor if enabled else Qt.CursorShape.CrossCursor)

    def setCursorEnabled(self, enabled: bool):
        self._cursor_enabled = enabled
        if not enabled:
            self._hover_info = None
            self.cursorChanged.emit("Cursor: disabled")
            self.update()

    def resetView(self):
        if self._data_bounds is None:
            return
        self._view_bounds = list(self._data_bounds)
        self._hover_info = None
        self.update()

    def zoomByFactor(self, factor: float):
        if self._plot_rect.isEmpty():
            return
        self._zoomAt(self._plot_rect.center(), factor)

    def paintEvent(self, event):
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))

        bounds = self.rect().adjusted(12, 12, -12, -12)
        painter.setPen(QPen(QColor("#d9dde3"), 1))
        painter.drawRect(bounds)

        if not self._segments or self._view_bounds is None:
            painter.setPen(QColor("#667085"))
            painter.drawText(bounds, Qt.AlignmentFlag.AlignCenter, self._message)
            return

        left_margin = 60
        right_margin = 18
        top_margin = 18
        bottom_margin = 42
        self._plot_rect = QRectF(bounds.adjusted(left_margin, top_margin, -right_margin, -bottom_margin))
        if self._plot_rect.width() <= 0 or self._plot_rect.height() <= 0:
            return

        x_min, x_max, y_min, y_max = self._view_bounds
        self._drawGrid(painter, x_min, x_max, y_min, y_max)

        painter.save()
        painter.setClipRect(self._plot_rect)
        for segment in self._segments:
            points = []
            for x_value, y_value in zip(segment["x"], segment["y"]):
                if x_value < x_min or x_value > x_max or y_value < y_min or y_value > y_max:
                    points.append(None)
                    continue
                points.append(self._mapDataToPlot(x_value, y_value))

            painter.setPen(QPen(segment["color"], 2))
            self._drawSegmentPolyline(painter, points)
        painter.restore()

        painter.setPen(QColor("#101828"))
        painter.drawText(self._plot_rect.adjusted(0, 0, 0, bottom_margin - 10), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, self._x_label)

        painter.save()
        painter.translate(bounds.left() + 18, self._plot_rect.center().y())
        painter.rotate(-90)
        painter.drawText(0, 0, self._y_label)
        painter.restore()

        painter.setPen(QColor("#475467"))
        painter.drawText(bounds.adjusted(4, 2, -4, -2), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft, f"{self._x_label}: {x_min:.4g} to {x_max:.4g}")
        painter.drawText(bounds.adjusted(4, 2, -4, -2), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight, f"{self._y_label}: {y_min:.4g} to {y_max:.4g}")

        if self._cursor_enabled and self._hover_info is not None:
            self._drawCursor(painter)

    def wheelEvent(self, event: QWheelEvent):
        if self._view_bounds is None or not self._plot_rect.contains(event.position()):
            event.ignore()
            return
        factor = 0.85 if event.angleDelta().y() > 0 else 1.15
        self._zoomAt(event.position(), factor)
        event.accept()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self._pan_mode and self._plot_rect.contains(event.position()):
            self._last_pan_pos = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._pan_mode and self._last_pan_pos is not None and self._view_bounds is not None:
            delta = event.position() - self._last_pan_pos
            self._last_pan_pos = event.position()
            x_min, x_max, y_min, y_max = self._view_bounds
            x_shift = -(delta.x() / max(self._plot_rect.width(), 1.0)) * (x_max - x_min)
            y_shift = (delta.y() / max(self._plot_rect.height(), 1.0)) * (y_max - y_min)
            self._view_bounds = [x_min + x_shift, x_max + x_shift, y_min + y_shift, y_max + y_shift]
            self.update()
            event.accept()
            return

        if self._cursor_enabled and self._plot_rect.contains(event.position()):
            self._hover_info = self._findNearestPoint(event.position())
            if self._hover_info is not None:
                cycle_text = f" | cycle {self._hover_info['cycle']}" if self._hover_info["cycle"] else ""
                self.cursorChanged.emit(f"Cursor: x={self._hover_info['x']:.6g}, y={self._hover_info['y']:.6g}{cycle_text}")
            else:
                self.cursorChanged.emit("Cursor: hover over a trace")
            self.update()
        else:
            self._hover_info = None
            if self._cursor_enabled:
                self.cursorChanged.emit("Cursor: hover over a trace")
            self.update()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self._pan_mode:
            self._last_pan_pos = None
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def leaveEvent(self, event):
        self._hover_info = None
        self._last_pan_pos = None
        if self._cursor_enabled:
            self.cursorChanged.emit("Cursor: hover over a trace")
        if self._pan_mode:
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.update()
        super().leaveEvent(event)

    def _computeDataBounds(self):
        x_values = []
        y_values = []
        for segment in self._segments:
            x_values.extend(segment["x"])
            y_values.extend(segment["y"])
        if not x_values or not y_values:
            return None

        x_min = min(x_values)
        x_max = max(x_values)
        y_min = min(y_values)
        y_max = max(y_values)
        if x_min == x_max:
            x_min -= 0.5
            x_max += 0.5
        if y_min == y_max:
            y_min -= 0.5
            y_max += 0.5
        return [x_min, x_max, y_min, y_max]

    def _drawGrid(self, painter: QPainter, x_min: float, x_max: float, y_min: float, y_max: float):
        painter.setPen(QPen(QColor("#d0d5dd"), 1, Qt.PenStyle.DotLine))
        for step in range(1, 5):
            x = self._plot_rect.left() + (self._plot_rect.width() * step / 5)
            y = self._plot_rect.top() + (self._plot_rect.height() * step / 5)
            painter.drawLine(int(x), int(self._plot_rect.top()), int(x), int(self._plot_rect.bottom()))
            painter.drawLine(int(self._plot_rect.left()), int(y), int(self._plot_rect.right()), int(y))

        painter.setPen(QPen(QColor("#344054"), 1.4))
        painter.drawLine(self._plot_rect.bottomLeft(), self._plot_rect.topLeft())
        painter.drawLine(self._plot_rect.bottomLeft(), self._plot_rect.bottomRight())

        painter.setPen(QColor("#667085"))
        for step in range(0, 6):
            x_value = x_min + ((x_max - x_min) * step / 5)
            y_value = y_max - ((y_max - y_min) * step / 5)
            x_pos = self._plot_rect.left() + (self._plot_rect.width() * step / 5)
            y_pos = self._plot_rect.top() + (self._plot_rect.height() * step / 5)
            painter.drawText(QRectF(x_pos - 35, self._plot_rect.bottom() + 4, 70, 18), Qt.AlignmentFlag.AlignHCenter, f"{x_value:.4g}")
            painter.drawText(QRectF(self._plot_rect.left() - 56, y_pos - 9, 48, 18), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"{y_value:.4g}")

    def _drawSegmentPolyline(self, painter: QPainter, points):
        current = []
        for point in points:
            if point is None:
                if len(current) == 1:
                    painter.drawPoint(current[0])
                elif len(current) > 1:
                    painter.drawPolyline(QPolygonF(current))
                current = []
                continue
            current.append(point)
        if len(current) == 1:
            painter.drawPoint(current[0])
        elif len(current) > 1:
            painter.drawPolyline(QPolygonF(current))

    def _drawCursor(self, painter: QPainter):
        if self._hover_info is None:
            return
        plot_pos = self._hover_info["plot_pos"]
        painter.setPen(QPen(QColor("#98a2b3"), 1, Qt.PenStyle.DashLine))
        painter.drawLine(int(plot_pos.x()), int(self._plot_rect.top()), int(plot_pos.x()), int(self._plot_rect.bottom()))
        painter.drawLine(int(self._plot_rect.left()), int(plot_pos.y()), int(self._plot_rect.right()), int(plot_pos.y()))

        painter.setPen(QPen(self._hover_info["color"], 2))
        painter.setBrush(self._hover_info["color"])
        painter.drawEllipse(plot_pos, 4, 4)

    def _mapDataToPlot(self, x_value: float, y_value: float):
        if self._view_bounds is None:
            return QPointF()
        x_min, x_max, y_min, y_max = self._view_bounds
        x_ratio = (x_value - x_min) / (x_max - x_min)
        y_ratio = (y_value - y_min) / (y_max - y_min)
        x_pos = self._plot_rect.left() + (x_ratio * self._plot_rect.width())
        y_pos = self._plot_rect.bottom() - (y_ratio * self._plot_rect.height())
        return QPointF(x_pos, y_pos)

    def _mapPlotToData(self, plot_pos: QPointF):
        if self._view_bounds is None:
            return 0.0, 0.0
        x_min, x_max, y_min, y_max = self._view_bounds
        x_ratio = (plot_pos.x() - self._plot_rect.left()) / max(self._plot_rect.width(), 1.0)
        y_ratio = (self._plot_rect.bottom() - plot_pos.y()) / max(self._plot_rect.height(), 1.0)
        x_value = x_min + (x_ratio * (x_max - x_min))
        y_value = y_min + (y_ratio * (y_max - y_min))
        return x_value, y_value

    def _zoomAt(self, anchor_pos: QPointF, factor: float):
        if self._view_bounds is None:
            return
        x_value, y_value = self._mapPlotToData(anchor_pos)
        x_min, x_max, y_min, y_max = self._view_bounds
        x_range = max((x_max - x_min) * factor, 1e-12)
        y_range = max((y_max - y_min) * factor, 1e-12)
        x_anchor_ratio = (anchor_pos.x() - self._plot_rect.left()) / max(self._plot_rect.width(), 1.0)
        y_anchor_ratio = (self._plot_rect.bottom() - anchor_pos.y()) / max(self._plot_rect.height(), 1.0)

        new_x_min = x_value - (x_range * x_anchor_ratio)
        new_x_max = new_x_min + x_range
        new_y_min = y_value - (y_range * y_anchor_ratio)
        new_y_max = new_y_min + y_range
        self._view_bounds = [new_x_min, new_x_max, new_y_min, new_y_max]
        self.update()

    def _findNearestPoint(self, cursor_pos: QPointF):
        nearest = None
        nearest_distance_sq = 18.0 * 18.0
        for segment in self._segments:
            for x_value, y_value in zip(segment["x"], segment["y"]):
                if self._view_bounds is None:
                    continue
                x_min, x_max, y_min, y_max = self._view_bounds
                if x_value < x_min or x_value > x_max or y_value < y_min or y_value > y_max:
                    continue
                plot_pos = self._mapDataToPlot(x_value, y_value)
                dx = plot_pos.x() - cursor_pos.x()
                dy = plot_pos.y() - cursor_pos.y()
                distance_sq = (dx * dx) + (dy * dy)
                if distance_sq > nearest_distance_sq:
                    continue
                nearest_distance_sq = distance_sq
                nearest = {
                    "x": x_value,
                    "y": y_value,
                    "cycle": segment["cycle_label"],
                    "plot_pos": plot_pos,
                    "color": segment["color"],
                }
        return nearest


class DataPlotterWidget(QWidget):
    statusChanged = Signal(str)
    liveInfoChanged = Signal(str)
    cursorInfoChanged = Signal(str)

    COLOR_MAPS = {
        "Viridis": ["#440154", "#414487", "#2a788e", "#22a884", "#7ad151", "#fde725"],
        "Plasma": ["#0d0887", "#6a00a8", "#b12a90", "#e16462", "#fca636", "#f0f921"],
        "Turbo": ["#30123b", "#4145ab", "#2ab0ff", "#3edc81", "#f9f721", "#f58b1f", "#7a0403"],
        "Warm": ["#7f3b08", "#b35806", "#e08214", "#fdb863", "#fee0b6"],
        "Cool": ["#3b4cc0", "#688aef", "#98c1ff", "#d1e5f0", "#fddbc7", "#f4a582", "#d6604d"],
        "Set1": ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf"],
        "Monochrome": ["#1565c0"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = ""
        self.headers = []
        self.rows = []
        self.file_mtime = None
        self.file_size = None
        self.live_metadata = {}
        self.cycle_color_overrides = {}
        self.status_text = "Load a delimited text file with column titles."
        self.live_text = "Idle"
        self.cursor_text = "Cursor: idle"

        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(1000)
        self.refresh_timer.timeout.connect(self._refreshFromTimer)

        layout = QVBoxLayout(self)

        title_label = QLabel("Data Plotter")
        title_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        layout.addWidget(title_label)

        controls_layout = QHBoxLayout()
        self.button_select_file = QPushButton("Select File")
        self.button_select_file.clicked.connect(self.selectFile)
        controls_layout.addWidget(self.button_select_file)

        self.label_file = QLabel("No file selected")
        self.label_file.setWordWrap(True)
        controls_layout.addWidget(self.label_file, 1)
        layout.addLayout(controls_layout)

        live_layout = QHBoxLayout()
        self.check_follow_running = QCheckBox("Follow running tech")
        self.check_follow_running.setChecked(True)
        self.check_follow_running.toggled.connect(self._updateTimerState)
        live_layout.addWidget(self.check_follow_running)

        self.check_live_refresh = QCheckBox("Live refresh")
        self.check_live_refresh.setChecked(True)
        self.check_live_refresh.toggled.connect(self._updateTimerState)
        live_layout.addWidget(self.check_live_refresh)

        live_layout.addWidget(QLabel("Refresh ms"))
        self.spin_refresh_ms = QSpinBox()
        self.spin_refresh_ms.setRange(250, 10000)
        self.spin_refresh_ms.setSingleStep(250)
        self.spin_refresh_ms.setValue(1000)
        self.spin_refresh_ms.valueChanged.connect(self.refresh_timer.setInterval)
        live_layout.addWidget(self.spin_refresh_ms)
        live_layout.addStretch(1)
        layout.addLayout(live_layout)

        axis_layout = QHBoxLayout()
        self.combo_x = QComboBox()
        self.combo_y = QComboBox()
        self.combo_cycle = QComboBox()
        self.combo_x.currentIndexChanged.connect(self.refreshPlot)
        self.combo_y.currentIndexChanged.connect(self.refreshPlot)
        self.combo_cycle.currentIndexChanged.connect(self.refreshPlot)
        axis_layout.addWidget(QLabel("X Axis"))
        axis_layout.addWidget(self.combo_x, 1)
        axis_layout.addWidget(QLabel("Y Axis"))
        axis_layout.addWidget(self.combo_y, 1)
        axis_layout.addWidget(QLabel("Cycle Column"))
        axis_layout.addWidget(self.combo_cycle, 1)
        layout.addLayout(axis_layout)

        self.plot_widget = SimpleLinePlot()

        tool_layout = QHBoxLayout()
        self.button_zoom_in = QPushButton("Zoom In")
        self.button_zoom_in.clicked.connect(lambda: self.plot_widget.zoomByFactor(0.85))
        tool_layout.addWidget(self.button_zoom_in)

        self.button_zoom_out = QPushButton("Zoom Out")
        self.button_zoom_out.clicked.connect(lambda: self.plot_widget.zoomByFactor(1.15))
        tool_layout.addWidget(self.button_zoom_out)

        self.button_reset_zoom = QPushButton("Reset View")
        self.button_reset_zoom.clicked.connect(self.plot_widget.resetView)
        tool_layout.addWidget(self.button_reset_zoom)

        self.check_pan = QCheckBox("Pan")
        self.check_pan.toggled.connect(self.plot_widget.setPanMode)
        tool_layout.addWidget(self.check_pan)

        self.check_cursor = QCheckBox("Cursor")
        self.check_cursor.setChecked(True)
        self.check_cursor.toggled.connect(self.plot_widget.setCursorEnabled)
        tool_layout.addWidget(self.check_cursor)

        tool_layout.addStretch(1)
        layout.addLayout(tool_layout)

        color_layout = QHBoxLayout()
        self.combo_colormap = QComboBox()
        self.combo_colormap.addItems(list(self.COLOR_MAPS.keys()))
        self.combo_colormap.currentIndexChanged.connect(self.refreshPlot)
        color_layout.addWidget(QLabel("Color Map"))
        color_layout.addWidget(self.combo_colormap, 1)

        self.combo_cycle_color_target = QComboBox()
        self.combo_cycle_color_target.currentIndexChanged.connect(self._updateColorButtonText)
        color_layout.addWidget(QLabel("Color Target"))
        color_layout.addWidget(self.combo_cycle_color_target, 1)

        self.button_pick_color = QPushButton("Set Color")
        self.button_pick_color.clicked.connect(self._pickCycleColor)
        color_layout.addWidget(self.button_pick_color)

        self.button_clear_color = QPushButton("Clear Override")
        self.button_clear_color.clicked.connect(self._clearCycleColorOverride)
        color_layout.addWidget(self.button_clear_color)
        layout.addLayout(color_layout)

        layout.addWidget(self.plot_widget, 1)

        self.plot_widget.cursorChanged.connect(self._setCursorText)

        self._setSelectorsEnabled(False)
        self._setColorTargets(["All data"])
        self._updateColorButtonText()
        self._setStatusText(self.status_text)
        self._setLiveText(self.live_text)
        self._setCursorText(self.cursor_text)
        self._updateTimerState()

    def _setSelectorsEnabled(self, enabled: bool):
        self.combo_x.setEnabled(enabled)
        self.combo_y.setEnabled(enabled)
        self.combo_cycle.setEnabled(enabled)
        self.combo_colormap.setEnabled(enabled)
        self.combo_cycle_color_target.setEnabled(enabled)
        self.button_pick_color.setEnabled(enabled)
        self.button_clear_color.setEnabled(enabled)

    def selectFile(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Data File",
            "",
            "Data Files (*.csv *.txt *.dat *.tsv);;All Files (*.*)",
        )
        if not file_path:
            return
        self.live_metadata = {}
        self.loadFile(file_path)
        self._setLiveText("Manual file selected")
        self._updateTimerState()

    def loadFile(self, file_path: str, preserve_axes: bool = True):
        previous_x = self.combo_x.currentText() if preserve_axes else ""
        previous_y = self.combo_y.currentText() if preserve_axes else ""
        previous_cycle = self.combo_cycle.currentText() if preserve_axes else ""
        try:
            headers, rows = self._readDelimitedFile(file_path)
        except Exception as ex:
            self.file_path = ""
            self.headers = []
            self.rows = []
            self.file_mtime = None
            self.file_size = None
            self.label_file.setText("No file selected")
            self._setStatusText(f"Unable to read file: {ex}")
            self._setSelectorsEnabled(False)
            self.combo_x.clear()
            self.combo_y.clear()
            self.combo_cycle.clear()
            self._setColorTargets(["All data"])
            self.plot_widget.clearPlot("Unable to load selected file.")
            return

        self.file_path = file_path
        self.headers = headers
        self.rows = rows
        self._updateFileSnapshot()
        self.label_file.setText(os.path.basename(file_path))

        self.combo_x.blockSignals(True)
        self.combo_y.blockSignals(True)
        self.combo_cycle.blockSignals(True)
        self.combo_x.clear()
        self.combo_y.clear()
        self.combo_cycle.clear()
        self.combo_x.addItems(headers)
        self.combo_y.addItems(headers)
        self.combo_cycle.addItem("None")
        self.combo_cycle.addItems(headers)

        if headers:
            self.combo_x.setCurrentIndex(0)
            self.combo_y.setCurrentIndex(1 if len(headers) > 1 else 0)
            self.combo_cycle.setCurrentIndex(0)

        self._restoreAxisSelection(previous_x, previous_y, previous_cycle)
        self._applyPreferredSelections()

        self.combo_x.blockSignals(False)
        self.combo_y.blockSignals(False)
        self.combo_cycle.blockSignals(False)
        self._setSelectorsEnabled(bool(headers))
        self.refreshPlot()

    def setLiveSource(self, file_path: str, metadata: dict | None = None):
        if metadata is not None:
            self.live_metadata = dict(metadata)
        if not file_path:
            self._updateTimerState()
            return

        if self.check_follow_running.isChecked() and file_path != self.file_path:
            self.loadFile(file_path, preserve_axes=True)

        if self.live_metadata:
            channel = self.live_metadata.get("channel", "?")
            technique = self.live_metadata.get("technique", "")
            name = self.live_metadata.get("name", "")
            status = self.live_metadata.get("status", "")
            tech_index = self.live_metadata.get("tech_index", "")
            details = f"Live source: CH {channel}"
            if technique:
                details += f" | {technique}"
            if name:
                details += f"_{name}"
            if tech_index != "":
                details += f" | seq {tech_index}"
            if status:
                details += f" | {status}"
            self._setLiveText(details)

        self._updateTimerState()

    def pauseLiveRefresh(self):
        self.refresh_timer.stop()

    def clearLiveSource(self, message: str = "Idle", clear_plot: bool = False):
        self.live_metadata = {}
        self._setLiveText(message)
        if clear_plot:
            self.file_path = ""
            self.headers = []
            self.rows = []
            self.file_mtime = None
            self.file_size = None
            self.label_file.setText("No file selected")
            self._setStatusText("Select a data file to plot.")
            self.combo_x.clear()
            self.combo_y.clear()
            self.combo_cycle.clear()
            self._setColorTargets(["All data"])
            self.plot_widget.clearPlot("Select a data file to plot.")
            self._setSelectorsEnabled(False)
        self._updateTimerState()

    def refreshPlot(self):
        if not self.headers or not self.rows:
            self._setStatusText("Load a delimited text file with column titles.")
            self.plot_widget.clearPlot("Select a data file to plot.")
            self._setColorTargets(["All data"])
            return

        x_index = self.combo_x.currentIndex()
        y_index = self.combo_y.currentIndex()
        cycle_index = self.combo_cycle.currentIndex() - 1

        if x_index < 0 or y_index < 0:
            self._setStatusText("Select both X and Y axis columns.")
            self.plot_widget.clearPlot("Select X and Y axis data.")
            return

        grouped_segments = []
        cycle_values = []
        current_segment = None
        skipped_rows = 0

        for row in self.rows:
            if x_index >= len(row) or y_index >= len(row):
                skipped_rows += 1
                continue
            x_value = self._toFloat(row[x_index])
            y_value = self._toFloat(row[y_index])
            if x_value is None or y_value is None:
                skipped_rows += 1
                continue

            cycle_label = ""
            if cycle_index >= 0 and cycle_index < len(row):
                cycle_label = self._formatCycleValue(row[cycle_index])

            if current_segment is None or current_segment["cycle_label"] != cycle_label:
                current_segment = {"cycle_label": cycle_label, "x": [], "y": []}
                grouped_segments.append(current_segment)
                if cycle_label and cycle_label not in cycle_values:
                    cycle_values.append(cycle_label)

            current_segment["x"].append(x_value)
            current_segment["y"].append(y_value)

        x_label = self.headers[x_index]
        y_label = self.headers[y_index]
        if not grouped_segments:
            self._setStatusText(f"No numeric rows available for {x_label} vs {y_label}.")
            self.plot_widget.clearPlot("No numeric data available for the selected axes.")
            self._setColorTargets(["All data"])
            return

        colors_by_cycle = self._buildColors(cycle_values if cycle_values else ["All data"])
        segments = []
        for index, segment in enumerate(grouped_segments):
            cycle_label = segment["cycle_label"] or "All data"
            color = colors_by_cycle.get(cycle_label, self._paletteColor(index))
            segments.append(
                {
                    "cycle_label": segment["cycle_label"],
                    "x": segment["x"],
                    "y": segment["y"],
                    "color": color,
                }
            )

        self.plot_widget.setPlotData(segments, x_label, y_label)
        target_items = cycle_values if cycle_values else ["All data"]
        self._setColorTargets(target_items)
        self._setStatusText(
            f"Plotting {sum(len(segment['x']) for segment in segments)} rows from {os.path.basename(self.file_path)}"
            + (f" | {len(target_items)} cycle groups" if cycle_values else "")
            + (f" | {skipped_rows} skipped" if skipped_rows else "")
        )

    def _updateTimerState(self):
        is_live_run = bool(self.live_metadata) and self.live_metadata.get("status") != "STOP"
        should_run = bool(self.file_path) and self.check_live_refresh.isChecked() and is_live_run
        if should_run:
            self.refresh_timer.start(self.spin_refresh_ms.value())
        else:
            self.refresh_timer.stop()

    def _refreshFromTimer(self):
        if not self.file_path or not os.path.exists(self.file_path):
            return
        if not self._hasFileChanged():
            return
        try:
            self.loadFile(self.file_path, preserve_axes=True)
            if self.live_metadata:
                self._setLiveText(self.live_text.split(" | updated")[0] + " | updated")
        except Exception as ex:
            self._setLiveText(f"Live refresh waiting: {ex}")

    def _setStatusText(self, text: str):
        self.status_text = text
        self.statusChanged.emit(text)

    def _setLiveText(self, text: str):
        self.live_text = text
        self.liveInfoChanged.emit(text)

    def _setCursorText(self, text: str):
        self.cursor_text = text
        self.cursorInfoChanged.emit(text)

    def _updateFileSnapshot(self):
        if not self.file_path or not os.path.exists(self.file_path):
            self.file_mtime = None
            self.file_size = None
            return
        stat_result = os.stat(self.file_path)
        self.file_mtime = stat_result.st_mtime
        self.file_size = stat_result.st_size

    def _hasFileChanged(self):
        if not self.file_path or not os.path.exists(self.file_path):
            return False
        stat_result = os.stat(self.file_path)
        return stat_result.st_mtime != self.file_mtime or stat_result.st_size != self.file_size

    def _restoreAxisSelection(self, previous_x: str, previous_y: str, previous_cycle: str):
        if previous_x:
            index_x = self.combo_x.findText(previous_x)
            if index_x >= 0:
                self.combo_x.setCurrentIndex(index_x)
        if previous_y:
            index_y = self.combo_y.findText(previous_y)
            if index_y >= 0:
                self.combo_y.setCurrentIndex(index_y)
        if previous_cycle:
            index_cycle = self.combo_cycle.findText(previous_cycle)
            if index_cycle >= 0:
                self.combo_cycle.setCurrentIndex(index_cycle)

    def _applyPreferredSelections(self):
        if not self.combo_x.currentText() or self.combo_x.currentIndex() == 0:
            self._setComboToPreferred(self.combo_x, ["t", "time", "freq", "frequency", "Ewe"])
        if (
            not self.combo_y.currentText()
            or self.combo_y.currentText() == self.combo_x.currentText()
            or self.combo_y.currentIndex() in (0, 1)
        ):
            self._setComboToPreferred(self.combo_y, ["Iwe", "I", "Ewe", "Zwe", "phase", "abs_I", "abs_Ewe"])
            if self.combo_y.currentText() == self.combo_x.currentText() and len(self.headers) > 1:
                for index in range(self.combo_y.count()):
                    if self.combo_y.itemText(index) != self.combo_x.currentText():
                        self.combo_y.setCurrentIndex(index)
                        break
        if self.combo_cycle.currentIndex() <= 0:
            self._setComboToPreferred(self.combo_cycle, ["cycle", "Cycle", "cycle number", "cycle_index"])

    def _setComboToPreferred(self, combo: QComboBox, preferred_names):
        for preferred_name in preferred_names:
            index = combo.findText(preferred_name)
            if index >= 0:
                combo.setCurrentIndex(index)
                return

    def _setColorTargets(self, targets):
        previous = self.combo_cycle_color_target.currentText()
        self.combo_cycle_color_target.blockSignals(True)
        self.combo_cycle_color_target.clear()
        self.combo_cycle_color_target.addItems(targets)
        if previous:
            previous_index = self.combo_cycle_color_target.findText(previous)
            if previous_index >= 0:
                self.combo_cycle_color_target.setCurrentIndex(previous_index)
        self.combo_cycle_color_target.blockSignals(False)
        self._updateColorButtonText()

    def _updateColorButtonText(self):
        target = self.combo_cycle_color_target.currentText() or "All data"
        if target in self.cycle_color_overrides:
            self.button_pick_color.setText(f"Set Color ({self.cycle_color_overrides[target]})")
        else:
            self.button_pick_color.setText("Set Color")

    def _pickCycleColor(self):
        target = self.combo_cycle_color_target.currentText() or "All data"
        initial_color = QColor(self.cycle_color_overrides.get(target, "#1565c0"))
        color = QColorDialog.getColor(initial_color, self, f"Select Color for {target}")
        if not color.isValid():
            return
        self.cycle_color_overrides[target] = color.name()
        self._updateColorButtonText()
        self.refreshPlot()

    def _clearCycleColorOverride(self):
        target = self.combo_cycle_color_target.currentText() or "All data"
        if target in self.cycle_color_overrides:
            self.cycle_color_overrides.pop(target)
            self._updateColorButtonText()
            self.refreshPlot()

    def _buildColors(self, cycle_labels):
        colors = {}
        for index, cycle_label in enumerate(cycle_labels):
            if cycle_label in self.cycle_color_overrides:
                colors[cycle_label] = QColor(self.cycle_color_overrides[cycle_label])
            else:
                colors[cycle_label] = self._paletteColor(index)
        return colors

    def _paletteColor(self, index: int):
        palette = self.COLOR_MAPS.get(self.combo_colormap.currentText(), self.COLOR_MAPS["Viridis"])
        return QColor(palette[index % len(palette)])

    def _formatCycleValue(self, value):
        text = str(value).strip()
        if not text:
            return ""
        numeric_value = self._toFloat(text)
        if numeric_value is None:
            return text
        if float(numeric_value).is_integer():
            return str(int(numeric_value))
        return f"{numeric_value:.6g}"

    def _readDelimitedFile(self, file_path: str):
        with open(file_path, "r", newline="", encoding="utf-8-sig") as file_obj:
            sample = file_obj.read(4096)
            file_obj.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except csv.Error:
                dialect = csv.excel

            try:
                has_header = csv.Sniffer().has_header(sample)
            except csv.Error:
                has_header = True

            reader = csv.reader(file_obj, dialect)
            raw_rows = [row for row in reader if any(cell.strip() for cell in row)]

        if not raw_rows:
            raise ValueError("file is empty")

        if has_header:
            headers = raw_rows[0]
            data_rows = raw_rows[1:]
        else:
            column_count = max(len(row) for row in raw_rows)
            headers = [f"Column {index + 1}" for index in range(column_count)]
            data_rows = raw_rows

        return self._normalizeHeaders(headers), data_rows

    def _normalizeHeaders(self, headers):
        normalized = []
        used_names = {}
        for index, header in enumerate(headers):
            base_name = str(header).strip() or f"Column {index + 1}"
            occurrence = used_names.get(base_name, 0)
            used_names[base_name] = occurrence + 1
            normalized.append(base_name if occurrence == 0 else f"{base_name} ({occurrence + 1})")
        return normalized

    def _toFloat(self, value):
        text = str(value).strip()
        if not text:
            return None
        try:
            return float(text)
        except ValueError:
            return None