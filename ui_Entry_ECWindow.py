#& "C:\Users\chrst\AppData\Roaming\Python\Python313\Scripts\pyside6-uic.exe" "uiEC.ui" "-o" "uiEC.py" "--from-imports"
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QApplication, QWidget,QTreeWidget,QTreeWidgetItem,QPushButton,QHBoxLayout,QLabel,QMainWindow,QTabWidget, QTabBar,QDockWidget,QVBoxLayout, QPlainTextEdit, QLineEdit
from PySide6.QtCore import QSize, Qt, QEvent, QMimeData, QModelIndex, QPoint, QRect, QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QAbstractItemView 
from PySide6.QtGui import QMouseEvent,QDrag,QFont,QShortcut,QCursor,QAction,QKeySequence
from qt_ECO_Main import Ui_MainWindow

from misc_handleException import exception2msg, msg2file, errorDeco

from misc_ModifiedUI import TechTreeWidget, FloatingTabWindow  

from ui_CV import CV as CVUI
from ui_CA import CA as CAUI 
from ui_CP import CP as CPUI
from ui_OCV import OCV as OCVUI
from ui_EIS import EIS as EISUI
from qt_Move import Ui_Form as MoveUI
from qt_Loop import Ui_Form as LoopUI
from ui_PsInfoDialog import get_potentiostat_info_from_dialog

from pt_biologic import Biologic

class ECO_pot(QMainWindow, Ui_MainWindow):
    def __init__(self):
        CR=None
        PR=None
        BW=None
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
        self.restyle()
        self.bindEvent()
        self.bindSignalSlot()
        self.showMaximized()
      
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
        
        # Setup potentiostat section - add placeholder for tech details
        self._clearWidget(self.frame_pot)
        

    @errorDeco(logger='self.Log')
    def addTech(self,sender,event):
        item=QTreeWidgetItem([sender.text()],i_ranges=)
        item.setSizeHint(0,QSize(0,30))
        font = QFont()
        font.setPointSize(14)      
        item.setFont(0, font) 
        self.treeWidget.addTopLevelItem(item)
        
        # Remove all widgets from the potentiostat section before loading new Form
        self._clearWidget(self.frame_pot)

        ui_class = self.dicTechWin.get(sender.text())
        page = self._buildTab(ui_class,item)     # QWidget ready
        self.frame_pot.layout().addWidget(page)
        self.itemTechPair[item] = page

    #---------------- Signal-Slot binding ----------------

    def bindSignalSlot(self):
        # Show the tech setup for the clicked tree item
        self.treeWidget.itemClicked.connect(self.TreeItemClicked)
        self.pushButtonStart.clicked.connect(self.startTech)
        self.pushButtonConnect.clicked.connect(self.startPotentiostat)
        self.pushButtonPsInfo.clicked.connect(self.configurePotentiostat)

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
        for item in self.treeWidget.findItems("", Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive):
            page=self.itemTechPair.get(item)
            if page is not None:
                self.sequence.append(page.outputParam())
        if hasattr(self, 'bio_worker'):
            self.bio_worker.runSequence(self.sequence)
        else:
            self.logMsg("> Potentiostat not connected.")

    # Start potentiostat thread
    @errorDeco(logger='self.Log')
    def startPotentiostat(self):
        def setCR(SignalData):
            channel, CRlist = SignalData
            for item in self.treeWidget.findItems("", Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive):
                page=self.itemTechPair.get(item)
                if page is not None and hasattr(page, "comboBoxCR"):
                    page.comboBoxCR.clear()
                    page.comboBoxCR.addItems(CRlist)
                    self.CRdic={channel:CRlist}

        self.bio_thread = QThread(self)
        self.bio_worker = Biologic(self.ps_address, self.ps_binary_path, self.ps_channel)
        self.bio_worker.moveToThread(self.bio_thread)

        self.bio_thread.started.connect(self.bio_worker.connectDevice)
        self.bio_worker.signalCR.connect(setCR)
        self.bio_worker.signalPR.connect(lambda PRlist: setattr(self, 'PR', PRlist))
        self.bio_worker.signalBW.connect(lambda BWlist: setattr(self, 'BW', BWlist))
        self.bio_worker.signalLog.connect(self.Log.appendPlainText)
        self.bio_thread.finished.connect(self.bio_thread.deleteLater)

        self.bio_thread.start()


    def logMsg(self, msg:str):
        self.Log.appendPlainText(msg)

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

    def _buildTab(self, ui_class,item:QTreeWidgetItem) -> QWidget:
        obj = ui_class()
        if hasattr(ui_class, "nameChanged"):
            obj.nameChanged.connect(lambda new_name, item=item: item.setText(0, new_name))
        if hasattr(obj, "setupUi") and not isinstance(obj, QWidget):
            container = QWidget()
            obj.setupUi(container)
            return container
        return obj
    
    def closeEvent(self, event):
        if hasattr(self, 'bio_thread') and self.bio_thread.isRunning():
            self.bio_worker.api.Disconnect(self.bio_worker.id_)
            self.bio_thread.quit()
            self.bio_thread.wait()
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
