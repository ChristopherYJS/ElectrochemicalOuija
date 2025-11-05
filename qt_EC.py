# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_EC.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QPushButton, QScrollArea, QSizePolicy, QSplitter,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1091, 712)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter_2 = QSplitter(Form)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.widget_2 = QWidget(self.splitter_2)
        self.widget_2.setObjectName(u"widget_2")
        self.splitter_2.addWidget(self.widget_2)
        self.widget = QWidget(self.splitter_2)
        self.widget.setObjectName(u"widget")
        self.splitter_2.addWidget(self.widget)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Vertical)
        self.treeWidget = QTreeWidget(self.splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.treeWidget)
        self.scrollAreaOption = QScrollArea(self.splitter)
        self.scrollAreaOption.setObjectName(u"scrollAreaOption")
        sizePolicy.setHeightForWidth(self.scrollAreaOption.sizePolicy().hasHeightForWidth())
        self.scrollAreaOption.setSizePolicy(sizePolicy)
        self.scrollAreaOption.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 595, 126))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents_3.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_3.setSizePolicy(sizePolicy1)
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

        self.labelMove = QLabel(self.scrollAreaWidgetContents_3)
        self.labelMove.setObjectName(u"labelMove")

        self.verticalLayout.addWidget(self.labelMove)

        self.labelLoop = QLabel(self.scrollAreaWidgetContents_3)
        self.labelLoop.setObjectName(u"labelLoop")

        self.verticalLayout.addWidget(self.labelLoop)

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

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelTechCA.setText(QCoreApplication.translate("Form", u"CA", None))
        self.labelTechCP.setText(QCoreApplication.translate("Form", u"CP", None))
        self.labelTechCV.setText(QCoreApplication.translate("Form", u"CV", None))
        self.labelTechEIS.setText(QCoreApplication.translate("Form", u"EIS", None))
        self.labelMove.setText(QCoreApplication.translate("Form", u"Move", None))
        self.labelLoop.setText(QCoreApplication.translate("Form", u"Loop", None))
        self.pushBtnProceed.setText(QCoreApplication.translate("Form", u"Proceed", None))
    # retranslateUi

