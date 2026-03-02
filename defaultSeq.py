from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import QSize
from PySide6.QtGui import QFont

from UIModification.ui_CA import CA as CAUI
from UIModification.ui_Loop import Loop as LoopUI

def build_default_sequence_ui(main_window):
    """
    Builds the default sequence in the UI by adding techs programmatically.
    main_window: the ECO_pot instance
    """
    # Clear existing techs
    main_window.treeWidget_Techs.clear()
    main_window.dict_ChannelTechs[main_window.channel_Current] = {}
    
    font = QFont()
    font.setPointSize(14)
    
    # Add CA(name=1) top level
    item1 = QTreeWidgetItem()
    item1.setText(0, "CA")
    item1.setSizeHint(0, QSize(0, 30))
    item1.setFont(0, font)
    main_window.treeWidget_Techs.addTopLevelItem(item1)
    page1 = main_window._buildTechPage(CAUI, item1, i_ranges=[])
    main_window.dict_ChannelTechs[main_window.channel_Current][item1] = page1
    page1.lineEditName.setText('1')
    page1.lineEditName.editingFinished.emit()     # trigger nameChanged signal to set initial name
    
    # Add LOOP(iteration=2) top level
    item2 = QTreeWidgetItem()
    item2.setText(0, "Loop")
    item2.setSizeHint(0, QSize(0, 30))
    item2.setFont(0, font)
    main_window.treeWidget_Techs.addTopLevelItem(item2)
    page2 = main_window._buildTechPage(LoopUI, item2, i_ranges=[])
    main_window.dict_ChannelTechs[main_window.channel_Current][item2] = page2
    page2.lineEdit.setText('2')
    page2.lineEdit.editingFinished.emit()     # trigger editingFinished signal to set initial iterations
    
    # Add CA(name=2) as child of LOOP
    item3 = QTreeWidgetItem()
    item3.setText(0, "CA")
    item3.setSizeHint(0, QSize(0, 30))
    item3.setFont(0, font)
    item2.addChild(item3)
    page3 = main_window._buildTechPage(CAUI, item3, i_ranges=[])
    main_window.dict_ChannelTechs[main_window.channel_Current][item3] = page3
    page3.lineEditName.setText('2')
    page3.lineEditName.editingFinished.emit()     # trigger nameChanged signal to set initial name
    
    # Add LOOP(iteration=3) as child of CA
    item4 = QTreeWidgetItem()
    item4.setText(0, "Loop")
    item4.setSizeHint(0, QSize(0, 30))
    item4.setFont(0, font)
    item2.addChild(item4)
    page4 = main_window._buildTechPage(LoopUI, item4, i_ranges=[])
    main_window.dict_ChannelTechs[main_window.channel_Current][item4] = page4
    page4.lineEdit.setText('3')
    page4.lineEdit.editingFinished.emit()     # trigger editingFinished signal to set initial iterations
    
    # Add CA(name=3) as child of LOOP
    item5 = QTreeWidgetItem()
    item5.setText(0, "CA")
    item5.setSizeHint(0, QSize(0, 30))
    item5.setFont(0, font)
    item4.addChild(item5)
    page5 = main_window._buildTechPage(CAUI, item5, i_ranges=[])
    main_window.dict_ChannelTechs[main_window.channel_Current][item5] = page5
    page5.lineEditName.setText('3')
    page5.lineEditName.editingFinished.emit()     # trigger nameChanged signal to set initial name
