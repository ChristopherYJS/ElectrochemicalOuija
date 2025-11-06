# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_ECO_Main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
    QPushButton, QScrollArea, QSizePolicy, QSplitter,
    QStatusBar, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

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
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setFrameShape(QFrame.Box)
        self.splitter.setOrientation(Qt.Vertical)
        self.treeWidget = QTreeWidget(self.splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy1)
        self.splitter.addWidget(self.treeWidget)
        self.scrollAreaOption = QScrollArea(self.splitter)
        self.scrollAreaOption.setObjectName(u"scrollAreaOption")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollAreaOption.sizePolicy().hasHeightForWidth())
        self.scrollAreaOption.setSizePolicy(sizePolicy2)
        self.scrollAreaOption.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 192, 192))
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents_3.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_3.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelTechCA = QLabel(self.scrollAreaWidgetContents_3)
        self.labelTechCA.setObjectName(u"labelTechCA")
        sizePolicy1.setHeightForWidth(self.labelTechCA.sizePolicy().hasHeightForWidth())
        self.labelTechCA.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.labelTechCA)

        self.labelTechCP = QLabel(self.scrollAreaWidgetContents_3)
        self.labelTechCP.setObjectName(u"labelTechCP")

        self.verticalLayout.addWidget(self.labelTechCP)

        self.labelTechCV = QLabel(self.scrollAreaWidgetContents_3)
        self.labelTechCV.setObjectName(u"labelTechCV")

        self.verticalLayout.addWidget(self.labelTechCV)

        self.labelTechEIS = QLabel(self.scrollAreaWidgetContents_3)
        self.labelTechEIS.setObjectName(u"labelTechEIS")

        self.verticalLayout.addWidget(self.labelTechEIS)

        self.labelMove = QLabel(self.scrollAreaWidgetContents_3)
        self.labelMove.setObjectName(u"labelMove")

        self.verticalLayout.addWidget(self.labelMove)

        self.labelLoop = QLabel(self.scrollAreaWidgetContents_3)
        self.labelLoop.setObjectName(u"labelLoop")
        sizePolicy1.setHeightForWidth(self.labelLoop.sizePolicy().hasHeightForWidth())
        self.labelLoop.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.labelLoop)

        self.scrollAreaOption.setWidget(self.scrollAreaWidgetContents_3)
        self.splitter.addWidget(self.scrollAreaOption)

        self.horizontalLayout.addWidget(self.splitter)

        self.splitter2 = QSplitter(self.centralwidget)
        self.splitter2.setObjectName(u"splitter2")
        self.splitter2.setOrientation(Qt.Vertical)
        self.tabWidgetTop = QTabWidget(self.splitter2)
        self.tabWidgetTop.setObjectName(u"tabWidgetTop")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidgetTop.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidgetTop.addTab(self.tab_4, "")
        self.splitter2.addWidget(self.tabWidgetTop)
        self.tabWidgetBtm = QTabWidget(self.splitter2)
        self.tabWidgetBtm.setObjectName(u"tabWidgetBtm")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidgetBtm.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidgetBtm.addTab(self.tab_2, "")
        self.splitter2.addWidget(self.tabWidgetBtm)

        self.horizontalLayout.addWidget(self.splitter2)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.pushBtnProceed = QPushButton(self.centralwidget)
        self.pushBtnProceed.setObjectName(u"pushBtnProceed")

        self.verticalLayout_2.addWidget(self.pushBtnProceed)

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

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionECTech_Tab.setText(QCoreApplication.translate("MainWindow", u"ECTech Tab", None))
        self.actionECPlot_Tab.setText(QCoreApplication.translate("MainWindow", u"ECPlot Tab", None))
        self.actionPositioner_Tab.setText(QCoreApplication.translate("MainWindow", u"Positioner Tab", None))
        self.actionLog_Tab.setText(QCoreApplication.translate("MainWindow", u"Log Tab", None))
        self.actionMiscoscope_Tab.setText(QCoreApplication.translate("MainWindow", u"Miscoscope Tab", None))
        self.labelTechCA.setText(QCoreApplication.translate("MainWindow", u"CA", None))
        self.labelTechCP.setText(QCoreApplication.translate("MainWindow", u"CP", None))
        self.labelTechCV.setText(QCoreApplication.translate("MainWindow", u"CV", None))
        self.labelTechEIS.setText(QCoreApplication.translate("MainWindow", u"EIS", None))
        self.labelMove.setText(QCoreApplication.translate("MainWindow", u"Move", None))
        self.labelLoop.setText(QCoreApplication.translate("MainWindow", u"Loop", None))
        self.tabWidgetTop.setTabText(self.tabWidgetTop.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidgetTop.setTabText(self.tabWidgetTop.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.tabWidgetBtm.setTabText(self.tabWidgetBtm.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidgetBtm.setTabText(self.tabWidgetBtm.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.pushBtnProceed.setText(QCoreApplication.translate("MainWindow", u"Proceed", None))
        self.menuConnect.setTitle(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.menuPreference.setTitle(QCoreApplication.translate("MainWindow", u"Preference", None))
        self.menuWindows.setTitle(QCoreApplication.translate("MainWindow", u"Windows", None))
    # retranslateUi

