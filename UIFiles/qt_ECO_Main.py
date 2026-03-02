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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1155, 812)
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
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frameShortCut = QFrame(self.centralwidget)
        self.frameShortCut.setObjectName(u"frameShortCut")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameShortCut.sizePolicy().hasHeightForWidth())
        self.frameShortCut.setSizePolicy(sizePolicy)
        self.frameShortCut.setFrameShape(QFrame.StyledPanel)
        self.frameShortCut.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frameShortCut)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 0, 5, 0)
        self.pushButtonConnect = QPushButton(self.frameShortCut)
        self.pushButtonConnect.setObjectName(u"pushButtonConnect")
        self.pushButtonConnect.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButtonConnect.sizePolicy().hasHeightForWidth())
        self.pushButtonConnect.setSizePolicy(sizePolicy1)
        self.pushButtonConnect.setMinimumSize(QSize(40, 40))
        self.pushButtonConnect.setMaximumSize(QSize(50, 50))
        self.pushButtonConnect.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        self.horizontalLayout_3.addWidget(self.pushButtonConnect)

        self.pushButtonPsInfo = QPushButton(self.frameShortCut)
        self.pushButtonPsInfo.setObjectName(u"pushButtonPsInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButtonPsInfo.sizePolicy().hasHeightForWidth())
        self.pushButtonPsInfo.setSizePolicy(sizePolicy2)
        self.pushButtonPsInfo.setMinimumSize(QSize(40, 40))
        self.pushButtonPsInfo.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_3.addWidget(self.pushButtonPsInfo)

        self.pushButton_7 = QPushButton(self.frameShortCut)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy1.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy1)
        self.pushButton_7.setMinimumSize(QSize(40, 40))
        self.pushButton_7.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_3.addWidget(self.pushButton_7)

        self.pushButton_5 = QPushButton(self.frameShortCut)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy3)
        self.pushButton_5.setMinimumSize(QSize(40, 40))
        self.pushButton_5.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_3.addWidget(self.pushButton_5)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_5.addWidget(self.frameShortCut)

        self.horizontalLayout_Main = QHBoxLayout()
        self.horizontalLayout_Main.setObjectName(u"horizontalLayout_Main")
        self.verticalLayout_Tech = QVBoxLayout()
        self.verticalLayout_Tech.setObjectName(u"verticalLayout_Tech")
        self.splitter_Tech = QSplitter(self.centralwidget)
        self.splitter_Tech.setObjectName(u"splitter_Tech")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.splitter_Tech.sizePolicy().hasHeightForWidth())
        self.splitter_Tech.setSizePolicy(sizePolicy4)
        self.splitter_Tech.setOrientation(Qt.Vertical)
        self.scrollAreaOption_Techs = QScrollArea(self.splitter_Tech)
        self.scrollAreaOption_Techs.setObjectName(u"scrollAreaOption_Techs")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.scrollAreaOption_Techs.sizePolicy().hasHeightForWidth())
        self.scrollAreaOption_Techs.setSizePolicy(sizePolicy5)
        self.scrollAreaOption_Techs.setWidgetResizable(True)
        self.scrollAreaWidgetContents_Tech = QWidget()
        self.scrollAreaWidgetContents_Tech.setObjectName(u"scrollAreaWidgetContents_Tech")
        self.scrollAreaWidgetContents_Tech.setGeometry(QRect(0, 0, 196, 126))
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.scrollAreaWidgetContents_Tech.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_Tech.setSizePolicy(sizePolicy6)
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents_Tech)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelTechCA = QLabel(self.scrollAreaWidgetContents_Tech)
        self.labelTechCA.setObjectName(u"labelTechCA")
        sizePolicy6.setHeightForWidth(self.labelTechCA.sizePolicy().hasHeightForWidth())
        self.labelTechCA.setSizePolicy(sizePolicy6)

        self.verticalLayout.addWidget(self.labelTechCA)

        self.labelTechCP = QLabel(self.scrollAreaWidgetContents_Tech)
        self.labelTechCP.setObjectName(u"labelTechCP")
        sizePolicy6.setHeightForWidth(self.labelTechCP.sizePolicy().hasHeightForWidth())
        self.labelTechCP.setSizePolicy(sizePolicy6)

        self.verticalLayout.addWidget(self.labelTechCP)

        self.labelTechCV = QLabel(self.scrollAreaWidgetContents_Tech)
        self.labelTechCV.setObjectName(u"labelTechCV")
        sizePolicy6.setHeightForWidth(self.labelTechCV.sizePolicy().hasHeightForWidth())
        self.labelTechCV.setSizePolicy(sizePolicy6)

        self.verticalLayout.addWidget(self.labelTechCV)

        self.labelTechEIS = QLabel(self.scrollAreaWidgetContents_Tech)
        self.labelTechEIS.setObjectName(u"labelTechEIS")
        sizePolicy6.setHeightForWidth(self.labelTechEIS.sizePolicy().hasHeightForWidth())
        self.labelTechEIS.setSizePolicy(sizePolicy6)

        self.verticalLayout.addWidget(self.labelTechEIS)

        self.labelMove = QLabel(self.scrollAreaWidgetContents_Tech)
        self.labelMove.setObjectName(u"labelMove")
        sizePolicy6.setHeightForWidth(self.labelMove.sizePolicy().hasHeightForWidth())
        self.labelMove.setSizePolicy(sizePolicy6)

        self.verticalLayout.addWidget(self.labelMove)

        self.labelLoop = QLabel(self.scrollAreaWidgetContents_Tech)
        self.labelLoop.setObjectName(u"labelLoop")
        sizePolicy6.setHeightForWidth(self.labelLoop.sizePolicy().hasHeightForWidth())
        self.labelLoop.setSizePolicy(sizePolicy6)

        self.verticalLayout.addWidget(self.labelLoop)

        self.scrollAreaOption_Techs.setWidget(self.scrollAreaWidgetContents_Tech)
        self.splitter_Tech.addWidget(self.scrollAreaOption_Techs)
        self.treeWidget_Techs = QTreeWidget(self.splitter_Tech)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget_Techs.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_Techs.setObjectName(u"treeWidget_Techs")
        sizePolicy4.setHeightForWidth(self.treeWidget_Techs.sizePolicy().hasHeightForWidth())
        self.treeWidget_Techs.setSizePolicy(sizePolicy4)
        self.splitter_Tech.addWidget(self.treeWidget_Techs)

        self.verticalLayout_Tech.addWidget(self.splitter_Tech)

        self.frame_Channels = QFrame(self.centralwidget)
        self.frame_Channels.setObjectName(u"frame_Channels")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.frame_Channels.sizePolicy().hasHeightForWidth())
        self.frame_Channels.setSizePolicy(sizePolicy7)
        self.frame_Channels.setFrameShape(QFrame.Box)
        self.formLayout_Channel = QFormLayout(self.frame_Channels)
        self.formLayout_Channel.setObjectName(u"formLayout_Channel")

        self.verticalLayout_Tech.addWidget(self.frame_Channels)

        self.frame_Tech = QFrame(self.centralwidget)
        self.frame_Tech.setObjectName(u"frame_Tech")
        sizePolicy7.setHeightForWidth(self.frame_Tech.sizePolicy().hasHeightForWidth())
        self.frame_Tech.setSizePolicy(sizePolicy7)
        self.frame_Tech.setFrameShape(QFrame.StyledPanel)
        self.frame_Tech.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_Tech)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_SingleRun = QPushButton(self.frame_Tech)
        self.pushButton_SingleRun.setObjectName(u"pushButton_SingleRun")
        self.pushButton_SingleRun.setEnabled(True)
        sizePolicy7.setHeightForWidth(self.pushButton_SingleRun.sizePolicy().hasHeightForWidth())
        self.pushButton_SingleRun.setSizePolicy(sizePolicy7)
        self.pushButton_SingleRun.setMinimumSize(QSize(40, 40))
        self.pushButton_SingleRun.setMaximumSize(QSize(80, 40))
        self.pushButton_SingleRun.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        self.horizontalLayout.addWidget(self.pushButton_SingleRun)

        self.pushButton_ErrorTest = QPushButton(self.frame_Tech)
        self.pushButton_ErrorTest.setObjectName(u"pushButton_ErrorTest")
        sizePolicy7.setHeightForWidth(self.pushButton_ErrorTest.sizePolicy().hasHeightForWidth())
        self.pushButton_ErrorTest.setSizePolicy(sizePolicy7)
        self.pushButton_ErrorTest.setMinimumSize(QSize(40, 40))
        self.pushButton_ErrorTest.setMaximumSize(QSize(80, 40))

        self.horizontalLayout.addWidget(self.pushButton_ErrorTest)

        self.pushButton_3 = QPushButton(self.frame_Tech)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy7.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy7)
        self.pushButton_3.setMinimumSize(QSize(40, 40))
        self.pushButton_3.setMaximumSize(QSize(80, 40))

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_MultiRun = QPushButton(self.frame_Tech)
        self.pushButton_MultiRun.setObjectName(u"pushButton_MultiRun")
        sizePolicy7.setHeightForWidth(self.pushButton_MultiRun.sizePolicy().hasHeightForWidth())
        self.pushButton_MultiRun.setSizePolicy(sizePolicy7)
        self.pushButton_MultiRun.setMinimumSize(QSize(40, 40))
        self.pushButton_MultiRun.setMaximumSize(QSize(80, 40))

        self.horizontalLayout.addWidget(self.pushButton_MultiRun)


        self.verticalLayout_Tech.addWidget(self.frame_Tech)

        self.verticalLayout_Tech.setStretch(0, 8)

        self.horizontalLayout_Main.addLayout(self.verticalLayout_Tech)

        self.splitter_Mid = QSplitter(self.centralwidget)
        self.splitter_Mid.setObjectName(u"splitter_Mid")
        self.splitter_Mid.setOrientation(Qt.Vertical)
        self.verticalLayoutWidget_3 = QWidget(self.splitter_Mid)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayout_Pot = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_Pot.setObjectName(u"verticalLayout_Pot")
        self.verticalLayout_Pot.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget_3)
        self.label_2.setObjectName(u"label_2")
        sizePolicy6.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy6)
        font = QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)

        self.verticalLayout_Pot.addWidget(self.label_2)

        self.frame_ps = QFrame(self.verticalLayoutWidget_3)
        self.frame_ps.setObjectName(u"frame_ps")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.frame_ps.sizePolicy().hasHeightForWidth())
        self.frame_ps.setSizePolicy(sizePolicy8)
        self.frame_ps.setFrameShape(QFrame.Panel)

        self.verticalLayout_Pot.addWidget(self.frame_ps)

        self.splitter_Mid.addWidget(self.verticalLayoutWidget_3)
        self.verticalLayoutWidget_2 = QWidget(self.splitter_Mid)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayout_Pos = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_Pos.setObjectName(u"verticalLayout_Pos")
        self.verticalLayout_Pos.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")
        sizePolicy6.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy6)
        self.label.setFont(font)

        self.verticalLayout_Pos.addWidget(self.label)

        self.frame_mp = QFrame(self.verticalLayoutWidget_2)
        self.frame_mp.setObjectName(u"frame_mp")
        sizePolicy8.setHeightForWidth(self.frame_mp.sizePolicy().hasHeightForWidth())
        self.frame_mp.setSizePolicy(sizePolicy8)
        self.frame_mp.setFrameShape(QFrame.Panel)

        self.verticalLayout_Pos.addWidget(self.frame_mp)

        self.splitter_Mid.addWidget(self.verticalLayoutWidget_2)
        self.verticalLayoutWidget_4 = QWidget(self.splitter_Mid)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayout_Log = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_Log.setObjectName(u"verticalLayout_Log")
        self.verticalLayout_Log.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget_4)
        self.label_3.setObjectName(u"label_3")
        sizePolicy6.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy6)
        self.label_3.setFont(font)

        self.verticalLayout_Log.addWidget(self.label_3)

        self.frame_log = QFrame(self.verticalLayoutWidget_4)
        self.frame_log.setObjectName(u"frame_log")
        sizePolicy8.setHeightForWidth(self.frame_log.sizePolicy().hasHeightForWidth())
        self.frame_log.setSizePolicy(sizePolicy8)
        self.frame_log.setFrameShape(QFrame.Panel)

        self.verticalLayout_Log.addWidget(self.frame_log)

        self.lineEdit = QLineEdit(self.verticalLayoutWidget_4)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_Log.addWidget(self.lineEdit)

        self.splitter_Mid.addWidget(self.verticalLayoutWidget_4)

        self.horizontalLayout_Main.addWidget(self.splitter_Mid)

        self.verticalLayout_Plot = QVBoxLayout()
        self.verticalLayout_Plot.setObjectName(u"verticalLayout_Plot")

        self.horizontalLayout_Main.addLayout(self.verticalLayout_Plot)

        self.horizontalLayout_Main.setStretch(0, 1)
        self.horizontalLayout_Main.setStretch(1, 2)
        self.horizontalLayout_Main.setStretch(2, 3)

        self.verticalLayout_5.addLayout(self.horizontalLayout_Main)

        self.verticalLayout_5.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1155, 21))
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
        self.pushButtonConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.pushButtonPsInfo.setText(QCoreApplication.translate("MainWindow", u"pB", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.labelTechCA.setText(QCoreApplication.translate("MainWindow", u"CA", None))
        self.labelTechCP.setText(QCoreApplication.translate("MainWindow", u"CP", None))
        self.labelTechCV.setText(QCoreApplication.translate("MainWindow", u"CV", None))
        self.labelTechEIS.setText(QCoreApplication.translate("MainWindow", u"EIS", None))
        self.labelMove.setText(QCoreApplication.translate("MainWindow", u"Move", None))
        self.labelLoop.setText(QCoreApplication.translate("MainWindow", u"Loop", None))
        self.pushButton_SingleRun.setText(QCoreApplication.translate("MainWindow", u"Single\n"
"Run", None))
        self.pushButton_ErrorTest.setText(QCoreApplication.translate("MainWindow", u"Filename\n"
"Test", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Default\n"
"Seq", None))
        self.pushButton_MultiRun.setText(QCoreApplication.translate("MainWindow", u"Multi\n"
"Run", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Potentiostat", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Positioner", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Log", None))
        self.menuConnect.setTitle(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.menuPreference.setTitle(QCoreApplication.translate("MainWindow", u"Preference", None))
        self.menuWindows.setTitle(QCoreApplication.translate("MainWindow", u"Windows", None))
    # retranslateUi

