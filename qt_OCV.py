# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_OCV.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 2, 0, 1, 2)

        self.labelSampleTime = QLabel(Form)
        self.labelSampleTime.setObjectName(u"labelSampleTime")

        self.gridLayout.addWidget(self.labelSampleTime, 3, 0, 1, 1)

        self.lineEditSampleTime = QLineEdit(Form)
        self.lineEditSampleTime.setObjectName(u"lineEditSampleTime")

        self.gridLayout.addWidget(self.lineEditSampleTime, 3, 1, 1, 1)

        self.lineEditDuration = QLineEdit(Form)
        self.lineEditDuration.setObjectName(u"lineEditDuration")

        self.gridLayout.addWidget(self.lineEditDuration, 1, 1, 1, 1)

        self.labelDuration = QLabel(Form)
        self.labelDuration.setObjectName(u"labelDuration")

        self.gridLayout.addWidget(self.labelDuration, 1, 0, 1, 1)

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setObjectName(u"lineEditName")

        self.gridLayout.addWidget(self.lineEditName, 0, 1, 1, 1)

        self.labelSampleCurrent = QLabel(Form)
        self.labelSampleCurrent.setObjectName(u"labelSampleCurrent")

        self.gridLayout.addWidget(self.labelSampleCurrent, 4, 0, 1, 1)

        self.lineEditSampleCurrent = QLineEdit(Form)
        self.lineEditSampleCurrent.setObjectName(u"lineEditSampleCurrent")

        self.gridLayout.addWidget(self.lineEditSampleCurrent, 4, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.plainTextEdit = QPlainTextEdit(Form)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.horizontalLayout.addWidget(self.plainTextEdit)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelSampleTime.setText(QCoreApplication.translate("Form", u"Sample per time /  s ", None))
        self.lineEditSampleTime.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditDuration.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.labelDuration.setText(QCoreApplication.translate("Form", u"Duration / s", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name", None))
        self.lineEditName.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
        self.labelSampleCurrent.setText(QCoreApplication.translate("Form", u"Sample per potential /  V ", None))
        self.lineEditSampleCurrent.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
    # retranslateUi

