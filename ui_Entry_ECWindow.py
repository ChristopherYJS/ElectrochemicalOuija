#& "C:\Users\chrst\AppData\Roaming\Python\Python313\Scripts\pyside6-uic.exe" "uiEC.ui" "-o" "uiEC.py" "--from-imports"
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QApplication, QWidget,QTreeWidget,QTreeWidgetItem,QPushButton,QHBoxLayout,QLabel,QMainWindow,QTabWidget, QTabBar,QDockWidget,QVBoxLayout, QPlainTextEdit, QLineEdit
from PySide6.QtCore import QSize, Qt, QEvent, QMimeData, QModelIndex, QPoint, QRect, QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QAbstractItemView 
from PySide6.QtGui import QMouseEvent,QDrag,QFont
from qt_ECO_Main import Ui_MainWindow

from misc_handleException import exception2msg, msg2file, errorDeco
from ui_CV import CV as CVUI
from ui_CA import CA as CAUI 
from ui_CP import CP as CPUI
from ui_OCV import OCV as OCVUI
from ui_EIS import EIS as EISUI
from qt_Move import Ui_Form as MoveUI
from qt_Loop import Ui_Form as LoopUI

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
        self.restyle()
        self.bindEvent()
        self.bindSignalSlot()
        self.showMaximized()
      
    def restyle(self):
        #Replace the treewidget in the ui file with our custom one
        oldTreeWidget =self.treeWidget
        self.treeWidget= TechTreeWidget(self.splitter)
        self.splitter.insertWidget(1, self.treeWidget)
        self.treeWidget.setGeometry(oldTreeWidget.geometry())
        self.treeWidget.setObjectName(oldTreeWidget.objectName())
        oldTreeWidget.deleteLater()
        self.treeWidget.clear()
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setAcceptDrops(True)
        self.treeWidget.setDropIndicatorShown(True)
        self.treeWidget.setDefaultDropAction(Qt.MoveAction)
        self.treeWidget.setDragDropMode(QTreeWidget.InternalMove)
        #Replace the top tabwidget
        oldTabWidgetTop =self.tabWidgetTop
        self.tabWidgetTop= TockWidget(self,oldTabWidgetTop.parent())
        self.splitter2.insertWidget(0, self.tabWidgetTop)
        self.tabWidgetTop.setGeometry(oldTabWidgetTop.geometry())
        self.tabWidgetTop.setObjectName(oldTabWidgetTop.objectName())
        oldTabWidgetTop.deleteLater()
        
        #Replace the bottom tabwidget
        oldTabWidgetBtm=self.tabWidgetBtm
        self.tabWidgetBtm= TockWidget(self,oldTabWidgetBtm.parent())
        self.splitter2.insertWidget(1, self.tabWidgetBtm)
        self.tabWidgetBtm.setGeometry(oldTabWidgetBtm.geometry())
        self.tabWidgetBtm.setObjectName(oldTabWidgetBtm.objectName())
        oldTabWidgetBtm.deleteLater()
        
        # Add tabs after both widgets are replaced
        self.tabWidgetTop.addTab(QWidget(),"ExpSequence")
        self.tabWidgetTop.addTab(QWidget(),"Positioner")
        
        # Add Log tab to bottom widget and setup Log widget
        self.Log = QPlainTextEdit()
        self.Log.setReadOnly(True)
        logTab = self.tabWidgetBtm._findTabByTitle("Log")
        if logTab is None:
            logTab = QWidget()
            self.tabWidgetBtm.addTab(logTab, "Log")
        self._clearWidget(logTab)
        logTab.layout().addWidget(self.Log)
        

    @errorDeco(logger='self.Log')
    def addTech(self,sender,event):
        item=QTreeWidgetItem([sender.text()])
        item.setSizeHint(0,QSize(0,30))
        font = QFont()
        font.setPointSize(14)      
        item.setFont(0, font) 
        self.treeWidget.addTopLevelItem(item)
        
        # use the Designer dockWidget placeholder directly
        if not hasattr(self, 'tabWidgetTop'):
            raise AttributeError("ECO_pot has no attribute 'tabWidgetTop', The tabWidget might has been removed by accident")
        if not hasattr(self, 'tabWidgetBtm'):
            raise AttributeError("ECO_pot has no attribute 'tabWidgetBtm', The tabWidget might has been removed by accident")
        
        #Find if tabTech exists in any of the two tabwidgets
        tabTech = (self.tabWidgetTop._findTabByTitle("ExpSequence")
            or self.tabWidgetBtm._findTabByTitle("ExpSequence"))
        if  tabTech is None:
            w = QWidget()
            self.tabWidgetTop.addTab(w, "ExpSequence")
            tabTech = w
        # Remove all widgets from the placeholder's layout before loading new Form
        self._clearWidget(tabTech)

        ui_class = self.dicTechWin.get(sender.text())
        page = self._buildTab(ui_class,item)     # QWidget ready
        tabTech.layout().addWidget(page)
        self.itemTechPair[item] = page
        self.tabWidgetTop.setCurrentWidget(tabTech)

    #---------------- Signal-Slot binding ----------------

    def bindSignalSlot(self):
        # Show the tech setup for the clicked tree item
        self.treeWidget.itemClicked.connect(self.TreeItemClicked)
        self.pushButtonStart.clicked.connect(self.startTech)
        self.pushButtonConnect.clicked.connect(self.startPotentiostat)
    
    def bindEvent(self):
        for label in self.scrollAreaOption.findChildren(QLabel):
            label.mouseDoubleClickEvent=lambda e, sender=label: self.addTech(sender,e)
        
    #---------------- Slot functions ----------------  
    @errorDeco(logger='self.Log')
    def TreeItemClicked(self, item, column=None):
        page = self.itemTechPair.get(item)

        tabTech = (self.tabWidgetTop._findTabByTitle("ExpSequence")
                or self.tabWidgetBtm._findTabByTitle("ExpSequence"))
        if tabTech is None:
            w = QWidget()
            self.tabWidgetTop.addTab(w, "ExpSequence")
            tabTech = w

        self._clearWidget(tabTech)  # removes children AND clears layout
        tabTech.layout().addWidget(page)
        self.tabWidgetTop.setCurrentWidget(tabTech)

    @errorDeco(logger='self.Log')
    def startTech(self):
        # if not hasattr(self, 'bio_worker') or not self.bio_worker:
        # if False:
        #     self.logMsg("> Potentiostat not connected. Please connect to the device first.")
        # else:
        # for item in self.treeWidget.findItems("", Qt.MatchContains | Qt.MatchRecursive):
        #     print(item)
                # page=self.itemTechPair.get(item)
            #     print(type(page))
            # for widget in page.findChildren(QLineEdit):
            #     print(f"{widget}: {widget.text()}")
        print('start clicked')

    # Start potentiostat thread
    @errorDeco(logger='self.Log')
    def startPotentiostat(self):
        def setCR(CRlist):
            for item in self.treeWidget.findItems("", Qt.MatchContains | Qt.MatchRecursive):
                page=self.itemTechPair.get(item)
                if hasattr(page, "comboBoxCR"):
                    page.comboBoxCR.clear()
                    page.comboBoxCR.addItems(CRlist)

        address = "192.168.2.2"
        channel = 1
        binary_path = os.environ.get("ECLIB_DIR", f"C:{os.sep}EC-Lab Development Package{os.sep}lib")

        self.bio_thread = QThread(self)
        self.bio_worker = Biologic(address, binary_path, channel)
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
            self.bio_thread.quit()
            self.bio_thread.wait()
        event.accept()
    
class TechTreeWidget(QTreeWidget):
    def dropEvent(self, event):
        target = self.itemAt(event.position().toPoint())
        # Detect nesting (dropping onto another item)
        # Allow if target is None (empty area) → reorder/top-level move
        # Allow if target.text(0) == 'Loop'
        # Ignore if target exists and is not 'Loop'
        if target and target.text(0) != 'Loop':
            drop_indicator = self.dropIndicatorPosition()
            if drop_indicator == QAbstractItemView.OnItem:  # only block nesting
                event.ignore()
                return
        super().dropEvent(event)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            item = self.currentItem()
            if item:
                parent = item.parent()
                if parent:
                    parent.removeChild(item)
                else:
                    idx = self.indexOfTopLevelItem(item)
                    self.takeTopLevelItem(idx)
        else:
            super().keyPressEvent(event)

class TearOffDockWidget(QDockWidget):
    def __init__(self, title: str, host_mainwindow: QMainWindow, tab_bar, source_tab: QTabWidget):
        super().__init__(title, host_mainwindow)
        self._host = host_mainwindow
        self._tab_bar = tab_bar
        self._source_tab = source_tab

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if not self.isFloating():
            return
        target = self._tab_bar._find_tabwidget_for_pos(event.globalPosition().toPoint(), self._source_tab)
        if target is not None:
            self._tab_bar._return_to_tabs(self, self.windowTitle(), target)

class TearOffTabBar(QTabBar):

    def __init__(self, host_mainwindow: QMainWindow, parent=None):
        super().__init__(parent)
        self._host = host_mainwindow
        self._drag_start_pos = QPoint()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_start_pos = e.position().toPoint()
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if not (e.buttons() & Qt.LeftButton):
            return super().mouseMoveEvent(e)

        if (e.position().toPoint() - self._drag_start_pos).manhattanLength() < 8:
            return super().mouseMoveEvent(e)

        idx = self.tabAt(self._drag_start_pos)
        if idx < 0:
            return super().mouseMoveEvent(e)

        # If pointer left the tab bar rect, treat as "tear off"
        if not self.rect().contains(e.position().toPoint()):
            self._tear_off(idx)
            return

        super().mouseMoveEvent(e)

    def _tear_off(self, idx: int):
        tw: TockWidget = self.parent()
        page = tw.widget(idx)
        title = tw.tabText(idx)
        tw.removeTab(idx)

        dock = TearOffDockWidget(title, self._host, self, tw)
        dock.setObjectName(f"Dock_{title}")
        dock.setWidget(page)
        dock.setFeatures(QDockWidget.DockWidgetClosable |
                        QDockWidget.DockWidgetMovable   |
                        QDockWidget.DockWidgetFloatable)
        dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        dock.setContextMenuPolicy(Qt.ActionsContextMenu)

        # Action to put the page back into the TockWidget
        act = dock.addAction("Return to Tabs")
        act.triggered.connect(lambda _, d=dock, t=title: self._return_to_tabs(d, t))

        self._host.addDockWidget(Qt.RightDockWidgetArea, dock)
        dock.setFloating(True)
        dock.show()
        dock.topLevelChanged.connect(
            lambda floating, d=dock, t=title:
                None if floating else None  # no-op; leave default docking alone
        )
        # Add a shortcut:
        act.setShortcut("Ctrl+Return")

    def _find_tabwidget_for_pos(self, global_pos: QPoint, fallback: QTabWidget | None) -> QTabWidget | None:
        candidates = []
        for name in ("tabWidgetTop", "tabWidgetBtm"):
            tw = getattr(self._host, name, None)
            if isinstance(tw, QTabWidget):
                candidates.append(tw)
        if fallback is not None and fallback not in candidates:
            candidates.append(fallback)

        for tw in candidates:
            top_left = tw.mapToGlobal(QPoint(0, 0))
            rect = QRect(top_left, tw.size())
            if rect.contains(global_pos):
                return tw
        return None

    def _return_to_tabs(self, dock: QDockWidget, title: str, target: QTabWidget | None = None):
        page = dock.widget()
        if page is None:
            return
        dock.setWidget(None)
        dock.close()       # hides & frees chrome; delete if you prefer
        if target is None:
            target = getattr(self._host, "tabWidgetTop", None)
        if target is None:
            return
        target.addTab(page, title)
        target.setCurrentWidget(page)

class TockWidget(QTabWidget):
    '''
    Dockable tab widget with tear-off tabs
    '''
    def __init__(self, host_mainwindow: QMainWindow, parent=None):
        super().__init__(parent)
        self.setTabBar(TearOffTabBar(host_mainwindow, self))
        self.setMovable(True)   # reordering inside the tab bar
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self._closeTab)

    def _findTabByTitle(self, title: str) -> QWidget | None:
        for i in range(self.count()):
            if self.tabText(i) == title:
                return self.widget(i)
        return None

    def _closeTab(self, index: int):
        self.removeTab(index)
        

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
