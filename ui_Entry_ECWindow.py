#& "C:\Users\chrst\AppData\Roaming\Python\Python313\Scripts\pyside6-uic.exe" "uiEC.ui" "-o" "uiEC.py" "--from-imports"
import sys, os, csv, types
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QWidget,QTreeWidget,QTreeWidgetItem,QPushButton,QHBoxLayout,QLabel,QMainWindow,QTabWidget, QTabBar,QDockWidget,QVBoxLayout, QPlainTextEdit, QRadioButton,QMessageBox, QButtonGroup, QInputDialog, QDialog, QDialogButtonBox, QCheckBox
from PySide6.QtCore import QSize, Qt, QEvent, QMimeData, QModelIndex, QPoint, QRect, QObject, QThread, Signal, Slot, QTimer
from PySide6.QtWidgets import QAbstractItemView 
from PySide6.QtGui import QMouseEvent,QDrag,QFont,QShortcut,QCursor,QAction,QKeySequence

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from misc_handleException import exception2msg, msg2file, errorDeco
from misc_ModifiedUI import TechTreeWidget

from pt_biologic import Biologic

from UIFiles.qt_ECO_Main import Ui_MainWindow
from UIModification.misc_BaseTech import MOTech
from UIModification.ui_CV import CV as CVUI
from UIModification.ui_CA import CA as CAUI 
from UIModification.ui_CP import CP as CPUI
from UIModification.ui_OCV import OCV as OCVUI
from UIModification.ui_EIS import EIS as EISUI
from UIModification.ui_Loop import Loop as LoopUI
from UIModification.ui_Move import Move as MoveUI

from ui_PsInfoDialog import get_potentiostat_info_from_dialog
from misc_plot_axis_options import get_axis_options, apply_axis_transform, normalize_technique_name
from ui_plot import ElectrochemPlotter


from defaultSeq import build_default_sequence_ui



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
        self.dict_ChannelTechs={} # QTreeWidgetItem and MOTech pair of each channel
        self.dict_ChannelParams={} #Tech params for each channel 
        self.dict_ChannelStatus={} #status of each channel

        self.address_PS = "192.168.2.2"
        self.channel_Current = 1 #channel number of whose setup is being displayed
        self.path_BinaryPS = os.environ.get("ECLIB_DIR", f"C:{os.sep}EC-Lab Development Package{os.sep}lib")

        self.dict_CR={} #current ranges for each channel
        self.dict_PR={} #potential ranges for each channel
        self.dict_BW={} #bandwidth options for each channel

        self.dict_ChannelRbtn={} #channel number to its radio button widget in the UI
        self.group_ChannelRbtn=QButtonGroup(self)
        self.group_ChannelRbtn.setExclusive(True)

        self.is_PSConnected = False
        self.filename_User = None #user set filename for data output

        self.plotDataByTech = {}
        self.currentMeasuredTech = None
        self.plotXAxisOptions = {}
        self.plotYAxisOptions = {}
        self.new_data_available = False
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self._check_and_replot)
        self.plot_timer.start(500)  # Update plot every 500ms
        
        self.current_file = None
        self.current_writer = None
        self.current_tech = None
        self.tech_counters = {}
        self.current_seq_index = -1

        self.setupUi(self)
        self.restyle()
        self.bindTechLabels()
        self.bindSignalSlot()
        self._updateStatusBar()

        self.updateChannelOption([1,2]) #test

        ##=====================================================================================## 
        # For checking variables in log 
        ##=====================================================================================## 
        self._repl_globals = {"__builtins__": __builtins__}
        self._repl_locals = {"self": self}

        self.showMaximized()

    def _check_and_replot(self):
        if self.new_data_available:
            selectedTech = self.plotter.tech_combo.currentText()
            if selectedTech == "Current Tech" or selectedTech == self.currentMeasuredTech:
                self._renderSelectedPlot()
            self.new_data_available = False
    ##=====================================================================================## 
    # Restyle and UI setup functions 
    ##=====================================================================================##
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
        log_frame = getattr(self, "frame_log", None) or getattr(self, "fram_log", None)
        if log_frame is not None:
            self._clearPSFrameWidget(log_frame)
            log_frame.layout().addWidget(self.Log)

        self.lineEditLogInput = getattr(self, "lineEdit", None) or getattr(self, "lineEdit_Log", None)
        if self.lineEditLogInput is not None:
            self.lineEditLogInput.setPlaceholderText("Enter Python expression and press Enter")
        # Setup potentiostat section - add placeholder for tech details
        self._clearPSFrameWidget(self.frame_ps)
        # Setup plot area and plot controls
        # self._initPlotWidgets()
    ##=====================================================================================##
    # Signal-slot binding functions
    ##=====================================================================================##
    def bindSignalSlot(self):
        # Show the tech setup for the clicked tree item
        self.treeWidget_Techs.itemClicked.connect(self.TreeItemClicked)
        self.treeWidget_Techs.itemRemoved.connect(self._onTechItemRemoved)
        self.treeWidget_Techs.itemsReordered.connect(self._onTechItemsReordered)
        self.pushButton_SingleRun.clicked.connect(self.startTech)
        self.pushButton_MultiRun.clicked.connect(self.startMultiTech)
        self.pushButtonConnect.clicked.connect(self.connectPs)
        self.pushButton_ErrorTest.clicked.connect(self.errorTest)
        self.pushButton_3.clicked.connect(lambda: build_default_sequence_ui(self))
        self.lineEditLogInput.returnPressed.connect(self.evalLogInput)
        self.group_ChannelRbtn.buttonToggled.connect(lambda btn: self.switchChannel(btn) )
    ##=====================================================================================##
    # Tech label binding functions
    ##=====================================================================================##
    def bindTechLabels(self):
        for label in self.scrollAreaOption_Techs.findChildren(QLabel):
            label.mouseDoubleClickEvent=lambda e, sender=label: self.addTech(sender,e)

    def errorTest(self):
        sequence = self._buildSequence(self.channel_Current)
        print("Tech Sequence:")
        for idx, page in enumerate(sequence):
            techname = page.tech
            expname = page.name
            loop = page.loop
            print(f"{idx+1}. CH{self.channel_Current}_{techname}_{expname}_loop{loop}")
        
    ##=====================================================================================##
    # Slot functions
    ##=====================================================================================##
    @errorDeco(logger='self.Log')
    def addTech(self,sender,event) -> None:
        """
        Add a technique to the sequence tree when its label is double-clicked in the UI.
        """
        isChannelFree=not self.dict_ChannelStatus.get(self.channel_Current, False)
        if self.is_PSConnected and isChannelFree: 
            if self.channel_Current not in self.dict_ChannelTechs:
                self.dict_ChannelTechs[self.channel_Current] = {}
            i_ranges = self.dict_CR.get(self.channel_Current, [])

            # If a loop item is focused, add new technique as its child; otherwise, add as a new top-level item
            treeWidgetFocused = self.treeWidget_Techs.currentItem()
            target_parent = None
            if treeWidgetFocused is not None:
                current_page = self.dict_ChannelTechs[self.channel_Current].get(treeWidgetFocused)
                if current_page and getattr(current_page, "tech", "") == "Loop":
                    target_parent = treeWidgetFocused

            item = QTreeWidgetItem()
            item.setText(0, sender.text())
            item.setSizeHint(0,QSize(0,30))
            font = QFont()
            font.setPointSize(14)      
            item.setFont(0, font) 
            if target_parent is not None:
                target_parent.addChild(item)
                target_parent.setExpanded(True)
            else:
                self.treeWidget_Techs.addTopLevelItem(item)
            
            # Remove all widgets from the potentiostat section before loading new Form
            self._clearPSFrameWidget(self.frame_ps)

            ui_class = self.dictTechWin.get(sender.text())
            page = self._buildTechPage(ui_class, item, i_ranges=i_ranges)     
            self.frame_ps.layout().addWidget(page)
            self.dict_ChannelTechs[self.channel_Current][item] = page
            self.treeWidget_Techs.setCurrentItem(item)
            if hasattr(page, "setCR") and self.channel_Current in self.dict_CR:
                page.setCR(self.dict_CR[self.channel_Current])
            if hasattr(page, "setPR") and self.channel_Current in self.dict_PR:
                page.setPR(self.dict_PR[self.channel_Current])
            if hasattr(page, "setBW") and self.channel_Current in self.dict_BW:
                page.setBW(self.dict_BW[self.channel_Current])
        else:
            #pop warning window to inform user to connect potentiostat or free the channel
            warning_msg = "Please connect to the potentiostat and ensure the channel is free before editing experiment sequence."
            QMessageBox.warning(self, "Cannot Add Technique", warning_msg) 
    

    @errorDeco(logger='self.Log')
    def TreeItemClicked(self, item, column=None):
        page = self.dict_ChannelTechs.get(self.channel_Current, {}).get(item)
        self._clearPSFrameWidget(self.frame_ps)
        self.frame_ps.layout().addWidget(page)
        page.show()

    @errorDeco(logger='self.Log')
    def startTech(self):
        if not hasattr(self, 'bio_worker'):
            self.logMsg("> Potentiostat not connected.")
            return

        filename, ok = QInputDialog.getText(self, "Enter Filename", "Enter base filename for data files:")
        if not ok or not filename:
            return
        self.filename_User = filename

        if self.current_file:
            self.current_file.close()
            self.current_file = None
        self.current_writer = None
        self.current_tech = None
        self.current_seq_index = -1
        self.tech_counters = {}

        sequence = self._buildSequence(self.channel_Current)
        if not sequence:
            msg = f"Channel {self.channel_Current} has an empty sequence."
            QMessageBox.critical(self, "Start Error", msg)
            raise ValueError(msg)

        self.sequence = sequence
        plot_sequence = [
            step.outputParam() if hasattr(step, "outputParam") and callable(step.outputParam) else step
            for step in self.sequence
        ]
        self._setPlotTechItemsFromSequence(plot_sequence)
        self.bio_worker.runSequence(self.sequence, self.channel_Current, self.filename_User)
        self.logMsg(f"> Starting single-channel run on CH {self.channel_Current}")

        for step in self.sequence:
            params = step.outputParam() if hasattr(step, "outputParam") and callable(step.outputParam) else step
            if isinstance(params, dict):
                self.logMsg(f"> CH {self.channel_Current} starting {params.get('technique', 'Unknown Tech')} with parameters: {params}")

    @errorDeco(logger='self.Log')
    def startMultiTech(self):
        if not hasattr(self, 'bio_worker'):
            self.logMsg("> Potentiostat not connected.")
            return

        run_channels = self._selectMultiRunChannels()
        if not run_channels:
            return

        filename, ok = QInputDialog.getText(self, "Enter Filename", "Enter base filename for data files:")
        if not ok or not filename:
            return
        self.filename_User = filename

        if self.current_file:
            self.current_file.close()
            self.current_file = None
        self.current_writer = None
        self.current_tech = None
        self.current_seq_index = -1
        self.tech_counters = {}

        channel_sequences = {}
        empty_channels = []
        for channel in run_channels:
            seq = self._buildSequence(channel)
            if not seq:
                empty_channels.append(channel)
            else:
                channel_sequences[channel] = seq

        if empty_channels:
            msg = f"Selected channel(s) have empty sequence: {empty_channels}"
            QMessageBox.critical(self, "Start Error", msg)
            raise ValueError(msg)

        primary_channel = self.channel_Current if self.channel_Current in channel_sequences else run_channels[0]
        self.sequence = channel_sequences[primary_channel]

        plot_sequence = [
            step.outputParam() if hasattr(step, "outputParam") and callable(step.outputParam) else step
            for step in self.sequence
        ]
        self._setPlotTechItemsFromSequence(plot_sequence)

        self.bio_worker.runSequence(channel_sequences, run_channels, self.filename_User)
        self.logMsg(f"> Starting multi-channel run on CH {run_channels}")

        for channel in run_channels:
            for step in channel_sequences[channel]:
                params = step.outputParam() if hasattr(step, "outputParam") and callable(step.outputParam) else step
                if isinstance(params, dict):
                    self.logMsg(f"> CH {channel} starting {params.get('technique', 'Unknown Tech')} with parameters: {params}")

    def _selectMultiRunChannels(self) -> list[int]:
        connected_channels = sorted(self.dict_ChannelRbtn.keys())
        if not connected_channels:
            QMessageBox.warning(self, "No Channels", "No connected channels available.")
            return []

        dialog = QDialog(self)
        dialog.setWindowTitle("Select Channels")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Select channels to run:"))

        checkboxes = {}
        for channel in connected_channels:
            checkbox = QCheckBox(f"CH {channel}")
            checkbox.setChecked(channel == self.channel_Current)
            checkboxes[channel] = checkbox
            layout.addWidget(checkbox)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec() != QDialog.Accepted:
            return []

        selected_channels = [channel for channel, checkbox in checkboxes.items() if checkbox.isChecked()]
        if not selected_channels:
            QMessageBox.warning(self, "No Selection", "Please select at least one channel.")
            return []

        return selected_channels

    def _buildSequence(self, channel: int, parent=None, pathCurrent=None) -> list[MOTech]:
        """
        This builds the sequence for both biologic to run and to output correct filename. 
        I dont know how this works but it works, so don't change it.
        """
        seq = []

        if pathCurrent is None:
            pathCurrent = [1]

        dictTechs = self.dict_ChannelTechs.get(channel, {})

        if parent is None:
            items = [item for item in dictTechs.keys() if item.parent() is None]
        else:
            items = [parent.child(i) for i in range(parent.childCount())]

        for item in items:
            if item is None:
                continue

            page = dictTechs.get(item)
            if page is None:
                continue

            if page.tech == "Loop":
                for i in range(1, int(page.iterations) + 1):
                    seq.extend(self._buildSequence(channel, item, pathCurrent + [i]))
                continue

            runtime = page.__class__()
            runtime.tech = page.tech
            runtime.name = page.name
            runtime.loop = pathCurrent.copy()

            frozen_param = page.outputParam()

            def _frozen_output(self, _param=frozen_param):
                return dict(_param)

            runtime.outputParam = types.MethodType(_frozen_output, runtime)
            seq.append(runtime)

        return seq

        
    @errorDeco(logger='self.Log')
    def getChannelInfo(self, listOptions):
        if listOptions and isinstance(listOptions[0], list):
            # Multiple channels: list of [channel, CRlist, PRlist, BWlist]
            for options in listOptions:
                channel, CRlist, PRlist, BWlist = options
                self.dict_CR[channel] = CRlist
                self.dict_PR[channel] = PRlist
                self.dict_BW[channel] = BWlist
            # Set default channel to the first available
            self.channel_Current = listOptions[0][0] if listOptions else 1
        else:
            # Single channel
            channel, CRlist, PRlist, BWlist = listOptions
            self.channel_Current = channel
            self.dict_CR[channel] = CRlist
            self.dict_PR[channel] = PRlist
            self.dict_BW[channel] = BWlist
        
        self._setPotentiostatConnected(True)
        self._refreshTechOptions()

    @errorDeco(logger='self.Log')
    def updateChannelOption(self,channelList):
        channels_frame = getattr(self, "fram_Channels", None) or getattr(self, "frame_Channels", None)
        channels_layout = channels_frame.layout() if channels_frame is not None else None
        if channels_frame is not None and channels_layout is None:
            channels_layout = QVBoxLayout(channels_frame)
            channels_layout.setContentsMargins(0, 0, 0, 0)

        for button in self.group_ChannelRbtn.buttons():
            self.group_ChannelRbtn.removeButton(button)
            button.setParent(None)
            button.deleteLater()
        self.dict_ChannelRbtn.clear()

        for channel in channelList:
            channelRbutton=QRadioButton(f"CH {channel}")
            channelRbutton.objectName=f"radioButton_CH{channel}"
            if channels_layout is not None:
                channels_layout.addWidget(channelRbutton)
            elif hasattr(self, "formLayout_Channel"):
                self.formLayout_Channel.addWidget(channelRbutton)
            self.dict_ChannelRbtn[channel]=channelRbutton
            self.group_ChannelRbtn.addButton(channelRbutton, channel)
            self.dict_ChannelStatus[channel]=False  
        self.channel_Current=channelList[0]
        self.group_ChannelRbtn.button(self.channel_Current).setChecked(True)


    # Start potentiostat thread
    @errorDeco(logger='self.Log')
    def connectPs(self):
        if hasattr(self, 'bio_thread') and self.bio_thread.isRunning():
            self.logMsg("> Potentiostat thread is already running.")
            return
        
        self.bio_thread = QThread(self)
        self.bio_worker = Biologic(self.address_PS, self.path_BinaryPS)
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
        channel = self.group_ChannelRbtn.id(btn)
        self.channel_Current = channel
        self._clearTreeWidget()
        self._clearPSFrameWidget(self.frame_ps)
        sequence = self.dict_ChannelTechs.get(channel, {})
        if sequence:
            for item, page in sequence.items():
                self.treeWidget_Techs.addTopLevelItem(item)
            first_item = self.treeWidget_Techs.topLevelItem(0)
            if first_item is not None:
                self.treeWidget_Techs.setCurrentItem(first_item)
                self.TreeItemClicked(first_item, 0)
                
    #---------------- Helper functions ----------------

    def _clearPSFrameWidget(self, widget: QWidget):
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

    def _clearTreeWidget(self):
        while self.treeWidget_Techs.topLevelItemCount() > 0:
            self.treeWidget_Techs.takeTopLevelItem(0)

    def _buildTechPage(self, ui_class, item: QTreeWidgetItem, *, i_ranges: list[str] | None = None) -> QWidget:
        try:
            obj = ui_class(i_ranges=i_ranges)
        except TypeError:
            obj = ui_class()
        if hasattr(obj, "nameChanged") and isinstance(obj.nameChanged, Signal):
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
        if self.channel_Current in self.dict_ChannelTechs:
            page = self.dict_ChannelTechs[self.channel_Current].pop(item, None)
            if page is not None:
                page.setParent(None)
                page.deleteLater()

    def _onTechItemsReordered(self):
        if self.channel_Current not in self.dict_ChannelTechs:
            return
        # Reorder the dict to match the full tree order (top-level + children)
        new_dict = {}
        for item in self._iter_tree_items():
            if item in self.dict_ChannelTechs[self.channel_Current]:
                new_dict[item] = self.dict_ChannelTechs[self.channel_Current][item]
        self.dict_ChannelTechs[self.channel_Current] = new_dict

    def _setPotentiostatConnected(self, connected: bool):
        self.is_PSConnected = connected
        self._updateStatusBar()

    # def _initPlotWidgets(self):
    #     # Create the plotter widget
    #     self.plotter = ElectrochemPlotter()
    #     self.verticalLayout_Plot.addWidget(self.plotter)
    #     # Connect signals
    #     self.plotter.tech_combo.currentTextChanged.connect(self._onPlotTechSelectionChanged)
    #     self.plotter.x_combo.currentTextChanged.connect(lambda _: self._renderSelectedPlot())
    #     self.plotter.y_combo.currentTextChanged.connect(lambda _: self._renderSelectedPlot())
    #     self.plotter.axisUnitChanged.connect(self._on_axis_unit_changed)

    # def _on_axis_unit_changed(self, axis, unit):
    #     # Re-render the plot with new units
    #     self._renderSelectedPlot()

    # def _onBiologicData(self, tech_name: str, output):
    #     self.currentMeasuredTech = tech_name
    #     self.plotDataByTech.setdefault(tech_name, []).append(output)
    #     self.new_data_available = True

    # def _setPlotTechItemsFromSequence(self, sequence: list):
    #     previousSelection = self.plotter.tech_combo.currentText()
    #     self.plotter.tech_combo.blockSignals(True)
    #     self.plotter.tech_combo.clear()
    #     self.plotter.tech_combo.addItem("Current Tech")

    #     seen = set()
    #     for measurement in sequence:
    #         tech_name = str(measurement.get("technique", "")).upper()
    #         if not tech_name or tech_name in seen:
    #             continue
    #         seen.add(tech_name)
    #         self.plotter.tech_combo.addItem(tech_name)

    #     if previousSelection and self.plotter.tech_combo.findText(previousSelection) >= 0:
    #         self.plotter.tech_combo.setCurrentText(previousSelection)
    #     else:
    #         self.plotter.tech_combo.setCurrentText("Current Tech")
    #     self.plotter.tech_combo.blockSignals(False)
    #     self._configureAxisCombosForSelectedTech()

    # def _onPlotTechSelectionChanged(self, _selected: str):
    #     self._configureAxisCombosForSelectedTech()
    #     self._renderSelectedPlot()

    # def _configureAxisCombosForSelectedTech(self):
    #     selectedTech = self.plotter.tech_combo.currentText()
    #     if not selectedTech:
    #         self.plotter.x_combo.clear()
    #         self.plotter.y_combo.clear()
    #         self.plotXAxisOptions = {}
    #         self.plotYAxisOptions = {}
    #         return

    #     techForAxes = self.currentMeasuredTech if selectedTech == "Current Tech" else selectedTech
    #     if not techForAxes:
    #         return

    #     axis_options = get_axis_options(normalize_technique_name(techForAxes))
    #     x_options = axis_options.get("x", [])
    #     y_options = axis_options.get("y", [])

    #     if not x_options or not y_options:
    #         return

    #     previousX = self.plotter.x_combo.currentText()
    #     previousY = self.plotter.y_combo.currentText()

    #     self.plotXAxisOptions = {option.label: option for option in x_options}
    #     self.plotYAxisOptions = {option.label: option for option in y_options}

    #     self.plotter.x_combo.blockSignals(True)
    #     self.plotter.y_combo.blockSignals(True)
    #     self.plotter.x_combo.clear()
    #     self.plotter.y_combo.clear()
    #     self.plotter.x_combo.addItems(list(self.plotXAxisOptions.keys()))
    #     self.plotter.y_combo.addItems(list(self.plotYAxisOptions.keys()))
    #     if previousX in self.plotXAxisOptions:
    #         self.plotter.x_combo.setCurrentText(previousX)
    #     if previousY in self.plotYAxisOptions:
    #         self.plotter.y_combo.setCurrentText(previousY)
    #     self.plotter.x_combo.blockSignals(False)
    #     self.plotter.y_combo.blockSignals(False)

    # def _renderSelectedPlot(self):
    #     selectedTech = self.plotter.tech_combo.currentText()
    #     techToPlot = self.currentMeasuredTech if selectedTech == "Current Tech" else selectedTech

    #     if not techToPlot:
    #         self._clearPlot("No tested data")
    #         return

    #     rows = self.plotDataByTech.get(techToPlot, [])
    #     if not rows:
    #         self._clearPlot(f"No tested data for {techToPlot}")
    #         return

    #     sample = next((row for row in rows if isinstance(row, dict) and row), None)
    #     if sample is None:
    #         self._clearPlot(f"No plottable data for {techToPlot}")
    #         return

    #     availableKeys = list(sample.keys())
    #     self._syncAxisCombo(self.plotter.x_combo, availableKeys, prefer="t")
    #     self._syncAxisCombo(self.plotter.y_combo, availableKeys, prefer="Ewe")

    #     xKey = self.plotter.x_combo.currentText()
    #     yKey = self.plotter.y_combo.currentText()
    #     if not xKey or not yKey:
    #         self._clearPlot(f"No axis selected for {techToPlot}")
    #         return

    #     # Determine axis types
    #     x_type = 'time' if 't' in xKey.lower() else 'other'
    #     y_type = 'current' if 'i' in yKey.lower() else ('potential' if 'e' in yKey.lower() or 'v' in yKey.lower() else 'other')
    #     self.plotter.set_axis_types(x_type, y_type)

    #     xAxisOption = self.plotXAxisOptions.get(xKey)
    #     yAxisOption = self.plotYAxisOptions.get(yKey)

    #     xData = []
    #     yData = []
    #     for row in rows:
    #         if not isinstance(row, dict):
    #             continue
    #         try:
    #             if xAxisOption and yAxisOption:
    #                 xRaw = row.get(xAxisOption.source)
    #                 yRaw = row.get(yAxisOption.source)
    #                 if xRaw is None or yRaw is None:
    #                     continue
    #                 xVal = apply_axis_transform(xAxisOption.transform, float(xRaw))
    #                 yVal = apply_axis_transform(yAxisOption.transform, float(yRaw))
    #             else:
    #                 xVal = row.get(xKey)
    #                 yVal = row.get(yKey)
    #                 if xVal is None or yVal is None:
    #                     continue
    #                 xVal = float(xVal)
    #                 yVal = float(yVal)

    #             if xVal is None or yVal is None:
    #                 continue
    #             xData.append(xVal)
    #             yData.append(yVal)
    #         except (TypeError, ValueError):
    #             continue

    #     if not xData:
    #         self._clearPlot(f"No numeric points for {techToPlot}")
    #         return

    #     # Apply unit scaling
    #     xData = self._scale_data(xData, self.plotter.current_x_unit, x_type)
    #     yData = self._scale_data(yData, self.plotter.current_y_unit, y_type)

    #     # Downsample if too many points
    #     if len(xData) > 1000:
    #         xData, yData = self._downsample(xData, yData, 1000)

    #     self.plotter.ax.clear()
    #     self.plotter.ax.plot(xData, yData)
    #     self.plotter.ax.set_title(f"{techToPlot}")
    #     self.plotter.ax.set_xlabel(f"{xKey} ({self.plotter.current_x_unit})")
    #     self.plotter.ax.set_ylabel(f"{yKey} ({self.plotter.current_y_unit})")
    #     self.plotter.ax.grid(True)
    #     self.plotter.canvas.draw_idle()

    # def _scale_data(self, data, unit, axis_type):
    #     if axis_type == 'current':
    #         # Data in mA
    #         if unit == 'A':
    #             return [v / 1000 for v in data]
    #         elif unit == 'mA':
    #             return data
    #         elif unit == 'uA':
    #             return [v * 1000 for v in data]
    #         elif unit == 'nA':
    #             return [v * 1000000 for v in data]
    #     elif axis_type == 'potential':
    #         # Data in V
    #         if unit == 'V':
    #             return data
    #         elif unit == 'mV':
    #             return [v * 1000 for v in data]
    #         elif unit == 'uV':
    #             return [v * 1000000 for v in data]
    #     elif axis_type == 'time':
    #         # Data in s
    #         if unit == 's':
    #             return data
    #         elif unit == 'ms':
    #             return [v * 1000 for v in data]
    #         elif unit == 'us':
    #             return [v * 1000000 for v in data]
    #     return data

    # def _downsample(self, x_data, y_data, max_points):
    #     if len(x_data) <= max_points:
    #         return x_data, y_data
    #     step = len(x_data) // max_points
    #     x_down = x_data[::step]
    #     y_down = y_data[::step]
    #     return x_down, y_down

    # def _syncAxisCombo(self, combo, keys: list[str], *, prefer: str):
    #     current = combo.currentText()
    #     if [combo.itemText(i) for i in range(combo.count())] == keys:
    #         if current in keys:
    #             combo.setCurrentText(current)
    #         return

    #     combo.blockSignals(True)
    #     combo.clear()
    #     combo.addItems(keys)
    #     if prefer in keys:
    #         combo.setCurrentText(prefer)
    #     elif current in keys:
    #         combo.setCurrentText(current)
    #     combo.blockSignals(False)

    # def _clearPlot(self, title: str):
    #     self.plotter.ax.clear()
    #     self.plotter.ax.set_title(title)
    #     self.plotter.ax.grid(True)
    #     self.plotter.canvas.draw_idle()

    def _updateStatusBar(self):
        message = f"Potentiostat Channel: {self.channel_Current}" if self.is_PSConnected else "Potentiostat Disconnected"
        self.statusBar().showMessage(message)
    
    def _refreshTechOptions(self):
        current_dictTechs = self.dict_ChannelTechs.get(self.channel_Current, {})
        for page in current_dictTechs.values():
            if hasattr(page, "setCR") and self.channel_Current in self.dict_CR:
                page.setCR(self.dict_CR[self.channel_Current])
            if hasattr(page, "setPR") and self.channel_Current in self.dict_PR:
                page.setPR(self.dict_PR[self.channel_Current])
            if hasattr(page, "setBW") and self.channel_Current in self.dict_BW:
                page.setBW(self.dict_BW[self.channel_Current])

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
