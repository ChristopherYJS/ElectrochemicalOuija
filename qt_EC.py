# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EC.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QScrollArea, QSizePolicy,
    QSplitter, QTabWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1001, 600)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter_2 = QSplitter(Form)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.tabWidget = QTabWidget(self.splitter_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.listWidget = QListWidget(self.tab)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 10, 650, 500))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.splitter_2.addWidget(self.tabWidget)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.scrollAreaParam = QScrollArea(self.splitter)
        self.scrollAreaParam.setObjectName(u"scrollAreaParam")
        self.scrollAreaParam.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 277, 394))
        self.scrollAreaParam.setWidget(self.scrollAreaWidgetContents)
        self.splitter.addWidget(self.scrollAreaParam)
        self.scrollAreaOption = QScrollArea(self.splitter)
        self.scrollAreaOption.setObjectName(u"scrollAreaOption")
        self.scrollAreaOption.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 277, 107))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollAreaWidgetContents_3.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_3.setSizePolicy(sizePolicy2)
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelTechCA = QLabel(self.scrollAreaWidgetContents_3)
        self.labelTechCA.setObjectName(u"labelTechCA")
        sizePolicy.setHeightForWidth(self.labelTechCA.sizePolicy().hasHeightForWidth())
        self.labelTechCA.setSizePolicy(sizePolicy)

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

        self.labelTechLoop = QLabel(self.scrollAreaWidgetContents_3)
        self.labelTechLoop.setObjectName(u"labelTechLoop")

        self.verticalLayout.addWidget(self.labelTechLoop)

        self.scrollAreaOption.setWidget(self.scrollAreaWidgetContents_3)
        self.splitter.addWidget(self.scrollAreaOption)
        self.splitter_2.addWidget(self.splitter)

        self.verticalLayout_2.addWidget(self.splitter_2)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.pushBtnProceed = QPushButton(Form)
        self.pushBtnProceed.setObjectName(u"pushBtnProceed")

        self.verticalLayout_2.addWidget(self.pushBtnProceed)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Tab 2", None))
        self.labelTechCA.setText(QCoreApplication.translate("Form", u"CA", None))
        self.labelTechCP.setText(QCoreApplication.translate("Form", u"CP", None))
        self.labelTechCV.setText(QCoreApplication.translate("Form", u"CV", None))
        self.labelTechEIS.setText(QCoreApplication.translate("Form", u"EIS", None))
        self.labelTechLoop.setText(QCoreApplication.translate("Form", u"Loop", None))
        self.pushBtnProceed.setText(QCoreApplication.translate("Form", u"Proceed", None))
    # retranslateUi

