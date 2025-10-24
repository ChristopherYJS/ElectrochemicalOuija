#& "C:\Users\chrst\AppData\Roaming\Python\Python313\Scripts\pyside6-uic.exe" "uiEC.ui" "-o" "uiEC.py" "--from-imports"
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QApplication, QWidget,QTreeWidget,QTreeWidgetItem,QPushButton,QHBoxLayout,QLabel
from PySide6.QtCore import QSize, Qt, QEvent,QMimeData,QModelIndex
from PySide6.QtWidgets import QAbstractItemView 
from PySide6.QtGui import QMouseEvent,QDrag
from qt_EC import Ui_Form 
from ui_SlotFuncs import *

from misc_PrintException import print_ex
from qt_CV import Ui_Form as CVUI
from qt_CA import Ui_Form as CAUI
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
        self.dicParamWin={}
        self.setupUi(self)
        self.Restyling()
        self.EventBinding()
        self.SignalSlotBinding()
        self.showMaximized()
      
    def Restyling(self):
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



    def TechAdding(self,sender,event):
        item=QTreeWidgetItem([sender.text()])
        self.treeWidget.addTopLevelItem(item)
        ui_class = self.dicTechWin.get(sender.text())
        middle_index = self.splitter_2.indexOf(self.widget)
        techWin = QWidget()
        ui = ui_class()
        ui.setupUi(techWin)

        self.splitter_2.insertWidget(middle_index, techWin)
        self.widget.deleteLater()
        self.widget = techWin        # update reference
        
    def SignalSlotBinding(self):
        # Binding the signals and slots
        self.pushBtnProceed.clicked.connect(lambda sender=self.pushBtnProceed: Proceed(sender))
    
    def EventBinding(self):
        for label in self.scrollAreaOption.findChildren(QLabel):
            label.mouseDoubleClickEvent=lambda e, sender=label: self.TechAdding(sender,e)
            
    def eventFilter(self, obj, event):
        # Delete the focused button's row when pressing Delete
        if isinstance(obj, QTreeWidgetItem) and event is not None:
            if event.type() == QEvent.KeyPress:
                key = event.key()
                if key == Qt.Key_Delete:
                    item=self.treeWidget.currentItem()
                    if item:
                        parent =item.parent()
                        if parent:
                            parent.removeChild(item)
                        else:
                            idx=self.treeWidget.indexOfTopLevelItem(item)
                            self.treeWidget.takeTopLevelItem(idx)
        return super().eventFilter(obj, event)



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

if __name__ =='__main__':
    try:
        Qapp=QApplication(sys.argv)
        Qapp.styleHints().setColorScheme(Qt.ColorScheme.Light)
        Qapp.setStyle("Fusion")
        app=ECO_pot()
        sys.exit(Qapp.exec())
    except Exception as ex:
        print_ex(ex)