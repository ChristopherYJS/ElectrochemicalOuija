#& "C:\Users\chrst\AppData\Roaming\Python\Python313\Scripts\pyside6-uic.exe" "uiEC.ui" "-o" "uiEC.py" "--from-imports"
import sys, os, csv, types, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QWidget,QTreeWidget,QTreeWidgetItem,QPushButton,QHBoxLayout,QLabel,QMainWindow,QTabWidget, QTabBar,QDockWidget,QVBoxLayout, QPlainTextEdit, QRadioButton,QMessageBox, QButtonGroup, QInputDialog, QDialog, QDialogButtonBox, QCheckBox, QFileDialog
from PySide6.QtCore import QSize, Qt, QEvent, QMimeData, QModelIndex, QPoint, QRect, QObject, QThread, Signal, Slot, QTimer
from PySide6.QtWidgets import QAbstractItemView 
from PySide6.QtGui import QMouseEvent,QDrag,QFont,QShortcut,QCursor,QAction,QKeySequence

from misc_handleException import exception2msg, msg2file, errorDeco
from misc_ModifiedUI import TechTreeWidget

from ps_biologic import Biologic

from UIFiles.qt_ECO_Main import Ui_MainWindow
from UIModification.misc_BaseTech import MOTech
from UIModification.ui_CV import CV as CVUI
from UIModification.ui_CA import CA as CAUI 
from UIModification.ui_CP import CP as CPUI
from UIModification.ui_OCV import OCV as OCVUI
from UIModification.ui_EIS import EIS as EISUI
from UIModification.ui_Loop import Loop as LoopUI
from UIModification.ui_Move import Move as MoveUI

from test_defaultSeq import buildTestSequence



class ECO_pot(QMainWindow, Ui_MainWindow):
    requestRunSequence = Signal(object, object)
    requestDisconnect = Signal()
    requestStopChannels = Signal(list)
    def __init__(self):
        super().__init__()
        self.tech_ui_classes={
            'CA':CAUI,
            'CP':CPUI,
            'CV':CVUI,
            'OCV':OCVUI,
            'EIS':EISUI,
            'Move':MoveUI,
            'Loop':LoopUI
        }
        self.channel_pages={} # QTreeWidgetItem and MOTech pair of each channel. {<channel number>: {<QTreeWidgetItem>: <MOTech subclass instance>}}
        self.channel_params={} #Tech params for each channel. {<channel number>: {<tech attribute>: <value>}}
        self.channel_is_running={} #status of each channel. {<channel number>: <bool>}

        self.address_ps = "192.168.2.2"
        self.channel_active = 1 #channel number of whose setup is being displayed
        self.binary_path_ps = os.environ.get("ECLIB_DIR", f"C:{os.sep}EC-Lab Development Package{os.sep}lib")

        self.channel_current_ranges={} #current ranges for each channel
        self.channel_potential_ranges={} #potential ranges for each channel
        self.channel_bandwidths={} #bandwidth options for each channel

        self.channel_radio_buttons={} #channel number to its radio button widget in the UI
        self.channel_radio_group=QButtonGroup(self)
        self.channel_radio_group.setExclusive(True)

        self.is_ps_connected = False
        self.filename_user = None #user set filename for data output
        
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
    ##=====================================================================================##
    # Signal-slot binding functions
    ##=====================================================================================##
    def bindSignalSlot(self):
        # Show the tech setup for the clicked tree item
        self.treeWidget_Techs.itemClicked.connect(self.TreeItemClicked)
        self.treeWidget_Techs.itemRemoved.connect(self._onTechItemRemoved)
        self.treeWidget_Techs.itemsReordered.connect(self._onTechItemsReordered)
        self.pushButton_SingleRun.clicked.connect(lambda: self.startChannels([self.channel_active]))
        self.pushButton_MultiRun.clicked.connect(self.selectMultiRunChannels)
        self.pushButtonConnect.clicked.connect(self.connectPS)
        self.pushButton_ErrorTest.clicked.connect(self.errorTest)
        self.pushButton_3.clicked.connect(lambda: buildTestSequence(self))
        self.lineEditLogInput.returnPressed.connect(self.evalLogInput)
        self.channel_radio_group.buttonToggled.connect(lambda btn: self.switchChannel(btn) )
        self.pushButton_StopSingle.clicked.connect(lambda: self.stopChannel([self.channel_active]))
        self.pushButton_StopAll.clicked.connect(lambda: self.stopChannel(list(self.channel_is_running.keys()))) 
    ##=====================================================================================##
    # Tech label binding functions
    ##=====================================================================================##
    def bindTechLabels(self):
        for label in self.scrollAreaOption_Techs.findChildren(QLabel):
            label.mouseDoubleClickEvent=lambda e, sender=label: self.addTech(sender,e)

    def errorTest(self):
        sequence = self._buildSequence(self.channel_active)
        if not sequence:
            return
        print("Tech Sequence:")
        for idx, page in enumerate(sequence):
            techname = page.tech
            expname = page.name
            loop = page.loop
            print(f"{idx+1}. CH{self.channel_active}_{techname}_{expname}_loop{loop}")
        
    ##=====================================================================================##
    # Potentiostat related
    ##=====================================================================================##

    @errorDeco(logger='self.Log')
    def connectPS(self):
        if hasattr(self, 'bio_thread') and self.bio_thread.isRunning():
            self.logMsg("> Potentiostat thread is already running.")
            return
        
        self.bio_thread = QThread(self)
        self.bio_worker = Biologic(self.address_ps, self.binary_path_ps)
        self.bio_worker.moveToThread(self.bio_thread)

        self.bio_thread.started.connect(self.bio_worker.connectDevice)
        self.bio_thread.finished.connect(lambda: self._setPotentiostatConnected(False))
        self.bio_thread.finished.connect(self.bio_thread.deleteLater)

        # self.bio_worker.signalData.connect(self._onBiologicData)
        self.bio_worker.signalConnected.connect(self._getChannelInfo)
        self.bio_worker.signalChannelOption.connect(self.updateChannelOption)
        self.bio_worker.signalFinished.connect(self.bio_thread.quit)
        self.bio_worker.signalLog.connect(self.Log.appendPlainText)
        self.requestRunSequence.connect(self.bio_worker.runSequence, Qt.ConnectionType.QueuedConnection)
        self.requestDisconnect.connect(self.bio_worker.disconnectDevice, Qt.ConnectionType.QueuedConnection)
        self.requestStopChannels.connect(self.bio_worker.stopExperiment, Qt.ConnectionType.QueuedConnection)
        self.bio_thread.start()

    @errorDeco(logger='self.Log')
    def addTech(self,sender,event) -> None:
        #Add a technique to the sequence tree when its label is double-clicked in the UI.
        if self.is_ps_connected and not self.channel_is_running.get(self.channel_active): 
            if self.channel_active not in self.channel_pages:
                self.channel_pages[self.channel_active] = {}
            i_ranges = self.channel_current_ranges.get(self.channel_active, [])

            # If a loop item is focused, add new technique as its child; otherwise, add as a new top-level item
            tree_widget_focused = self.treeWidget_Techs.currentItem()
            target_parent = None
            if tree_widget_focused is not None:
                current_page = self.channel_pages[self.channel_active].get(tree_widget_focused)
                if current_page and getattr(current_page, "tech", "") == "Loop":
                    target_parent = tree_widget_focused

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

            ui_class = self.tech_ui_classes.get(sender.text())
            page = self._buildTechPage(ui_class, item, i_ranges=i_ranges)     
            self.frame_ps.layout().addWidget(page)
            self.channel_pages[self.channel_active][item] = page
            self._ensureUniqueTechName(page, item, self.channel_active)
            self.treeWidget_Techs.setCurrentItem(item)
            if hasattr(page, "setCR") and self.channel_active in self.channel_current_ranges:
                page.setCR(self.channel_current_ranges[self.channel_active])
            if hasattr(page, "setPR") and self.channel_active in self.channel_potential_ranges:
                page.setPR(self.channel_potential_ranges[self.channel_active])
            if hasattr(page, "setBW") and self.channel_active in self.channel_bandwidths:
                page.setBW(self.channel_bandwidths[self.channel_active])
        else:
            #pop warning window to inform user to connect potentiostat or free the channel
            warning_msg = "Please connect to the potentiostat and ensure the channel is free before editing experiment sequence."
            QMessageBox.warning(self, "Cannot Add Technique", warning_msg) 
    

    @errorDeco(logger='self.Log')
    def TreeItemClicked(self, item, column=None):
        '''
        show the technique setup page in the potentiostat section when its item is clicked in the tree widget
        '''
        page = self.channel_pages.get(self.channel_active, {}).get(item)
        self._clearPSFrameWidget(self.frame_ps)
        self.frame_ps.layout().addWidget(page)
        page.show()

    @errorDeco(logger='self.Log')
    def startChannels(self,channels):
        '''
        send param sequence(s) to selected channel(s) to biologic to run
        '''
        #check if potentiostat is connected
        if not self.is_ps_connected:
            self.logMsg("> Potentiostat not connected.")
            return
        # Get save path + base filename from user (UI thread)
        default_name = f"{time.strftime('%Y%m%d')}.csv"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Experiment Data Series",
            default_name,
            "CSV Files (*.csv);;All Files (*.*)"
        )
        if not filename:
            return
        self.filename_user = os.path.splitext(filename)[0]

        # Build sequence for the selected channel and start the experiment
        self.channel_params = {}
        for ch in channels:
            if self.channel_is_running.get(ch, False):
                self.logMsg(f"> Channel {ch} is currently running.")
                return
            sequence_params = self._buildSequence(ch)
            if not sequence_params:
                self.logMsg(f"> Sequence build cancelled on CH {ch} due to invalid technique input.")
                return
            self.channel_params[ch] = sequence_params

        self.requestRunSequence.emit(self.channel_params, self.filename_user)
        self.channel_is_running.update(
            getattr(self.bio_worker, 'channel_is_running', {ch: True for ch in self.channel_params})
        )
        self.logMsg(f"> Starting single-channel run on CH {'&'.join(list(map(str, self.channel_params.keys())))}")

    @errorDeco(logger='self.Log')
    def selectMultiRunChannels(self) -> list[int]:
        '''
        Show a dialog to select multiple channels for running experiments.
        '''
        connected_channels = sorted(self.channel_is_running.keys())
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
            checkbox.setChecked(self.channel_is_running.get(channel, False))
            checkbox.setEnabled(not self.channel_is_running.get(channel, False))
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
        else:
            self.startChannels(selected_channels)

    @errorDeco(logger='self.Log')
    def _buildSequence(self, channel: int, parent=None, path_current=None) -> list[dict]:
        """
        Build the tech sequence for ONE given channel by traversing the tree widget. 

        This builds the sequence for both biologic to run and to output correct filename. 
        I dont know how this works but it works, so don't change it.
        """
        seq = []

        if path_current is None:
            path_current = [1]

        self._pruneChannelPages(channel)
        channel_pages = self.channel_pages.get(channel, {})

        if parent is None:
            items = [self.treeWidget_Techs.topLevelItem(i) for i in range(self.treeWidget_Techs.topLevelItemCount())]
        else:
            items = [parent.child(i) for i in range(parent.childCount())]

        for item in items:
            if item is None:
                continue

            page = channel_pages.get(item)
            if page is None:
                continue

            if page.tech == "Loop":
                loop_param = page.outputParam()
                iterations = int(loop_param.get('iterations', 1))
                for i in range(1, iterations + 1):
                    loop_seq = self._buildSequence(channel, item, path_current + [i])
                    if not loop_seq:
                        return []
                    seq.extend(loop_seq)
                continue

            page.loop = path_current.copy()
            frozen_param = page.outputParam()
            if not frozen_param:
                return []

            frozen_param = dict(frozen_param)
            frozen_param['loop'] = path_current.copy()
            seq.append(frozen_param)

        return seq

        
    @errorDeco(logger='self.Log')
    def _getChannelInfo(self, listOptions):
        if listOptions and isinstance(listOptions[0], list):
            # Multiple channels: list of [channel, CRlist, PRlist, BWlist]
            for options in listOptions:
                channel, cr_list, pr_list, bw_list = options
                self.channel_current_ranges[channel] = cr_list
                self.channel_potential_ranges[channel] = pr_list
                self.channel_bandwidths[channel] = bw_list
            # Set default channel to the first available
            self.channel_active = listOptions[0][0] if listOptions else 1
        else:
            # Single channel
            channel, cr_list, pr_list, bw_list = listOptions
            self.channel_active = channel
            self.channel_current_ranges[channel] = cr_list
            self.channel_potential_ranges[channel] = pr_list
            self.channel_bandwidths[channel] = bw_list
        
        self._setPotentiostatConnected(True)
        self._refreshTechOptions()

    @errorDeco(logger='self.Log')
    def updateChannelOption(self,channel_list):
        channels_frame = getattr(self, "fram_Channels", None) or getattr(self, "frame_Channels", None)
        channels_layout = channels_frame.layout() if channels_frame is not None else None
        if channels_frame is not None and channels_layout is None:
            channels_layout = QVBoxLayout(channels_frame)
            channels_layout.setContentsMargins(0, 0, 0, 0)

        for button in self.channel_radio_group.buttons():
            self.channel_radio_group.removeButton(button)
            button.setParent(None)
            button.deleteLater()
        self.channel_radio_buttons.clear()

        for channel in channel_list:
            channel_rbutton=QRadioButton(f"CH {channel}")
            channel_rbutton.objectName=f"radioButton_CH{channel}"
            if channels_layout is not None:
                channels_layout.addWidget(channel_rbutton)
            elif hasattr(self, "formLayout_Channel"):
                self.formLayout_Channel.addWidget(channel_rbutton)
            self.channel_radio_buttons[channel]=channel_rbutton
            self.channel_radio_group.addButton(channel_rbutton, channel)
            self.channel_is_running[channel]=False  
        self.channel_active=channel_list[0]
        self.channel_radio_group.button(self.channel_active).setChecked(True)

    @errorDeco(logger='self.Log')
    def switchChannel(self, btn):
        channel = self.channel_radio_group.id(btn)
        self.channel_active = channel
        self._pruneChannelPages(channel)
        self._clearTreeWidget()
        self._clearPSFrameWidget(self.frame_ps)
        sequence = self.channel_pages.get(channel, {})
        if sequence:
            for item in sequence.keys():
                try:
                    if item.parent() is None:
                        self.treeWidget_Techs.addTopLevelItem(item)
                except RuntimeError:
                    continue
            first_item = self.treeWidget_Techs.topLevelItem(0)
            if first_item is not None:
                self.treeWidget_Techs.setCurrentItem(first_item)
                self.TreeItemClicked(first_item, 0)

    @errorDeco(logger='self.Log')
    def stopChannel(self, channel:list):
        self.requestStopChannels.emit(channel)
        if hasattr(self, 'bio_worker') and hasattr(self.bio_worker, 'channel_is_running'):
            self.channel_is_running.update(self.bio_worker.channel_is_running)

    ##=====================================================================================##
    # Log page
    ##=====================================================================================##
    @errorDeco(logger='self.Log')
    def logMsg(self, msg:str):
        self.Log.appendPlainText(msg)
        self.Log.verticalScrollBar().setValue(self.Log.verticalScrollBar().maximum())

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

    ##=====================================================================================##
    # Helper functions
    ##=====================================================================================##

    def _clearPSFrameWidget(self, widget: QWidget):
        layout = widget.layout()
        if layout is None:
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
        while layout.count():
            layout_item = layout.takeAt(0)
            child_widget = layout_item.widget()
            if child_widget:
                child_widget.hide()
                child_widget.setParent(None)

    def _clearTreeWidget(self):
        while self.treeWidget_Techs.topLevelItemCount() > 0:
            self.treeWidget_Techs.takeTopLevelItem(0)

    def _buildTechPage(self, ui_class, item: QTreeWidgetItem, *, i_ranges: list[str] | None = None) -> QWidget:
        try:
            obj = ui_class(i_ranges=i_ranges)
        except TypeError:
            obj = ui_class()
        if hasattr(obj, "nameChanged") and isinstance(obj.nameChanged, Signal):
            obj.nameChanged.connect(lambda new_name, item=item, page=obj: self._onTechNameChanged(item, page, new_name))
        if hasattr(obj, "setupUi") and not isinstance(obj, QWidget):
            container = QWidget()
            obj.setupUi(container)
            return container
        return obj

    def _extractTechSuffix(self, tech_type: str, display_name: str) -> str:
        name = str(display_name or "").strip()
        prefix = f"{tech_type}_"
        if not name:
            return ""
        if name.upper().startswith(prefix):
            return name[len(prefix):].strip()
        if name.upper() == tech_type:
            return ""
        return name

    def _ensureUniqueTechName(self, page, item: QTreeWidgetItem, channel: int, requested_name: str | None = None):
        tech_type = str(getattr(page, "tech", "")).upper().strip()
        if not tech_type:
            return

        taken_suffixes = set()
        for existing_item, existing_page in self.channel_pages.get(channel, {}).items():
            if existing_item is item:
                continue
            if str(getattr(existing_page, "tech", "")).upper().strip() != tech_type:
                continue
            existing_text = existing_item.text(0)
            if existing_text:
                taken_suffixes.add(self._extractTechSuffix(tech_type, existing_text))

        requested_suffix = ""
        if requested_name is not None:
            requested_suffix = self._extractTechSuffix(tech_type, requested_name)

        if not requested_suffix or requested_suffix in taken_suffixes:
            n = 1
            while str(n) in taken_suffixes:
                n += 1
            unique_suffix = str(n)
        else:
            unique_suffix = requested_suffix

        unique_display_name = f"{tech_type}_{unique_suffix}"
        page.name = unique_suffix

        if hasattr(page, "lineEditName") and page.lineEditName is not None:
            page.lineEditName.blockSignals(True)
            page.lineEditName.setText(unique_suffix)
            page.lineEditName.blockSignals(False)

        item.setText(0, unique_display_name)

    def _onTechNameChanged(self, item: QTreeWidgetItem, page, new_name: str):
        self._ensureUniqueTechName(page, item, self.channel_active, requested_name=new_name)

    def _iterTreeItems(self, parent: QTreeWidgetItem | None = None):
        if parent is None:
            for idx in range(self.treeWidget_Techs.topLevelItemCount()):
                item = self.treeWidget_Techs.topLevelItem(idx)
                if item is None:
                    continue
                yield item
                yield from self._iterTreeItems(item)
            return
        for idx in range(parent.childCount()):
            item = parent.child(idx)
            if item is None:
                continue
            yield item
            yield from self._iterTreeItems(item)

    def _isValidTreeItem(self, item: QTreeWidgetItem | None) -> bool:
        if item is None:
            return False
        try:
            item.text(0)
            return True
        except RuntimeError:
            return False

    def _iterSubtreeItems(self, root: QTreeWidgetItem | None):
        if root is None:
            return
        if not self._isValidTreeItem(root):
            return
        yield root
        for idx in range(root.childCount()):
            child = root.child(idx)
            yield from self._iterSubtreeItems(child)

    def _pruneChannelPages(self, channel: int):
        pages = self.channel_pages.get(channel)
        if not pages:
            return
        for item in list(pages.keys()):
            if self._isValidTreeItem(item):
                continue
            page = pages.pop(item, None)
            if page is not None:
                page.setParent(None)
                page.deleteLater()

    def _onTechItemRemoved(self, item: QTreeWidgetItem):
        if self.channel_active not in self.channel_pages:
            return
        pages = self.channel_pages[self.channel_active]
        for subtree_item in list(self._iterSubtreeItems(item)):
            page = pages.pop(subtree_item, None)
            if page is not None:
                page.setParent(None)
                page.deleteLater()
        self._pruneChannelPages(self.channel_active)

    def _onTechItemsReordered(self):
        if self.channel_active not in self.channel_pages:
            return
        self._pruneChannelPages(self.channel_active)
        # Reorder the dict to match the full tree order (top-level + children)
        new_dict = {}
        for item in self._iterTreeItems():
            if item in self.channel_pages[self.channel_active]:
                new_dict[item] = self.channel_pages[self.channel_active][item]
        self.channel_pages[self.channel_active] = new_dict

    def _setPotentiostatConnected(self, connected: bool):
        self.is_ps_connected = connected
        self._updateStatusBar()

    def _updateStatusBar(self):
        message = f"Potentiostat Channel: {self.channel_active}" if self.is_ps_connected else "Potentiostat Disconnected"
        self.statusBar().showMessage(message)
    
    def _refreshTechOptions(self):
        channel_active_techs = self.channel_pages.get(self.channel_active, {})
        for page in channel_active_techs.values():
            if hasattr(page, "setCR") and self.channel_active in self.channel_current_ranges:
                page.setCR(self.channel_current_ranges[self.channel_active])
            if hasattr(page, "setPR") and self.channel_active in self.channel_potential_ranges:
                page.setPR(self.channel_potential_ranges[self.channel_active])
            if hasattr(page, "setBW") and self.channel_active in self.channel_bandwidths:
                page.setBW(self.channel_bandwidths[self.channel_active])
            
    ##=====================================================================================##
    # Event functions
    ##=====================================================================================##

    def closeEvent(self, event):
        if any(self.channel_is_running.values()):
            running_channels = [str(ch) for ch, running in self.channel_is_running.items() if running]
            QMessageBox.warning(
                self,
                "Channels Running",
                f"Channel(s) {', '.join(running_channels)} are still running. Stop all running channels before closing."
            )
            event.ignore()
            return
        self.requestDisconnect.emit()
        if hasattr(self, 'bio_thread') and self.bio_thread.isRunning():
            self.bio_thread.quit()
            self.bio_thread.wait()
        event.accept()
    

        

if __name__ =='__main__':
    try:
        app_qt=QApplication(sys.argv)
        app_qt.styleHints().setColorScheme(Qt.ColorScheme.Light)
        app_qt.setStyle("Fusion")
        app=ECO_pot()
        sys.exit(app_qt.exec())
    except Exception as ex:
        error_msg = exception2msg(ex)
        print(error_msg)
        msg2file(error_msg)
