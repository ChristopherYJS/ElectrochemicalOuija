# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_ECO_Main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSplitter, QStatusBar, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(809, 592)
        self.actionECTech_Tab = QAction(MainWindow)
        self.actionECTech_Tab.setObjectName(u"actionECTech_Tab")
        self.actionECPlot_Tab = QAction(MainWindow)
        self.actionECPlot_Tab.setObjectName(u"actionECPlot_Tab")
        self.actionPositioner_Tab = QAction(MainWindow)
        self.actionPositioner_Tab.setObjectName(u"actionPositioner_Tab")
        self.actionLog_Tab = QAction(MainWindow)
        self.actionLog_Tab.setObjectName(u"actionLog_Tab")
        self.actionMiscoscope_Tab = QAction(MainWindow)
        self.actionMiscoscope_Tab.setObjectName(u"actionMiscoscope_Tab")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frameShortCut = QFrame(self.centralwidget)
        self.frameShortCut.setObjectName(u"frameShortCut")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameShortCut.sizePolicy().hasHeightForWidth())
        self.frameShortCut.setSizePolicy(sizePolicy)
        self.frameShortCut.setFrameShape(QFrame.StyledPanel)
        self.frameShortCut.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frameShortCut)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_6 = QPushButton(self.frameShortCut)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy1)
        self.pushButton_6.setMinimumSize(QSize(40, 40))
        self.pushButton_6.setMaximumSize(QSize(40, 40))
        self.pushButton_6.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        self.horizontalLayout_3.addWidget(self.pushButton_6)

        self.pushButton_8 = QPushButton(self.frameShortCut)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy1.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy1)
        self.pushButton_8.setMinimumSize(QSize(40, 40))
        self.pushButton_8.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_3.addWidget(self.pushButton_8)

        self.pushButton_7 = QPushButton(self.frameShortCut)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy1.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy1)
        self.pushButton_7.setMinimumSize(QSize(40, 40))
        self.pushButton_7.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_3.addWidget(self.pushButton_7)

        self.pushButton_5 = QPushButton(self.frameShortCut)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy2)
        self.pushButton_5.setMinimumSize(QSize(40, 40))
        self.pushButton_5.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_3.addWidget(self.pushButton_5)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.frameShortCut)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy3)
        self.splitter.setOrientation(Qt.Vertical)
        self.scrollAreaOption = QScrollArea(self.splitter)
        self.scrollAreaOption.setObjectName(u"scrollAreaOption")
        sizePolicy.setHeightForWidth(self.scrollAreaOption.sizePolicy().hasHeightForWidth())
        self.scrollAreaOption.setSizePolicy(sizePolicy)
        self.scrollAreaOption.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 196, 126))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_3.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_3.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelTechCA = QLabel(self.scrollAreaWidgetContents_3)
        self.labelTechCA.setObjectName(u"labelTechCA")
        sizePolicy.setHeightForWidth(self.labelTechCA.sizePolicy().hasHeightForWidth())
        self.labelTechCA.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.labelTechCA)

        self.labelTechCP = QLabel(self.scrollAreaWidgetContents_3)
        self.labelTechCP.setObjectName(u"labelTechCP")
        sizePolicy.setHeightForWidth(self.labelTechCP.sizePolicy().hasHeightForWidth())
        self.labelTechCP.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.labelTechCP)

        self.labelTechCV = QLabel(self.scrollAreaWidgetContents_3)
        self.labelTechCV.setObjectName(u"labelTechCV")
        sizePolicy.setHeightForWidth(self.labelTechCV.sizePolicy().hasHeightForWidth())
        self.labelTechCV.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.labelTechCV)

        self.labelTechEIS = QLabel(self.scrollAreaWidgetContents_3)
        self.labelTechEIS.setObjectName(u"labelTechEIS")
        sizePolicy.setHeightForWidth(self.labelTechEIS.sizePolicy().hasHeightForWidth())
        self.labelTechEIS.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.labelTechEIS)

        self.labelMove = QLabel(self.scrollAreaWidgetContents_3)
        self.labelMove.setObjectName(u"labelMove")
        sizePolicy.setHeightForWidth(self.labelMove.sizePolicy().hasHeightForWidth())
        self.labelMove.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.labelMove)

        self.labelLoop = QLabel(self.scrollAreaWidgetContents_3)
        self.labelLoop.setObjectName(u"labelLoop")
        sizePolicy.setHeightForWidth(self.labelLoop.sizePolicy().hasHeightForWidth())
        self.labelLoop.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.labelLoop)

        self.scrollAreaOption.setWidget(self.scrollAreaWidgetContents_3)
        self.splitter.addWidget(self.scrollAreaOption)
        self.treeWidget = QTreeWidget(self.splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy4)
        self.splitter.addWidget(self.treeWidget)

        self.verticalLayout_2.addWidget(self.splitter)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy5)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setMinimumSize(QSize(40, 40))
        self.pushButton.setMaximumSize(QSize(40, 40))
        self.pushButton.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)
        self.pushButton_2.setMinimumSize(QSize(40, 40))
        self.pushButton_2.setMaximumSize(QSize(40, 40))

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy1.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy1)
        self.pushButton_3.setMinimumSize(QSize(40, 40))
        self.pushButton_3.setMaximumSize(QSize(40, 40))

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.frame)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy2.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy2)
        self.pushButton_4.setMinimumSize(QSize(40, 40))
        self.pushButton_4.setMaximumSize(QSize(40, 40))

        self.horizontalLayout.addWidget(self.pushButton_4)


        self.verticalLayout_2.addWidget(self.frame)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.splitter2 = QSplitter(self.centralwidget)
        self.splitter2.setObjectName(u"splitter2")
        self.splitter2.setOrientation(Qt.Vertical)
        self.tabWidgetTop = QTabWidget(self.splitter2)
        self.tabWidgetTop.setObjectName(u"tabWidgetTop")
        sizePolicy4.setHeightForWidth(self.tabWidgetTop.sizePolicy().hasHeightForWidth())
        self.tabWidgetTop.setSizePolicy(sizePolicy4)
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidgetTop.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidgetTop.addTab(self.tab_4, "")
        self.splitter2.addWidget(self.tabWidgetTop)
        self.tabWidgetBtm = QTabWidget(self.splitter2)
        self.tabWidgetBtm.setObjectName(u"tabWidgetBtm")
        sizePolicy4.setHeightForWidth(self.tabWidgetBtm.sizePolicy().hasHeightForWidth())
        self.tabWidgetBtm.setSizePolicy(sizePolicy4)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidgetBtm.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidgetBtm.addTab(self.tab_2, "")
        self.splitter2.addWidget(self.tabWidgetBtm)

        self.horizontalLayout_2.addWidget(self.splitter2)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.frameStatus = QFrame(self.centralwidget)
        self.frameStatus.setObjectName(u"frameStatus")
        self.frameStatus.setFrameShape(QFrame.StyledPanel)
        self.frameStatus.setFrameShadow(QFrame.Raised)

        self.verticalLayout_3.addWidget(self.frameStatus)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 809, 21))
        self.menuConnect = QMenu(self.menubar)
        self.menuConnect.setObjectName(u"menuConnect")
        self.menuPreference = QMenu(self.menubar)
        self.menuPreference.setObjectName(u"menuPreference")
        self.menuWindows = QMenu(self.menubar)
        self.menuWindows.setObjectName(u"menuWindows")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuConnect.menuAction())
        self.menubar.addAction(self.menuPreference.menuAction())
        self.menubar.addAction(self.menuWindows.menuAction())
        self.menuWindows.addAction(self.actionECTech_Tab)
        self.menuWindows.addAction(self.actionECPlot_Tab)
        self.menuWindows.addAction(self.actionPositioner_Tab)
        self.menuWindows.addAction(self.actionLog_Tab)
        self.menuWindows.addAction(self.actionMiscoscope_Tab)

        self.retranslateUi(MainWindow)

        self.tabWidgetTop.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionECTech_Tab.setText(QCoreApplication.translate("MainWindow", u"ECTech Tab", None))
        self.actionECPlot_Tab.setText(QCoreApplication.translate("MainWindow", u"ECPlot Tab", None))
        self.actionPositioner_Tab.setText(QCoreApplication.translate("MainWindow", u"Positioner Tab", None))
        self.actionLog_Tab.setText(QCoreApplication.translate("MainWindow", u"Log Tab", None))
        self.actionMiscoscope_Tab.setText(QCoreApplication.translate("MainWindow", u"Miscoscope Tab", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.labelTechCA.setText(QCoreApplication.translate("MainWindow", u"CA", None))
        self.labelTechCP.setText(QCoreApplication.translate("MainWindow", u"CP", None))
        self.labelTechCV.setText(QCoreApplication.translate("MainWindow", u"CV", None))
        self.labelTechEIS.setText(QCoreApplication.translate("MainWindow", u"EIS", None))
        self.labelMove.setText(QCoreApplication.translate("MainWindow", u"Move", None))
        self.labelLoop.setText(QCoreApplication.translate("MainWindow", u"Loop", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.tabWidgetTop.setTabText(self.tabWidgetTop.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidgetTop.setTabText(self.tabWidgetTop.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.tabWidgetBtm.setTabText(self.tabWidgetBtm.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidgetBtm.setTabText(self.tabWidgetBtm.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.menuConnect.setTitle(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.menuPreference.setTitle(QCoreApplication.translate("MainWindow", u"Preference", None))
        self.menuWindows.setTitle(QCoreApplication.translate("MainWindow", u"Windows", None))
    # retranslateUi

