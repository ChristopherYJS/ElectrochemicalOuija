#& "C:\Users\chrst\AppData\Roaming\Python\Python313\Scripts\pyside6-uic.exe" "uiEC.ui" "-o" "uiEC.py" "--from-imports"
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QApplication, QWidget,QTreeWidget,QTreeWidgetItem,QPushButton,QHBoxLayout,QLabel,QMainWindow,QTabWidget, QTabBar,QDockWidget,QVBoxLayout
from PySide6.QtCore import QSize, Qt, QEvent,QMimeData,QModelIndex,QPoint
from PySide6.QtWidgets import QAbstractItemView 
from PySide6.QtGui import QMouseEvent,QDrag,QFont
from qt_ECO_Main import Ui_MainWindow

from misc_PrintException import print_ex
from qt_CV import Ui_Form as CVUI
from ui_CA import CA as CAUI 
from ui_CP import CP as CPUI
from qt_EIS import Ui_Form as EISUI
from qt_Move import Ui_Form as MoveUI
from qt_Loop import Ui_Form as LoopUI

class ECO_pot(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.dicTechWin={
            'CA':CAUI,
            'CP':CPUI,
            'CV':CVUI,
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
        self.splitter.insertWidget(0, self.treeWidget)
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
        self.tabWidgetTop.addTab(QWidget(),"tabTech")
        self.tabWidgetTop.addTab(QWidget(),"tabLog")
        #Replace the bottom tabwidget
        oldTabWidgetBtm=self.tabWidgetBtm
        self.tabWidgetBtm= TockWidget(self,oldTabWidgetBtm.parent())
        self.splitter2.insertWidget(1, self.tabWidgetBtm)
        self.tabWidgetBtm.setGeometry(oldTabWidgetBtm.geometry())
        self.tabWidgetBtm.setObjectName(oldTabWidgetBtm.objectName())
        oldTabWidgetBtm.deleteLater()
        self.tabWidgetBtm.addTab(QWidget(),"tabPosition")

        

    def addTech(self,sender,event):
        item=QTreeWidgetItem([sender.text()])
        item.setSizeHint(0,QSize(0,30))
        font = QFont()
        font.setPointSize(14)      # e.g. 11-pt font
        item.setFont(0, font) 
        self.treeWidget.addTopLevelItem(item)
        
        # use the Designer dockWidget placeholder directly
        if not hasattr(self, 'tabWidgetTop'):
            print_ex(AttributeError("ECO_pot has no attribute 'tabWidgetTop', The tabWidget might has been removed by accident"))
        if not hasattr(self, 'tabWidgetBtm'):
            print_ex(AttributeError("ECO_pot has no attribute 'tabWidgetBtm', The tabWidget might has been removed by accident"))
        
        #Find if tabTech exists in any of the two tabwidgets
        tabTech = (self.tabWidgetTop._findTabByTitle("tabTech")
               or self.tabWidgetBtm._findTabByTitle("tabTech"))
        if  tabTech is None:
            w = QWidget()
            self.tabWidgetTop.addTab(w, "tabTech")
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
        # Binding the signals and slots
        self.pushBtnProceed.clicked.connect(lambda sender=self.pushBtnProceed: Proceed(sender))
        # itemClicked emits (QTreeWidgetItem, int). Connect handler that accepts both args.
        # Connect directly so the slot can accept (item, column).
        self.treeWidget.itemClicked.connect(self.TreeItemClicked)
    
    def bindEvent(self):
        for label in self.scrollAreaOption.findChildren(QLabel):
            label.mouseDoubleClickEvent=lambda e, sender=label: self.addTech(sender,e)
        
    #---------------- Slot functions ----------------  

    def TreeItemClicked(self, item, column=None):
        page = self.itemTechPair.get(item)

        tabTech = (self.tabWidgetTop._findTabByTitle("tabTech")
                or self.tabWidgetBtm._findTabByTitle("tabTech"))
        if tabTech is None:
            w = QWidget()
            self.tabWidgetTop.addTab(w, "tabTech")
            tabTech = w

        self._clearWidget(tabTech)  # removes children AND clears layout
        tabTech.layout().addWidget(page)
        self.tabWidgetTop.setCurrentWidget(tabTech)


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

class TearOffTabBar(QTabBar):
    def __init__(self, host_mainwindow: QMainWindow, parent=None):
        super().__init__(parent)
        self._host = host_mainwindow
        self._drag_start_pos = QPoint()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_start_pos = e.pos()
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if not (e.buttons() & Qt.LeftButton):
            return super().mouseMoveEvent(e)

        if (e.pos() - self._drag_start_pos).manhattanLength() < 8:
            return super().mouseMoveEvent(e)

        idx = self.tabAt(self._drag_start_pos)
        if idx < 0:
            return super().mouseMoveEvent(e)

        # If pointer left the tab bar rect, treat as "tear off"
        if not self.rect().contains(e.pos()):
            self._tear_off(idx)
            return

        super().mouseMoveEvent(e)

    def _tear_off(self, idx: int):
        tw: TockWidget = self.parent()
        page = tw.widget(idx)
        title = tw.tabText(idx)
        tw.removeTab(idx)

        dock = QDockWidget(title, self._host)
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
    def _return_to_tabs(self, dock: QDockWidget, title: str):
        page = dock.widget()
        dock.setWidget(None)
        dock.close()       # hides & frees chrome; delete if you prefer
        # choose target tab widget; here: top
        self._host.tabWidgetTop.addTab(page, title)
        self._host.tabWidgetTop.setCurrentWidget(page)
        


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
        print_ex(ex)