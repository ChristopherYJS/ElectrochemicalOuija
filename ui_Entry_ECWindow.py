#& "C:\Users\chrst\AppData\Roaming\Python\Python313\Scripts\pyside6-uic.exe" "uiEC.ui" "-o" "uiEC.py" "--from-imports"
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QApplication, QWidget,QTreeWidget,QTreeWidgetItem,QPushButton,QHBoxLayout,QLabel
from PySide6.QtCore import QSize, Qt, QEvent,QMimeData,QModelIndex
from PySide6.QtWidgets import QAbstractItemView 
from PySide6.QtGui import QMouseEvent,QDrag,QFont
from qt_EC import Ui_Form 
from ui_SlotFuncs import *

from misc_PrintException import print_ex
from qt_CV import Ui_Form as CVUI
from ui_CA import CA as CAUI 
from qt_CP import Ui_Form as CPUI
from qt_EIS import Ui_Form as EISUI
from qt_Move import Ui_Form as MoveUI
from qt_Loop import Ui_Form as LoopUI

class ECO_pot(QWidget, Ui_Form):
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
        

    def addTech(self,sender,event):
        item=QTreeWidgetItem([sender.text()])
        item.setSizeHint(0,QSize(0,30))
        font = QFont()
        font.setPointSize(14)      # e.g. 11-pt font
        item.setFont(0, font) 
        self.treeWidget.addTopLevelItem(item)
        ui_class = self.dicTechWin.get(sender.text())
        # use the Designer dockWidget placeholder directly
        if not hasattr(self, 'dockWidget'):
            raise AttributeError("ECO_pot has no attribute 'dockWidget' — ensure the placeholder dockWidget exists in the UI and is named 'dockWidget'")
        placeholder = self.dockWidget
        # Remove all widgets from the placeholder's layout before loading new Form
        layout = placeholder.layout()
        if layout is not None:
            while layout.count():
                item_layout = layout.takeAt(0)
                w = item_layout.widget()
                if w:
                    w.setParent(None)
                    w.deleteLater()
        # Setup the new Form directly into the placeholder
        if ui_class is None:
            print(f"No ui_class for {sender.text()}")
            return
        ui = ui_class()
        ui.setupUi(placeholder)
        self.itemTechPair[item] = ui

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
        """Handle tree item clicks.

        The QTreeWidget.itemClicked signal provides (item, column). We accept
        the optional column and safely lookup the mapped Ui helper. If found,
        we clear the placeholder dockWidget and call its setupUi to load the form.
        """
        # use the Designer dockWidget placeholder directly
        if not hasattr(self, 'dockWidget'):
            raise AttributeError("ECO_pot has no attribute 'dockWidget' — ensure the placeholder dockWidget exists in the UI and is named 'dockWidget'")
        placeholder = self.dockWidget

        # Clear placeholder layout
        layout = placeholder.layout()
        if layout is not None:
            while layout.count():
                item_layout = layout.takeAt(0)
                w = item_layout.widget()
                if w:
                    w.setParent(None)
                    w.deleteLater()

        # Try lookup by the QTreeWidgetItem object first, then fall back to the item's text
        ui = self.itemTechPair.get(item)
        if ui is None:
            ui = self.itemTechPair.get(item.text(0))
        if ui is not None:
            ui.setupUi(placeholder)

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
if __name__ =='__main__':
    try:
        Qapp=QApplication(sys.argv)
        Qapp.styleHints().setColorScheme(Qt.ColorScheme.Light)
        Qapp.setStyle("Fusion")
        app=ECO_pot()
        sys.exit(Qapp.exec())
    except Exception as ex:
        print_ex(ex)