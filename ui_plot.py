# ui_plot.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QToolButton, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal

class ElectrochemPlotter(QWidget):
    # Signal to notify UI of changes (e.g., for axis unit updates)
    axisUnitChanged = Signal(str, str)  # axis ('x' or 'y'), unit

    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        
        # Toolbar for zoom/resize (built-in Matplotlib toolbar)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # Custom buttons for interactions
        self.zoom_button = QPushButton("Zoom")
        self.zoom_button.clicked.connect(self.enable_zoom)
        self.resize_button = QPushButton("Resize/Fit")
        self.resize_button.clicked.connect(self.resize_plot)
        
        # Tool buttons for axis units
        self.x_unit_button = QToolButton()
        self.x_unit_button.setText("X Units")
        self.y_unit_button = QToolButton()
        self.y_unit_button.setText("Y Units")
        
        # Current units
        self.current_x_unit = 's'  # default
        self.current_y_unit = 'mA'  # default
        
        # Combo boxes for plot selection
        self.tech_combo = QComboBox()
        self.x_combo = QComboBox()
        self.y_combo = QComboBox()
        
        # Layout
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(QLabel("Tech:"))
        button_layout.addWidget(self.tech_combo)
        button_layout.addWidget(QLabel("X:"))
        button_layout.addWidget(self.x_combo)
        button_layout.addWidget(QLabel("Y:"))
        button_layout.addWidget(self.y_combo)
        button_layout.addWidget(QLabel("X Units:"))
        button_layout.addWidget(self.x_unit_button)
        button_layout.addWidget(QLabel("Y Units:"))
        button_layout.addWidget(self.y_unit_button)
        button_layout.addWidget(self.zoom_button)
        button_layout.addWidget(self.resize_button)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Connect hover event
        self.canvas.mpl_connect('motion_notify_event', self.on_hover)

    def plot_data(self, x_data, y_data, x_label="X", y_label="Y"):
        """Plot the given data."""
        self.ax.clear()
        self.ax.plot(x_data, y_data)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.canvas.draw()

    def enable_zoom(self):
        """Enable zoom mode (using Matplotlib's built-in zoom)."""
        self.toolbar.zoom()

    def resize_plot(self):
        """Resize/fit the plot to the canvas."""
        self.ax.autoscale()
        self.canvas.draw()

    def on_hover(self, event):
        """Show point data on hover."""
        if event.inaxes == self.ax:
            x, y = event.xdata, event.ydata
            # Display tooltip (you can use PyQt's QToolTip or a custom label)
            self.setToolTip(f"X: {x:.2f}, Y: {y:.2f}")

    def set_axis_types(self, x_type, y_type):
        self.set_unit_menu(self.x_unit_button, x_type, 'x')
        self.set_unit_menu(self.y_unit_button, y_type, 'y')

    def set_unit_menu(self, button, axis_type, axis):
        menu = button.menu()
        if not menu:
            menu = QMenu(self)
            button.setMenu(menu)
        menu.clear()
        if axis_type == 'current':
            units = ['A', 'mA', 'uA', 'nA']
        elif axis_type == 'potential':
            units = ['V', 'mV', 'uV']
        elif axis_type == 'time':
            units = ['s', 'ms', 'us']
        else:
            units = ['default']
        for unit in units:
            action = QAction(unit, self)
            action.triggered.connect(lambda checked, u=unit, a=axis: self.change_axis_units(a, u))
            menu.addAction(action)

    def change_axis_units(self, axis, unit):
        if axis == 'x':
            self.current_x_unit = unit
        elif axis == 'y':
            self.current_y_unit = unit
        self.axisUnitChanged.emit(axis, unit)