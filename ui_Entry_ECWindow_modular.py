import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QTreeWidgetItem

from misc_handleException import exception2msg, msg2file
from ecw_modular_layout import apply_four_panel_restyle
from ui_Entry_ECWindow import ECO_pot
from misc_handleException import errorDeco


class ECO_pot_modular(ECO_pot):
    def restyle(self):
        super().restyle()
        apply_four_panel_restyle(self)

    @errorDeco(logger='self.Log')
    def addTech(self, sender, event):
        item = QTreeWidgetItem([sender.text()])
        item.setSizeHint(0, self.treeWidget.sizeHint())
        font = QFont()
        font.setPointSize(14)
        item.setFont(0, font)
        self.treeWidget.addTopLevelItem(item)

        ui_class = self.dicTechWin.get(sender.text())
        page = self._buildTab(ui_class, item)
        self.itemTechPair[item] = page
        self._show_in_potentiostat_panel(page)

    @errorDeco(logger='self.Log')
    def TreeItemClicked(self, item, column=None):
        page = self.itemTechPair.get(item)
        if page is None:
            return
        self._show_in_potentiostat_panel(page)

    def _show_in_potentiostat_panel(self, page):
        panel = getattr(self, "potentiostatPanel", None)
        if panel is None:
            return
        self._clearWidget(panel)
        panel.layout().addWidget(page)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        app.styleHints().setColorScheme(Qt.ColorScheme.Light)
        app.setStyle("Fusion")
        window = ECO_pot_modular()
        sys.exit(app.exec())
    except Exception as ex:
        error_msg = exception2msg(ex)
        print(error_msg)
        msg2file(error_msg)
