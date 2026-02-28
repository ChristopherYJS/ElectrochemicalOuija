# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_CP.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(662, 399)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEditSampleTime = QLineEdit(Form)
        self.lineEditSampleTime.setObjectName(u"lineEditSampleTime")

        self.gridLayout.addWidget(self.lineEditSampleTime, 4, 1, 1, 2)

        self.lineEditDuration = QLineEdit(Form)
        self.lineEditDuration.setObjectName(u"lineEditDuration")

        self.gridLayout.addWidget(self.lineEditDuration, 2, 1, 1, 2)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 3)

        self.lineEditCurrent = QLineEdit(Form)
        self.lineEditCurrent.setObjectName(u"lineEditCurrent")

        self.gridLayout.addWidget(self.lineEditCurrent, 1, 1, 1, 2)

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setObjectName(u"lineEditName")

        self.gridLayout.addWidget(self.lineEditName, 0, 1, 1, 2)

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.labelCR = QLabel(Form)
        self.labelCR.setObjectName(u"labelCR")

        self.gridLayout.addWidget(self.labelCR, 8, 0, 1, 1)

        self.comboBoxCR = QComboBox(Form)
        self.comboBoxCR.setObjectName(u"comboBoxCR")

        self.gridLayout.addWidget(self.comboBoxCR, 8, 1, 1, 2)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 7, 0, 1, 3)

        self.labelSampleCurrent = QLabel(Form)
        self.labelSampleCurrent.setObjectName(u"labelSampleCurrent")

        self.gridLayout.addWidget(self.labelSampleCurrent, 5, 0, 1, 1)

        self.labelSampleTime = QLabel(Form)
        self.labelSampleTime.setObjectName(u"labelSampleTime")

        self.gridLayout.addWidget(self.labelSampleTime, 4, 0, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.labelSampleRepeat = QLabel(Form)
        self.labelSampleRepeat.setObjectName(u"labelSampleRepeat")

        self.gridLayout.addWidget(self.labelSampleRepeat, 6, 0, 1, 1)

        self.lineEditSampleCurrent = QLineEdit(Form)
        self.lineEditSampleCurrent.setObjectName(u"lineEditSampleCurrent")

        self.gridLayout.addWidget(self.lineEditSampleCurrent, 5, 1, 1, 2)

        self.lineEditSampleRepeat = QLineEdit(Form)
        self.lineEditSampleRepeat.setObjectName(u"lineEditSampleRepeat")

        self.gridLayout.addWidget(self.lineEditSampleRepeat, 6, 1, 1, 2)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.horizontalLayout.setStretch(0, 2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lineEditSampleTime.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditDuration.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditCurrent.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditName.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name", None))
        self.labelCR.setText(QCoreApplication.translate("Form", u"Current Range", None))
        self.labelSampleCurrent.setText(QCoreApplication.translate("Form", u"Sample per potential /  V ", None))
        self.labelSampleTime.setText(QCoreApplication.translate("Form", u"Sample per time /  s ", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Duration / s", None))
        self.label.setText(QCoreApplication.translate("Form", u"Current / A", None))
        self.labelSampleRepeat.setText(QCoreApplication.translate("Form", u"Repeat", None))
        self.lineEditSampleCurrent.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditSampleRepeat.setPlaceholderText(QCoreApplication.translate("Form", u"<int>", None))
    # retranslateUi

