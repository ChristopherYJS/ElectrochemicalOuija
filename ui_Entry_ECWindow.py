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
        middle_index = self.splitter_2.indexOf(self.widget)
        techWin = QWidget()
        ui = ui_class()
        ui.setupUi(techWin)
        self.itemTechPair[item] = techWin
        self.splitter_2.insertWidget(middle_index, techWin)
        self.widget.deleteLater()
        self.widget = techWin        # update reference
        try:
            if hasattr(self, 'widget') and self.widget is not None:
                self.widget.hide()
        except Exception:
           pass

    def bindSignalSlot(self):
        # Binding the signals and slots
        self.pushBtnProceed.clicked.connect(lambda sender=self.pushBtnProceed: Proceed(sender))
        self.treeWidget.itemClicked.connect(lambda item: self.TreeItemClicked(item))
        
        

    
    def bindEvent(self):
        for label in self.scrollAreaOption.findChildren(QLabel):
            label.mouseDoubleClickEvent=lambda e, sender=label: self.addTech(sender,e)
        
    #---------------- Slot functions ----------------        
    def TreeItemClicked(self,item):
        # safe lookup (won't raise if mapping is missing)
        widget = self.itemTechPair.get(item)
        if not widget:
            return
        try:
            if hasattr(self, 'widget') and self.widget is not None:
                self.widget.hide()
        except Exception:
           pass
        widget.show()
        self.widget = widget

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