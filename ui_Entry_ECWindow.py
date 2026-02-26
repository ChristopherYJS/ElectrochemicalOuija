#& "C:\Users\chrst\AppData\Roaming\Python\Python313\Scripts\pyside6-uic.exe" "uiEC.ui" "-o" "uiEC.py" "--from-imports"
import sys, os, csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QApplication, QWidget,QTreeWidget,QTreeWidgetItem,QPushButton,QHBoxLayout,QLabel,QMainWindow,QTabWidget, QTabBar,QDockWidget,QVBoxLayout, QPlainTextEdit, QRadioButton,QMessageBox, QButtonGroup, QInputDialog
from PySide6.QtCore import QSize, Qt, QEvent, QMimeData, QModelIndex, QPoint, QRect, QObject, QThread, Signal, Slot, QTimer
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
from UIModification.ui_Loop import Loop as LoopUI
from UIModification.ui_Move import Move as MoveUI
from UIFiles.qt_Move import Ui_Form as MoveUI
from UIFiles.qt_Loop import Ui_Form as LoopUI
from ui_PsInfoDialog import get_potentiostat_info_from_dialog
from misc_plot_axis_options import get_axis_options, apply_axis_transform, normalize_technique_name
from ui_plot import ElectrochemPlotter

from pt_biologic import Biologic

class ECO_pot(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.dictTechWin={
            'CA':CAUI,
            'CP':CPUI,
            'CV':CVUI,
            'OCV':OCVUI,
            'EIS':EISUI,
            'Move':MoveUI,
            'Loop':LoopUI
        }
        self.dictChannelTechs={}
        self.setupUi(self)
        self.addressPs = "192.168.2.2"
        self.numCurrentChannel = 1
        self.ps_binary_path = os.environ.get("ECLIB_DIR", f"C:{os.sep}EC-Lab Development Package{os.sep}lib")
        self.dictCR={}
        self.dictPR={}
        self.dictBW={}
        self.dictChannelRbtn={}
        self.groupChannelRbtn=QButtonGroup(self)
        self.groupChannelRbtn.setExclusive(True)
        self.isPSConnected = False
        self.dictChannelStatus={} 
        self.plotDataByTech = {}
        self.currentMeasuredTech = None
        self.plotXAxisOptions = {}
        self.plotYAxisOptions = {}
        self.new_data_available = False
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self._check_and_replot)
        self.plot_timer.start(500)  # Update plot every 500ms
        self.user_filename = None
        self.current_file = None
        self.current_writer = None
        self.current_tech = None
        self.tech_counters = {}
        self.current_seq_index = -1
        self.restyle()
        self.bindTechLabels()
        self.bindSignalSlot()
        self._updateStatusBar()
        self.showMaximized()
        self._repl_globals = {"__builtins__": __builtins__}
        self._repl_locals = {"self": self}

    def _check_and_replot(self):
        if self.new_data_available:
            selectedTech = self.plotter.tech_combo.currentText()
            if selectedTech == "Current Tech" or selectedTech == self.currentMeasuredTech:
                self._renderSelectedPlot()
            self.new_data_available = False
      
    def restyle(self):
        # Replace the treewidget in the ui file with our custom one
        oldTreeWidget = self.treeWidget_Techs
        self.treeWidget_Techs = TechTreeWidget(self.splitter_Tech)
        self.splitter_Tech.insertWidget(1, self.treeWidget_Techs)
        self.treeWidget_Techs.setGeometry(oldTreeWidget.geometry())
        self.treeWidget_Techs.setObjectName(oldTreeWidget.objectName())
        oldTreeWidget.deleteLater()
        self.treeWidget_Techs.clear()
        self.treeWidget_Techs.setHeaderHidden(True)
        self.treeWidget_Techs.setDragEnabled(True)
        self.treeWidget_Techs.setAcceptDrops(True)
        self.treeWidget_Techs.setDropIndicatorShown(True)
        self.treeWidget_Techs.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.treeWidget_Techs.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        
        # Setup Log widget in the log section
        self.Log = QPlainTextEdit()
        self.Log.setReadOnly(True)
        self._clearWidget(self.frame_log)
        self.frame_log.layout().addWidget(self.Log)
        self.lineEditLogInput = self.lineEdit
        self.lineEditLogInput.setPlaceholderText("Enter Python expression and press Enter")
        
        # Setup potentiostat section - add placeholder for tech details
        self._clearWidget(self.frame_ps)

        # Setup plot area and plot controls
        self._initPlotWidgets()
        

    @errorDeco(logger='self.Log')
    def addTech(self,sender,event):
        isChannelFree=not self.dictChannelStatus.get(self.numCurrentChannel, False)
        if self.isPSConnected and isChannelFree:
            if self.numCurrentChannel not in self.dictChannelTechs:
                self.dictChannelTechs[self.numCurrentChannel] = {}
            i_ranges = self.dictCR.get(self.numCurrentChannel, [])
            item = QTreeWidgetItem()
            item.setText(0, sender.text())
            item.setSizeHint(0,QSize(0,30))
            font = QFont()
            font.setPointSize(14)      
            item.setFont(0, font) 
            self.treeWidget_Techs.addTopLevelItem(item)
            
            # Remove all widgets from the potentiostat section before loading new Form
            self._clearWidget(self.frame_ps)

            ui_class = self.dictTechWin.get(sender.text())
            page = self._buildTab(ui_class, item, i_ranges=i_ranges)     # QWidget ready
            self.frame_ps.layout().addWidget(page)
            self.dictChannelTechs[self.numCurrentChannel][item] = page
            if hasattr(page, "setCR") and self.numCurrentChannel in self.dictCR:
                    page.setCR(self.dictCR[self.numCurrentChannel])
            if hasattr(page, "setPR") and self.numCurrentChannel in self.dictPR:
                page.setPR(self.dictPR[self.numCurrentChannel])
            if hasattr(page, "setBW") and self.numCurrentChannel in self.dictBW:
                page.setBW(self.dictBW[self.numCurrentChannel])
        else:
            #pop warning window to inform user to connect potentiostat or free the channel
            warning_msg = "Please connect to the potentiostat and ensure the channel is free before editing experiment sequence."
            QMessageBox.warning(self, "Cannot Add Technique", warning_msg) 

            

    #---------------- Signal-Slot binding ----------------
    @errorDeco(logger='self.Log')
    def bindSignalSlot(self):
        # Show the tech setup for the clicked tree item
        self.treeWidget_Techs.itemClicked.connect(self.TreeItemClicked)
        self.treeWidget_Techs.itemRemoved.connect(self._onTechItemRemoved)
        self.treeWidget_Techs.itemsReordered.connect(self._onTechItemsReordered)
        self.pushButtonStart.clicked.connect(self.startTech)
        self.pushButtonConnect.clicked.connect(self.connectPs)
        self.pushButtonErrorTest.clicked.connect(self.errorTest)
        # self.pushButtonPsInfo.clicked.connect(self.configurePotentiostat)
        if hasattr(self, "lineEditLogInput"):
            self.lineEditLogInput.returnPressed.connect(self.evalLogInput)
        self.groupChannelRbtn.buttonToggled.connect(lambda btn: self.switchChannel(btn) )

    # @errorDeco(logger='self.Log')
    # def configurePotentiostat(self):
    #     result = get_potentiostat_info_from_dialog(
    #         self,
    #         self.addressPs,
    #         self.ps_binary_path,
    #     )
    #     if result is not None:
    #         self.addressPs, self.ps_binary_path = result
    #         self.logMsg(
    #             f"> Potentiostat info updated: address={self.addressPs}, binary_path={self.ps_binary_path}"
    #         )
    #         self._updateStatusBar()
    
    def bindTechLabels(self):
        for label in self.scrollAreaOption_Techs.findChildren(QLabel):
            label.mouseDoubleClickEvent=lambda e, sender=label: self.addTech(sender,e)
    
    def errorTest(self):
        # Build the sequence
        self.sequence_meta = self._buildSequence()
        self.tech_counters = {}
        print("Tech Sequence:")
        for idx, meta in enumerate(self.sequence_meta):
            param = meta['param']
            loop_path = meta['loop_path']
            tech_name = param['Technique']
            if loop_path:
                loop_str = '-LOOP(' + ','.join(map(str, loop_path)) + ')'
                seq_str = ''
            else:
                self.tech_counters[tech_name] = self.tech_counters.get(tech_name, 0) + 1
                seq_str = f'-SEQ{self.tech_counters[tech_name]}'
                loop_str = ''
            filename = f'{self.user_filename}-CH{self.numCurrentChannel}{seq_str}{loop_str}-{tech_name.upper()}.csv'
            print(f"Step {idx+1}: {tech_name} -> {filename}")
        
    #---------------- Slot functions ----------------  
    @errorDeco(logger='self.Log')
    def TreeItemClicked(self, item, column=None):
        page = self.dictChannelTechs.get(self.numCurrentChannel, {}).get(item)
        if page is None:
            self._clearWidget(self.frame_ps)
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
        self._clearWidget(self.frame_ps)
        self.frame_ps.layout().addWidget(page)

    @errorDeco(logger='self.Log')
    def startTech(self):
        # Prompt for filename
        filename, ok = QInputDialog.getText(self, "Enter Filename", "Enter base filename for data files:")
        if not ok or not filename:
            return
        self.user_filename = filename
        # Close any open file
        if self.current_file:
            self.current_file.close()
            self.current_file = None
        self.current_tech = None
        self.tech_counters = {}  # Reset counters

        # Build sequence with loop expansion
        seq = self._buildSequence()
        self.sequence = [item['param'] for item in seq]
        self.sequence_meta = seq

        if not self.sequence:
            self.logMsg("> No techniques to run.")
            return

        if hasattr(self, 'bio_worker'):
            self._setPlotTechItemsFromSequence(self.sequence)
            self.bio_worker.runSequence(self.sequence, self.numCurrentChannel)
        else:
            self.logMsg("> Potentiostat not connected.")
        for item in self.sequence_meta:
            self.logMsg(f"> Starting {item['param'].get('technique', 'Unknown Tech')} with parameters: {item['param']}")

    def _buildSequence(self, parent=None, loop_path=None):
        if loop_path is None:
            loop_path = []
        seq = []
        if parent is None:
            # Top level items
            for idx in range(self.treeWidget_Techs.topLevelItemCount()):
                item = self.treeWidget_Techs.topLevelItem(idx)
                if item is None:
                    continue
                page = self.dictChannelTechs[self.numCurrentChannel].get(item)
                if page:
                    if page.tech == 'Loop':
                        iterations = page.iterations
                        for i in range(1, iterations + 1):
                            new_path = loop_path + [i]
                            subtree_seq = self._buildSequence(item, new_path)
                            seq.extend(subtree_seq)
                    else:
                        seq.append({'param': page.outputParam(), 'loop_path': loop_path})
        else:
            # Children of parent
            for idx in range(parent.childCount()):
                item = parent.child(idx)
                if item is None:
                    continue
                page = self.dictChannelTechs[self.numCurrentChannel].get(item)
                if page:
                    seq.append({'param': page.outputParam(), 'loop_path': loop_path})
        return seq

        
    @errorDeco(logger='self.Log')
    def getChannelInfo(self, listOptions):
        if listOptions and isinstance(listOptions[0], list):
            # Multiple channels: list of [channel, CRlist, PRlist, BWlist]
            for options in listOptions:
                channel, CRlist, PRlist, BWlist = options
                self.dictCR[channel] = CRlist
                self.dictPR[channel] = PRlist
                self.dictBW[channel] = BWlist
            # Set default channel to the first available
            self.numCurrentChannel = listOptions[0][0] if listOptions else 1
        else:
            # Single channel
            channel, CRlist, PRlist, BWlist = listOptions
            self.numCurrentChannel = channel
            self.dictCR[channel] = CRlist
            self.dictPR[channel] = PRlist
            self.dictBW[channel] = BWlist
        
        self._setPotentiostatConnected(True)
        self._refreshTechOptions()

    @errorDeco(logger='self.Log')
    def updateChannelOption(self,channelList):
        for channel in channelList:
            channelRbutton=QRadioButton(f"CH {channel}")
            channelRbutton.objectName=f"radioButton_CH{channel}"
            self.formLayout_Channel.addWidget(channelRbutton)
            self.dictChannelRbtn[channel]=channelRbutton
            self.groupChannelRbtn.addButton(channelRbutton, channel)
            self.dictChannelStatus[channel]=False  


    # Start potentiostat thread
    @errorDeco(logger='self.Log')
    def connectPs(self):
        if hasattr(self, 'bio_thread') and self.bio_thread.isRunning():
            self.logMsg("> Potentiostat thread is already running.")
            return
        
        self.bio_thread = QThread(self)
        self.bio_worker = Biologic(self.addressPs, self.ps_binary_path)
        self.bio_worker.moveToThread(self.bio_thread)

        self.bio_thread.started.connect(self.bio_worker.connectDevice)

        self.bio_worker.signalData.connect(self._onBiologicData)
        self.bio_worker.signalConnected.connect(self.getChannelInfo)
        self.bio_worker.signalChannelOption.connect(self.updateChannelOption)
        self.bio_worker.signalFinished.connect(self.bio_thread.quit)
        self.bio_worker.signalLog.connect(self.Log.appendPlainText)
        self.bio_thread.finished.connect(lambda: self._setPotentiostatConnected(False))
        self.bio_thread.finished.connect(self.bio_thread.deleteLater)

        self.bio_thread.start()


    def logMsg(self, msg:str):
        self.Log.appendPlainText(msg)

    

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

    @errorDeco(logger='self.Log')
    def switchChannel(self, btn):
        channel = self.groupChannelRbtn.id(btn)
        self.numCurrentChannel = channel
        self._detachTreeItems()
        self._clearWidget(self.frame_ps)
        sequence = self.dictChannelTechs.get(channel, {})
        if sequence:
            for item, page in sequence.items():
                self.treeWidget_Techs.addTopLevelItem(item)
            first_item = self.treeWidget_Techs.topLevelItem(0)
            if first_item is not None:
                self.treeWidget_Techs.setCurrentItem(first_item)
                self.TreeItemClicked(first_item, 0)
                
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
                childWidget.hide()
                childWidget.setParent(None)

    def _detachTreeItems(self):
        while self.treeWidget_Techs.topLevelItemCount() > 0:
            self.treeWidget_Techs.takeTopLevelItem(0)

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
            for idx in range(self.treeWidget_Techs.topLevelItemCount()):
                item = self.treeWidget_Techs.topLevelItem(idx)
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

    def _onTechItemRemoved(self, item: QTreeWidgetItem):
        if self.numCurrentChannel in self.dictChannelTechs:
            page = self.dictChannelTechs[self.numCurrentChannel].pop(item, None)
            if page is not None:
                page.setParent(None)
                page.deleteLater()

    def _onTechItemsReordered(self):
        if self.numCurrentChannel not in self.dictChannelTechs:
            return
        # Reorder the dict to match the full tree order (top-level + children)
        new_dict = {}
        for item in self._iter_tree_items():
            if item in self.dictChannelTechs[self.numCurrentChannel]:
                new_dict[item] = self.dictChannelTechs[self.numCurrentChannel][item]
        self.dictChannelTechs[self.numCurrentChannel] = new_dict

    def _setPotentiostatConnected(self, connected: bool):
        self.isPSConnected = connected
        self._updateStatusBar()

    def _initPlotWidgets(self):
        # Create the plotter widget
        self.plotter = ElectrochemPlotter()
        self.verticalLayout_Plot.addWidget(self.plotter)
        # Connect signals
        self.plotter.tech_combo.currentTextChanged.connect(self._onPlotTechSelectionChanged)
        self.plotter.x_combo.currentTextChanged.connect(lambda _: self._renderSelectedPlot())
        self.plotter.y_combo.currentTextChanged.connect(lambda _: self._renderSelectedPlot())
        self.plotter.axisUnitChanged.connect(self._on_axis_unit_changed)

    def _on_axis_unit_changed(self, axis, unit):
        # Re-render the plot with new units
        self._renderSelectedPlot()

    def _onBiologicData(self, tech_name: str, output):
        self.currentMeasuredTech = tech_name
        self.plotDataByTech.setdefault(tech_name, []).append(output)
        self.new_data_available = True
        # Save to file
        if self.user_filename and tech_name != self.current_tech:
            if self.current_file:
                self.current_file.close()
            self.current_seq_index += 1
            loop_path = self.sequence_meta[self.current_seq_index]['loop_path']
            if loop_path:
                loop_str = '-LOOP(' + ','.join(map(str, loop_path)) + ')'
                seq_str = ''
            else:
                self.tech_counters[tech_name] = self.tech_counters.get(tech_name, 0) + 1
                seq_str = f'-SEQ{self.tech_counters[tech_name]}'
                loop_str = ''
            filename = f'{self.user_filename}-CH{self.numCurrentChannel}{seq_str}{loop_str}-{tech_name.upper()}.csv'
            self.current_file = open(filename, 'w', newline='')
            self.current_writer = csv.DictWriter(self.current_file, fieldnames=output.keys())
            self.current_writer.writeheader()
            self.current_tech = tech_name
        if self.current_writer:
            self.current_writer.writerow(output)

    def _setPlotTechItemsFromSequence(self, sequence: list):
        previousSelection = self.plotter.tech_combo.currentText()
        self.plotter.tech_combo.blockSignals(True)
        self.plotter.tech_combo.clear()
        self.plotter.tech_combo.addItem("Current Tech")

        seen = set()
        for measurement in sequence:
            tech_name = str(measurement.get("technique", "")).upper()
            if not tech_name or tech_name in seen:
                continue
            seen.add(tech_name)
            self.plotter.tech_combo.addItem(tech_name)

        if previousSelection and self.plotter.tech_combo.findText(previousSelection) >= 0:
            self.plotter.tech_combo.setCurrentText(previousSelection)
        else:
            self.plotter.tech_combo.setCurrentText("Current Tech")
        self.plotter.tech_combo.blockSignals(False)
        self._configureAxisCombosForSelectedTech()

    def _onPlotTechSelectionChanged(self, _selected: str):
        self._configureAxisCombosForSelectedTech()
        self._renderSelectedPlot()

    def _configureAxisCombosForSelectedTech(self):
        selectedTech = self.plotter.tech_combo.currentText()
        if not selectedTech:
            self.plotter.x_combo.clear()
            self.plotter.y_combo.clear()
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

        previousX = self.plotter.x_combo.currentText()
        previousY = self.plotter.y_combo.currentText()

        self.plotXAxisOptions = {option.label: option for option in x_options}
        self.plotYAxisOptions = {option.label: option for option in y_options}

        self.plotter.x_combo.blockSignals(True)
        self.plotter.y_combo.blockSignals(True)
        self.plotter.x_combo.clear()
        self.plotter.y_combo.clear()
        self.plotter.x_combo.addItems(list(self.plotXAxisOptions.keys()))
        self.plotter.y_combo.addItems(list(self.plotYAxisOptions.keys()))
        if previousX in self.plotXAxisOptions:
            self.plotter.x_combo.setCurrentText(previousX)
        if previousY in self.plotYAxisOptions:
            self.plotter.y_combo.setCurrentText(previousY)
        self.plotter.x_combo.blockSignals(False)
        self.plotter.y_combo.blockSignals(False)

    def _renderSelectedPlot(self):
        selectedTech = self.plotter.tech_combo.currentText()
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
        self._syncAxisCombo(self.plotter.x_combo, availableKeys, prefer="t")
        self._syncAxisCombo(self.plotter.y_combo, availableKeys, prefer="Ewe")

        xKey = self.plotter.x_combo.currentText()
        yKey = self.plotter.y_combo.currentText()
        if not xKey or not yKey:
            self._clearPlot(f"No axis selected for {techToPlot}")
            return

        # Determine axis types
        x_type = 'time' if 't' in xKey.lower() else 'other'
        y_type = 'current' if 'i' in yKey.lower() else ('potential' if 'e' in yKey.lower() or 'v' in yKey.lower() else 'other')
        self.plotter.set_axis_types(x_type, y_type)

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

        # Apply unit scaling
        xData = self._scale_data(xData, self.plotter.current_x_unit, x_type)
        yData = self._scale_data(yData, self.plotter.current_y_unit, y_type)

        # Downsample if too many points
        if len(xData) > 1000:
            xData, yData = self._downsample(xData, yData, 1000)

        self.plotter.ax.clear()
        self.plotter.ax.plot(xData, yData)
        self.plotter.ax.set_title(f"{techToPlot}")
        self.plotter.ax.set_xlabel(f"{xKey} ({self.plotter.current_x_unit})")
        self.plotter.ax.set_ylabel(f"{yKey} ({self.plotter.current_y_unit})")
        self.plotter.ax.grid(True)
        self.plotter.canvas.draw_idle()

    def _scale_data(self, data, unit, axis_type):
        if axis_type == 'current':
            # Data in mA
            if unit == 'A':
                return [v / 1000 for v in data]
            elif unit == 'mA':
                return data
            elif unit == 'uA':
                return [v * 1000 for v in data]
            elif unit == 'nA':
                return [v * 1000000 for v in data]
        elif axis_type == 'potential':
            # Data in V
            if unit == 'V':
                return data
            elif unit == 'mV':
                return [v * 1000 for v in data]
            elif unit == 'uV':
                return [v * 1000000 for v in data]
        elif axis_type == 'time':
            # Data in s
            if unit == 's':
                return data
            elif unit == 'ms':
                return [v * 1000 for v in data]
            elif unit == 'us':
                return [v * 1000000 for v in data]
        return data

    def _downsample(self, x_data, y_data, max_points):
        if len(x_data) <= max_points:
            return x_data, y_data
        step = len(x_data) // max_points
        x_down = x_data[::step]
        y_down = y_data[::step]
        return x_down, y_down

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
        self.plotter.ax.clear()
        self.plotter.ax.set_title(title)
        self.plotter.ax.grid(True)
        self.plotter.canvas.draw_idle()

    def _updateStatusBar(self):
        message = f"Potentiostat Channel: {self.numCurrentChannel}" if self.isPSConnected else "Potentiostat Disconnected"
        self.statusBar().showMessage(message)
    
    def _refreshTechOptions(self):
        current_channel_dict = self.dictChannelTechs.get(self.numCurrentChannel, {})
        for page in current_channel_dict.values():
            if hasattr(page, "setCR") and self.numCurrentChannel in self.dictCR:
                page.setCR(self.dictCR[self.numCurrentChannel])
            if hasattr(page, "setPR") and self.numCurrentChannel in self.dictPR:
                page.setPR(self.dictPR[self.numCurrentChannel])
            if hasattr(page, "setBW") and self.numCurrentChannel in self.dictBW:
                page.setBW(self.dictBW[self.numCurrentChannel])

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
