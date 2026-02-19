#& "C:\Users\chrst\AppData\Roaming\Python\Python313\Scripts\pyside6-uic.exe" "uiEC.ui" "-o" "uiEC.py" "--from-imports"
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QApplication, QWidget,QTreeWidget,QTreeWidgetItem,QPushButton,QHBoxLayout,QLabel,QMainWindow,QTabWidget, QTabBar,QDockWidget,QVBoxLayout, QPlainTextEdit
from PySide6.QtCore import QSize, Qt, QEvent, QMimeData, QModelIndex, QPoint, QRect, QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QAbstractItemView 
from PySide6.QtGui import QMouseEvent,QDrag,QFont,QShortcut,QCursor,QAction,QKeySequence
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from UIFiles.qt_ECO_Main import Ui_MainWindow

from misc_handleException import exception2msg, msg2file, errorDeco

from misc_ModifiedUI import TechTreeWidget, FloatingTabWindow  

from UIModification.ui_CV import CV as CVUI
from UIModification.ui_CA import CA as CAUI 
from UIModification.ui_CP import CP as CPUI
from UIModification.ui_OCV import OCV as OCVUI
from UIModification.ui_EIS import EIS as EISUI
from UIFiles.qt_Move import Ui_Form as MoveUI
from UIFiles.qt_Loop import Ui_Form as LoopUI
from ui_PsInfoDialog import get_potentiostat_info_from_dialog
from misc_plot_axis_options import get_axis_options, apply_axis_transform, normalize_technique_name

from pt_biologic import Biologic

class ECO_pot(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.dicTechWin={
            'CA':CAUI,
            'CP':CPUI,
            'CV':CVUI,
            'OCV':OCVUI,
            'EIS':EISUI,
            'Move':MoveUI,
            'Loop':LoopUI
        }
        self.itemTechPair={}
        self.setupUi(self)
        self.ps_address = "192.168.2.2"
        self.ps_channel = 1
        self.ps_binary_path = os.environ.get("ECLIB_DIR", f"C:{os.sep}EC-Lab Development Package{os.sep}lib")
        self.CRdic={}
        self.PRDic={}
        self.BWDic={}
        self.currentChannel=1
        self.isPSConnected = False
        self.plotDataByTech = {}
        self.currentMeasuredTech = None
        self.plotXAxisOptions = {}
        self.plotYAxisOptions = {}
        self.restyle()
        self.bindEvent()
        self.bindSignalSlot()
        self._updateStatusBar()
        self.showMaximized()
        self._repl_globals = {"__builtins__": __builtins__}
        self._repl_locals = {"self": self}
      
    def restyle(self):
        # Replace the treewidget in the ui file with our custom one
        oldTreeWidget = self.treeWidget
        self.treeWidget = TechTreeWidget(self.splitter_Tech)
        self.splitter_Tech.insertWidget(1, self.treeWidget)
        self.treeWidget.setGeometry(oldTreeWidget.geometry())
        self.treeWidget.setObjectName(oldTreeWidget.objectName())
        oldTreeWidget.deleteLater()
        self.treeWidget.clear()
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setAcceptDrops(True)
        self.treeWidget.setDropIndicatorShown(True)
        self.treeWidget.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.treeWidget.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        
        # Setup Log widget in the log section
        self.Log = QPlainTextEdit()
        self.Log.setReadOnly(True)
        self._clearWidget(self.frame_Log)
        self.frame_Log.layout().addWidget(self.Log)
        self.lineEditLogInput = self.lineEdit
        self.lineEditLogInput.setPlaceholderText("Enter Python expression and press Enter")
        
        # Setup potentiostat section - add placeholder for tech details
        self._clearWidget(self.frame_pot)

        # Setup plot area and plot controls
        self._initPlotWidgets()
        

    @errorDeco(logger='self.Log')
    def addTech(self,sender,event):
        i_ranges = self.CRdic.get(self.currentChannel, [])
        item = QTreeWidgetItem()
        item.setText(0, sender.text())
        item.setSizeHint(0,QSize(0,30))
        font = QFont()
        font.setPointSize(14)      
        item.setFont(0, font) 
        self.treeWidget.addTopLevelItem(item)
        
        # Remove all widgets from the potentiostat section before loading new Form
        self._clearWidget(self.frame_pot)

        ui_class = self.dicTechWin.get(sender.text())
        page = self._buildTab(ui_class, item, i_ranges=i_ranges)     # QWidget ready
        self.frame_pot.layout().addWidget(page)
        self.itemTechPair[item] = page

    #---------------- Signal-Slot binding ----------------

    def bindSignalSlot(self):
        # Show the tech setup for the clicked tree item
        self.treeWidget.itemClicked.connect(self.TreeItemClicked)
        self.treeWidget.itemRemoved.connect(self._onTechItemRemoved)
        self.pushButtonStart.clicked.connect(self.startTech)
        self.pushButtonConnect.clicked.connect(self.connectPT)
        self.pushButtonPsInfo.clicked.connect(self.configurePotentiostat)
        if hasattr(self, "lineEditLogInput"):
            self.lineEditLogInput.returnPressed.connect(self.evalLogInput)
        if hasattr(self, "comboBoxPlotTech"):
            self.comboBoxPlotTech.currentTextChanged.connect(self._onPlotTechSelectionChanged)
        if hasattr(self, "comboBoxPlotX"):
            self.comboBoxPlotX.currentTextChanged.connect(lambda _: self._renderSelectedPlot())
        if hasattr(self, "comboBoxPlotY"):
            self.comboBoxPlotY.currentTextChanged.connect(lambda _: self._renderSelectedPlot())

    @errorDeco(logger='self.Log')
    def configurePotentiostat(self):
        result = get_potentiostat_info_from_dialog(
            self,
            self.ps_address,
            self.ps_channel,
            self.ps_binary_path,
        )
        if result is not None:
            self.ps_address, self.ps_channel, self.ps_binary_path = result
            self.logMsg(
                f"> Potentiostat info updated: address={self.ps_address}, channel={self.ps_channel}, binary_path={self.ps_binary_path}"
            )
            self._updateStatusBar()
    
    def bindEvent(self):
        for label in self.scrollAreaOption_Tech.findChildren(QLabel):
            label.mouseDoubleClickEvent=lambda e, sender=label: self.addTech(sender,e)
        
    #---------------- Slot functions ----------------  
    @errorDeco(logger='self.Log')
    def TreeItemClicked(self, item, column=None):
        page = self.itemTechPair.get(item)
        if page is None:
            return
        # If page is in a floating window, close that window
        current_parent = page.parent()
        if current_parent is not None:
            # Check if parent is a FloatingTabWindow
            if isinstance(current_parent, FloatingTabWindow):
                print(f"[DEBUG] Closing floating window for {page}")
                current_parent.close()
            # Reparent from any other parent
            page.setParent(None)
        
        # Show the tech details in potentiostat section
        self._clearWidget(self.frame_pot)
        self.frame_pot.layout().addWidget(page)

    @errorDeco(logger='self.Log')
    def startTech(self):
        self.sequence=[]
        for item in self._iter_tree_items():
            page=self.itemTechPair.get(item)
            if page is not None:
                self.sequence.append(page.outputParam())
        if hasattr(self, 'bio_worker'):
            self._setPlotTechItemsFromSequence(self.sequence)
            self.bio_worker.runSequence(self.sequence)
        else:
            self.logMsg("> Potentiostat not connected.")
        
    @errorDeco(logger='self.Log')
    def getChannelOptions(self, listOptions):
        channel, CRlist, PRlist, BWlist = listOptions
        self.ps_channel = channel
        self.CRdic[channel] = CRlist
        self.PRDic[channel] = PRlist
        self.BWDic[channel] = BWlist
        self._setPotentiostatConnected(True)
        self._refreshTechOptions()

    # Start potentiostat thread
    @errorDeco(logger='self.Log')
    def connectPT(self):
        if hasattr(self, 'bio_thread') and self.bio_thread.isRunning():
            self.logMsg("> Potentiostat thread is already running.")
            return
        
        self.bio_thread = QThread(self)
        self.bio_worker = Biologic(self.ps_address, self.ps_binary_path, self.ps_channel)
        self.bio_worker.moveToThread(self.bio_thread)

        self.bio_thread.started.connect(self.bio_worker.connectDevice)

        self.bio_worker.signalData.connect(self._onBiologicData)
        self.bio_worker.signalConnected.connect(self.getChannelOptions)
        self.bio_worker.signalFinished.connect(self.bio_thread.quit)
        self.bio_worker.signalLog.connect(self.Log.appendPlainText)
        self.bio_thread.finished.connect(lambda: self._setPotentiostatConnected(False))
        self.bio_thread.finished.connect(self.bio_thread.deleteLater)

        self.bio_thread.start()


    def logMsg(self, msg:str):
        self.Log.appendPlainText(msg)

    def _onTechItemRemoved(self, item: QTreeWidgetItem):
        page = self.itemTechPair.pop(item, None)
        if page is not None:
            page.setParent(None)
            page.deleteLater()

    @errorDeco(logger='self.Log')
    def evalLogInput(self):
        text = self.lineEditLogInput.text().strip()
        if not text:
            return
        self.lineEditLogInput.clear()
        self.logMsg(f">>> {text}")
        print(f">>> {text}")
        try:
            result = eval(text, self._repl_globals, self._repl_locals)
        except SyntaxError:
            try:
                exec(text, self._repl_globals, self._repl_locals)
                result = None
            except Exception as ex:
                error_msg = exception2msg(ex)
                self.logMsg(error_msg)
                print(error_msg)
                return
        except Exception as ex:
            error_msg = exception2msg(ex)
            self.logMsg(error_msg)
            print(error_msg)
            return
        if result is not None:
            msg = repr(result)
            self.logMsg(msg)
            print(msg)

    #---------------- Helper functions ----------------

    def _clearWidget(self, widget: QWidget):
        layout = widget.layout()
        if layout is None:
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
        while layout.count():
            layoutItem = layout.takeAt(0)
            childWidget = layoutItem.widget()
            if childWidget:
                childWidget.setParent(None)

    def _buildTab(self, ui_class, item: QTreeWidgetItem, *, i_ranges: list[str] | None = None) -> QWidget:
        try:
            obj = ui_class(i_ranges=i_ranges)
        except TypeError:
            obj = ui_class()
        if hasattr(ui_class, "nameChanged"):
            obj.nameChanged.connect(lambda new_name, item=item: item.setText(0, new_name))
        if hasattr(obj, "setupUi") and not isinstance(obj, QWidget):
            container = QWidget()
            obj.setupUi(container)
            return container
        return obj

    def _iter_tree_items(self, parent: QTreeWidgetItem | None = None):
        if parent is None:
            for idx in range(self.treeWidget.topLevelItemCount()):
                item = self.treeWidget.topLevelItem(idx)
                if item is None:
                    continue
                yield item
                yield from self._iter_tree_items(item)
            return
        for idx in range(parent.childCount()):
            item = parent.child(idx)
            if item is None:
                continue
            yield item
            yield from self._iter_tree_items(item)

    def _setPotentiostatConnected(self, connected: bool):
        self.isPSConnected = connected
        self._updateStatusBar()

    def _initPlotWidgets(self):
        self.comboBoxPlotTech.clear()

        self.comboBoxPlotX.clear()
        self.comboBoxPlotY.clear()
        self.plotXAxisOptions = {}
        self.plotYAxisOptions = {}

        self.plotFigure = Figure()
        self.plotAxes = self.plotFigure.add_subplot(111)
        self.plotCanvas = FigureCanvas(self.plotFigure)

        oldPlotWidget = self.graphicsView
        plotIndex = self.verticalLayout_Plot.indexOf(oldPlotWidget)
        if plotIndex >= 0:
            self.verticalLayout_Plot.removeWidget(oldPlotWidget)
            self.verticalLayout_Plot.insertWidget(plotIndex, self.plotCanvas)
        oldPlotWidget.setParent(None)
        oldPlotWidget.deleteLater()

    def _onBiologicData(self, tech_name: str, output):
        self.currentMeasuredTech = tech_name
        self.plotDataByTech.setdefault(tech_name, []).append(output)

        selectedTech = self.comboBoxPlotTech.currentText()
        if selectedTech == "Current Tech":
            self._renderSelectedPlot()
        elif selectedTech == tech_name:
            self._renderSelectedPlot()

    def _setPlotTechItemsFromSequence(self, sequence: list):
        previousSelection = self.comboBoxPlotTech.currentText()
        self.comboBoxPlotTech.blockSignals(True)
        self.comboBoxPlotTech.clear()
        self.comboBoxPlotTech.addItem("Current Tech")

        seen = set()
        for measurement in sequence:
            tech_name = str(measurement.get("technique", "")).upper()
            if not tech_name or tech_name in seen:
                continue
            seen.add(tech_name)
            self.comboBoxPlotTech.addItem(tech_name)

        if previousSelection and self.comboBoxPlotTech.findText(previousSelection) >= 0:
            self.comboBoxPlotTech.setCurrentText(previousSelection)
        else:
            self.comboBoxPlotTech.setCurrentText("Current Tech")
        self.comboBoxPlotTech.blockSignals(False)
        self._configureAxisCombosForSelectedTech()

    def _onPlotTechSelectionChanged(self, _selected: str):
        self._configureAxisCombosForSelectedTech()
        self._renderSelectedPlot()

    def _configureAxisCombosForSelectedTech(self):
        selectedTech = self.comboBoxPlotTech.currentText()
        if not selectedTech:
            self.comboBoxPlotX.clear()
            self.comboBoxPlotY.clear()
            self.plotXAxisOptions = {}
            self.plotYAxisOptions = {}
            return

        techForAxes = self.currentMeasuredTech if selectedTech == "Current Tech" else selectedTech
        if not techForAxes:
            return

        axis_options = get_axis_options(normalize_technique_name(techForAxes))
        x_options = axis_options.get("x", [])
        y_options = axis_options.get("y", [])

        if not x_options or not y_options:
            return

        previousX = self.comboBoxPlotX.currentText()
        previousY = self.comboBoxPlotY.currentText()

        self.plotXAxisOptions = {option.label: option for option in x_options}
        self.plotYAxisOptions = {option.label: option for option in y_options}

        self.comboBoxPlotX.blockSignals(True)
        self.comboBoxPlotY.blockSignals(True)
        self.comboBoxPlotX.clear()
        self.comboBoxPlotY.clear()
        self.comboBoxPlotX.addItems(list(self.plotXAxisOptions.keys()))
        self.comboBoxPlotY.addItems(list(self.plotYAxisOptions.keys()))
        if previousX in self.plotXAxisOptions:
            self.comboBoxPlotX.setCurrentText(previousX)
        if previousY in self.plotYAxisOptions:
            self.comboBoxPlotY.setCurrentText(previousY)
        self.comboBoxPlotX.blockSignals(False)
        self.comboBoxPlotY.blockSignals(False)

    def _renderSelectedPlot(self):
        selectedTech = self.comboBoxPlotTech.currentText()
        techToPlot = self.currentMeasuredTech if selectedTech == "Current Tech" else selectedTech

        if not techToPlot:
            self._clearPlot("No tested data")
            return

        rows = self.plotDataByTech.get(techToPlot, [])
        if not rows:
            self._clearPlot(f"No tested data for {techToPlot}")
            return

        sample = next((row for row in rows if isinstance(row, dict) and row), None)
        if sample is None:
            self._clearPlot(f"No plottable data for {techToPlot}")
            return

        availableKeys = list(sample.keys())
        self._syncAxisCombo(self.comboBoxPlotX, availableKeys, prefer="t")
        self._syncAxisCombo(self.comboBoxPlotY, availableKeys, prefer="Ewe")

        xKey = self.comboBoxPlotX.currentText()
        yKey = self.comboBoxPlotY.currentText()
        if not xKey or not yKey:
            self._clearPlot(f"No axis selected for {techToPlot}")
            return

        xAxisOption = self.plotXAxisOptions.get(xKey)
        yAxisOption = self.plotYAxisOptions.get(yKey)

        xData = []
        yData = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            try:
                if xAxisOption and yAxisOption:
                    xRaw = row.get(xAxisOption.source)
                    yRaw = row.get(yAxisOption.source)
                    if xRaw is None or yRaw is None:
                        continue
                    xVal = apply_axis_transform(xAxisOption.transform, float(xRaw))
                    yVal = apply_axis_transform(yAxisOption.transform, float(yRaw))
                else:
                    xVal = row.get(xKey)
                    yVal = row.get(yKey)
                    if xVal is None or yVal is None:
                        continue
                    xVal = float(xVal)
                    yVal = float(yVal)

                if xVal is None or yVal is None:
                    continue
                xData.append(xVal)
                yData.append(yVal)
            except (TypeError, ValueError):
                continue

        if not xData:
            self._clearPlot(f"No numeric points for {techToPlot}")
            return

        self.plotAxes.clear()
        self.plotAxes.plot(xData, yData)
        self.plotAxes.set_title(f"{techToPlot}")
        self.plotAxes.set_xlabel(xKey)
        self.plotAxes.set_ylabel(yKey)
        self.plotAxes.grid(True)
        self.plotCanvas.draw_idle()

    def _syncAxisCombo(self, combo, keys: list[str], *, prefer: str):
        current = combo.currentText()
        if [combo.itemText(i) for i in range(combo.count())] == keys:
            if current in keys:
                combo.setCurrentText(current)
            return

        combo.blockSignals(True)
        combo.clear()
        combo.addItems(keys)
        if prefer in keys:
            combo.setCurrentText(prefer)
        elif current in keys:
            combo.setCurrentText(current)
        combo.blockSignals(False)

    def _clearPlot(self, title: str):
        self.plotAxes.clear()
        self.plotAxes.set_title(title)
        self.plotAxes.grid(True)
        self.plotCanvas.draw_idle()

    def _updateStatusBar(self):
        message = f"Potentiostat Channel: {self.ps_channel}" if self.isPSConnected else "Potentiostat Disconnected"
        self.statusBar().showMessage(message)
    
    def _refreshTechOptions(self):
        for page in self.itemTechPair.values():
            if hasattr(page, "setCR") and self.ps_channel in self.CRdic:
                page.setCR(self.CRdic[self.ps_channel])
            if hasattr(page, "setPR") and self.ps_channel in self.PRDic:
                page.setPR(self.PRDic[self.ps_channel])
            if hasattr(page, "setBW") and self.ps_channel in self.BWDic:
                page.setBW(self.BWDic[self.ps_channel])

    def closeEvent(self, event):
        if hasattr(self, 'bio_thread') and self.bio_thread.isRunning():
            self.bio_worker.stopExperiment(disconnect=True)
            self.bio_thread.quit()
            self.bio_thread.wait()
        self._setPotentiostatConnected(False)
        event.accept()
    

        

if __name__ =='__main__':
    try:
        Qapp=QApplication(sys.argv)
        Qapp.styleHints().setColorScheme(Qt.ColorScheme.Light)
        Qapp.setStyle("Fusion")
        app=ECO_pot()
        sys.exit(Qapp.exec())
    except Exception as ex:
        error_msg = exception2msg(ex)
        print(error_msg)
        msg2file(error_msg)
