# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_CA.ui'
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
        Form.resize(654, 396)
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
        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 3, 0, 1, 3)

        self.lineEditSampleCurrent = QLineEdit(Form)
        self.lineEditSampleCurrent.setObjectName(u"lineEditSampleCurrent")

        self.gridLayout.addWidget(self.lineEditSampleCurrent, 5, 1, 1, 2)

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setObjectName(u"lineEditName")

        self.gridLayout.addWidget(self.lineEditName, 0, 1, 1, 2)

        self.labelPotential = QLabel(Form)
        self.labelPotential.setObjectName(u"labelPotential")

        self.gridLayout.addWidget(self.labelPotential, 1, 0, 1, 1)

        self.lineEditPotential = QLineEdit(Form)
        self.lineEditPotential.setObjectName(u"lineEditPotential")

        self.gridLayout.addWidget(self.lineEditPotential, 1, 1, 1, 2)

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.labelSampleTime = QLabel(Form)
        self.labelSampleTime.setObjectName(u"labelSampleTime")

        self.gridLayout.addWidget(self.labelSampleTime, 4, 0, 1, 1)

        self.labelDuration = QLabel(Form)
        self.labelDuration.setObjectName(u"labelDuration")

        self.gridLayout.addWidget(self.labelDuration, 2, 0, 1, 1)

        self.labelSampleCurrent = QLabel(Form)
        self.labelSampleCurrent.setObjectName(u"labelSampleCurrent")

        self.gridLayout.addWidget(self.labelSampleCurrent, 5, 0, 1, 1)

        self.lineEditSampleTime = QLineEdit(Form)
        self.lineEditSampleTime.setObjectName(u"lineEditSampleTime")

        self.gridLayout.addWidget(self.lineEditSampleTime, 4, 1, 1, 2)

        self.labelCR = QLabel(Form)
        self.labelCR.setObjectName(u"labelCR")

        self.gridLayout.addWidget(self.labelCR, 7, 0, 1, 1)

        self.lineEditDuration = QLineEdit(Form)
        self.lineEditDuration.setObjectName(u"lineEditDuration")

        self.gridLayout.addWidget(self.lineEditDuration, 2, 1, 1, 2)

        self.comboBoxCR = QComboBox(Form)
        self.comboBoxCR.setObjectName(u"comboBoxCR")

        self.gridLayout.addWidget(self.comboBoxCR, 7, 1, 1, 2)

        self.labelRepeat = QLabel(Form)
        self.labelRepeat.setObjectName(u"labelRepeat")

        self.gridLayout.addWidget(self.labelRepeat, 6, 0, 1, 1)

        self.lineEditRepeat = QLineEdit(Form)
        self.lineEditRepeat.setObjectName(u"lineEditRepeat")

        self.gridLayout.addWidget(self.lineEditRepeat, 6, 1, 1, 2)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.horizontalLayout.setStretch(0, 2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lineEditSampleCurrent.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditName.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
        self.labelPotential.setText(QCoreApplication.translate("Form", u"Potential / V", None))
        self.lineEditPotential.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name", None))
        self.labelSampleTime.setText(QCoreApplication.translate("Form", u"Sample per time /  s ", None))
        self.labelDuration.setText(QCoreApplication.translate("Form", u"Duration / s", None))
        self.labelSampleCurrent.setText(QCoreApplication.translate("Form", u"Sample per current / A", None))
        self.lineEditSampleTime.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.labelCR.setText(QCoreApplication.translate("Form", u"Current range", None))
        self.lineEditDuration.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.labelRepeat.setText(QCoreApplication.translate("Form", u"Repeat", None))
        self.lineEditRepeat.setPlaceholderText(QCoreApplication.translate("Form", u"<int>", None))
    # retranslateUi

