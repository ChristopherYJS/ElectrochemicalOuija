#& "C:\Users\chrst\AppData\Roaming\Python\Python313\Scripts\pyside6-uic.exe" "uiEC.ui" "-o" "uiEC.py" "--from-imports"
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QApplication, QWidget,QListWidgetItem,QPushButton,QHBoxLayout,QLabel
from PySide6.QtCore import QSize, Qt, QEvent
from PySide6.QtWidgets import QAbstractItemView 
from PySide6.QtGui import QMouseEvent
from ui_EC import Ui_Form 
from ui_SlotFuncs import *

from misc_PrintException import print_ex

class ECO_pot(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.listTechs=[]
        self.setupUi(self)
        self.EventHandling()
        self.SignalSlotBinding()
        self.Restyling()
        self.WidgetPropertySetting()
        self.showMaximized()

    def WidgetPropertySetting(self):
        # Make list draggable/reorderable
        self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDropIndicatorShown(True)
        self.listWidget.setDefaultDropAction(Qt.MoveAction)
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.SignalSlotBinding()
        # (optional) know when the order changes
        self.listWidget.model().rowsMoved.connect(self.on_rows_moved)

    def Restyling(self):
        #Restyle the widgets 
        pass

    def EventHandling(self):
        # Add double-click event to all QLabel children of scrollAreaOption
        for label in self.scrollAreaOption.findChildren(QLabel):
            label.mouseDoubleClickEvent=(lambda event, sender=label: self.TechAdding(sender, event))

    def SignalSlotBinding(self):
        # Binding the signals and slots
        self.pushBtnProceed.clicked.connect(lambda sender=self.pushBtnProceed: Proceed(sender))
            
    def TechAdding(self, sender, event):
        text = sender.text()
        item = QListWidgetItem()
        item.setSizeHint(QSize(200, 36))
        self.listWidget.addItem(item)

        row = QWidget()
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)

        btn = QPushButton(text, row)
        btn.setMinimumHeight(32)
        btn.clicked.connect(lambda checked=False, t=text: print(f"{t} clicked"))
        btn.setFocusPolicy(Qt.StrongFocus)          
        btn.installEventFilter(self)                
        lay.addWidget(btn)

        self.listWidget.setItemWidget(item, row)
        event.accept()
    

        # attach the widget to the item
        self.listWidget.setItemWidget(item, row)

    def on_rows_moved(self, *args):
        # Example: print the new order after a drag
        order = []
        for i in range(self.listWidget.count()):
            w = self.listWidget.itemWidget(self.listWidget.item(i))
            btn = w.findChild(QPushButton)
            order.append(btn.text() if btn else f"row {i}")
        print("New order:", order)

    def _remove_row_by_button(self, btn: QPushButton):
        # find which QListWidgetItem owns this button
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            row_widget = self.listWidget.itemWidget(item)
            if row_widget and row_widget.findChild(QPushButton) is btn:
                # remove visual widget and the item
                self.listWidget.removeItemWidget(item)
                row_widget.deleteLater()
                it = self.listWidget.takeItem(i)
                del it
                break
            
    def eventFilter(self, obj, event):
        # Delete the focused button's row when pressing Delete
        if isinstance(obj, QPushButton) and event is not None:
            if event.type() == QEvent.KeyPress:
                key = event.key()
                if key == Qt.Key_Delete:
                    self._remove_row_by_button(obj)
                    return True  # consume event
        return super().eventFilter(obj, event)




if __name__ =='__main__':
    try:
        Qapp=QApplication(sys.argv)
        app=ECO_pot()
        sys.exit(Qapp.exec())
    except Exception as ex:
        print_ex(ex)