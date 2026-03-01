from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QTabBar, QTreeWidget, QTreeWidgetItem,
                             QAbstractItemView, QVBoxLayout, QWidget)
from PySide6.QtCore import Qt, QPoint, QRect, Signal
from PySide6.QtGui import QAction, QKeySequence, QMouseEvent, QCursor

class TechTreeWidget(QTreeWidget):
    itemRemoved = Signal(QTreeWidgetItem)
    itemsReordered = Signal()

    def _is_loop_item(self, item: QTreeWidgetItem | None) -> bool:
        if item is None:
            return False
        return item.text(0).strip().startswith('Loop')

    def dropEvent(self, event):
        target = self.itemAt(event.position().toPoint())
        drop_indicator = self.dropIndicatorPosition()

        destination_parent = None
        if target is not None:
            if drop_indicator == QAbstractItemView.DropIndicatorPosition.OnItem:
                destination_parent = target
            elif drop_indicator in (
                QAbstractItemView.DropIndicatorPosition.AboveItem,
                QAbstractItemView.DropIndicatorPosition.BelowItem,
            ):
                destination_parent = target.parent()

        if destination_parent is not None and not self._is_loop_item(destination_parent):
            event.ignore()
            return

        super().dropEvent(event)
        self.itemsReordered.emit()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            item = self.currentItem()
            if item:
                self.itemRemoved.emit(item)
                parent = item.parent()
                if parent:
                    parent.removeChild(item)
                else:
                    idx = self.indexOfTopLevelItem(item)
                    self.takeTopLevelItem(idx)
        else:
            super().keyPressEvent(event)


class FloatingTabWindow(QWidget):
    """Floating window created when tab is released"""
    def __init__(self, title: str, page: QWidget):
        super().__init__(None)
        self._page = page
        self._title = title
        
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Ensure page is visible and has the right parent
        if page is not None:
            layout.addWidget(page)
            page.show()
            print(f"[DEBUG] FloatingTabWindow: added page {page}, parent: {page.parent()}, visible: {page.isVisible()}")
        else:
            print("[DEBUG] FloatingTabWindow: page is None!")
        
        self.resize(600, 400)
    
    def closeEvent(self, event):
        """Clean up when window is closed"""
        print(f"[DEBUG] FloatingTabWindow closing: {self._title}")
        # Remove the page from layout before closing to prevent it from being deleted
        if self._page and self._page.parent() == self:
            self._page.setParent(None)
        super().closeEvent(event)


class TearOffTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_start_pos = None
        self._drag_tab_index = -1
        self._dragging_widget = None  # Track the actual widget, not just index
        self._dragging_title = ""
        self._floating_windows = []  # Keep references to prevent garbage collection
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = event.position().toPoint()
            self._drag_tab_index = self.tabAt(self._drag_start_pos)
            
            # Store the actual widget and title at drag start
            tw = self.parent()
            if isinstance(tw, QTabWidget) and self._drag_tab_index >= 0:
                self._dragging_widget = tw.widget(self._drag_tab_index)
                self._dragging_title = tw.tabText(self._drag_tab_index)
                print(f"[DEBUG] Drag started on tab {self._drag_tab_index}: {self._dragging_title}, widget: {self._dragging_widget}")
            else:
                self._dragging_widget = None
                self._dragging_title = ""
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return super().mouseMoveEvent(event)
        
        if self._drag_start_pos is None or self._drag_tab_index < 0:
            return super().mouseMoveEvent(event)
        
        # Check if dragged beyond threshold
        distance = (event.position().toPoint() - self._drag_start_pos).manhattanLength()
        if distance < 15:
            # Not beyond threshold yet, allow normal tab reordering
            return super().mouseMoveEvent(event)
        
        # Beyond threshold - this is a tear-off operation, don't allow tab reordering
        # Do NOT call super() to prevent Qt from moving tabs around
        return
    
    def mouseReleaseEvent(self, event):
        # Check if this was a drag operation
        if self._drag_start_pos and self._dragging_widget is not None:
            distance = (event.position().toPoint() - self._drag_start_pos).manhattanLength()
            
            print(f"[DEBUG] mouseReleaseEvent: distance={distance}, threshold=15")
            print(f"[DEBUG] Dragging widget: {self._dragging_widget}, title: {self._dragging_title}")
            
            if distance >= 15:
                # Create floating window at release position using tracked widget
                tw = self.parent()
                print(f"[DEBUG] Parent TabWidget: {tw}")
                
                if isinstance(tw, QTabWidget):
                    # Find the current index of the widget we're dragging
                    current_index = tw.indexOf(self._dragging_widget)
                    print(f"[DEBUG] Current index of dragging widget: {current_index}")
                    
                    if current_index >= 0:
                        # Double-check that this is the correct widget
                        widget_at_index = tw.widget(current_index)
                        print(f"[DEBUG] Widget at index {current_index}: {widget_at_index}")
                        
                        if widget_at_index == self._dragging_widget:
                            # CRITICAL: Set page parent to None BEFORE removing tab
                            # This prevents Qt from deleting the widget
                            self._dragging_widget.setParent(None)
                            
                            # Remove tab from widget using current index
                            tw.removeTab(current_index)
                            print(f"[DEBUG] Tab removed at index {current_index}, title was: {self._dragging_title}")
                            print(f"[DEBUG] Remaining tabs: {[tw.tabText(i) for i in range(tw.count())]}")
                            
                            # Create floating window
                            floating = FloatingTabWindow(self._dragging_title, self._dragging_widget)
                            global_pos = event.globalPosition().toPoint()
                            floating.move(global_pos.x() - 50, global_pos.y() - 20)
                            floating.show()
                            
                            # Keep reference to prevent garbage collection
                            self._floating_windows.append(floating)
                            floating.destroyed.connect(lambda: self._floating_windows.remove(floating) if floating in self._floating_windows else None)
                            
                            print(f"[DEBUG] Floating window created and shown at {global_pos}, visible: {floating.isVisible()}")
                        else:
                            print(f"[DEBUG] ERROR: Widget mismatch! Expected {self._dragging_widget}, got {widget_at_index}")
                    else:
                        print(f"[DEBUG] Widget not found in tab widget (index={current_index})")
                else:
                    print("[DEBUG] Parent is not a QTabWidget")
        
        # Reset tracking
        self._drag_start_pos = None
        self._drag_tab_index = -1
        self._dragging_widget = None
        self._dragging_title = ""
        super().mouseReleaseEvent(event)


class TabDockWidget(QTabWidget):
    """Tab widget with tear-off capability"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabBar(TearOffTabBar(self))
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)
    
    def _findTabByTitle(self, title: str):
        """Find tab widget by title"""
        for i in range(self.count()):
            if self.tabText(i) == title:
                return self.widget(i)
        return None
