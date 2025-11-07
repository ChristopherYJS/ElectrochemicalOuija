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
    QLabel, QLayout, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(662, 636)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBoxDuration = QComboBox(Form)
        self.comboBoxDuration.addItem("")
        self.comboBoxDuration.addItem("")
        self.comboBoxDuration.addItem("")
        self.comboBoxDuration.setObjectName(u"comboBoxDuration")

        self.gridLayout.addWidget(self.comboBoxDuration, 2, 2, 1, 1)

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setObjectName(u"lineEditName")

        self.gridLayout.addWidget(self.lineEditName, 0, 1, 1, 2)

        self.labelBW = QLabel(Form)
        self.labelBW.setObjectName(u"labelBW")

        self.gridLayout.addWidget(self.labelBW, 12, 0, 1, 1)

        self.lineEditCurrent = QLineEdit(Form)
        self.lineEditCurrent.setObjectName(u"lineEditCurrent")

        self.gridLayout.addWidget(self.lineEditCurrent, 1, 1, 1, 2)

        self.lineEditSampleRate = QLineEdit(Form)
        self.lineEditSampleRate.setObjectName(u"lineEditSampleRate")

        self.gridLayout.addWidget(self.lineEditSampleRate, 3, 1, 1, 2)

        self.lineEditAREnd = QLineEdit(Form)
        self.lineEditAREnd.setObjectName(u"lineEditAREnd")

        self.gridLayout.addWidget(self.lineEditAREnd, 4, 2, 1, 1)

        self.labelUpperLimit = QLabel(Form)
        self.labelUpperLimit.setObjectName(u"labelUpperLimit")

        self.gridLayout.addWidget(self.labelUpperLimit, 8, 0, 1, 1)

        self.labelAverageRegion = QLabel(Form)
        self.labelAverageRegion.setObjectName(u"labelAverageRegion")

        self.gridLayout.addWidget(self.labelAverageRegion, 4, 0, 1, 1)

        self.lineEditARBegin = QLineEdit(Form)
        self.lineEditARBegin.setObjectName(u"lineEditARBegin")

        self.gridLayout.addWidget(self.lineEditARBegin, 4, 1, 1, 1)

        self.comboBoxLowerLimit = QComboBox(Form)
        self.comboBoxLowerLimit.addItem("")
        self.comboBoxLowerLimit.addItem("")
        self.comboBoxLowerLimit.setObjectName(u"comboBoxLowerLimit")

        self.gridLayout.addWidget(self.comboBoxLowerLimit, 7, 1, 1, 1)

        self.labelAverage = QLabel(Form)
        self.labelAverage.setObjectName(u"labelAverage")

        self.gridLayout.addWidget(self.labelAverage, 5, 0, 1, 1)

        self.labelLowerLimit = QLabel(Form)
        self.labelLowerLimit.setObjectName(u"labelLowerLimit")

        self.gridLayout.addWidget(self.labelLowerLimit, 7, 0, 1, 1)

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.lineEditAverage = QLineEdit(Form)
        self.lineEditAverage.setObjectName(u"lineEditAverage")

        self.gridLayout.addWidget(self.lineEditAverage, 5, 1, 1, 2)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.labelSampleRate = QLabel(Form)
        self.labelSampleRate.setObjectName(u"labelSampleRate")

        self.gridLayout.addWidget(self.labelSampleRate, 3, 0, 1, 1)

        self.lineEditDuration = QLineEdit(Form)
        self.lineEditDuration.setObjectName(u"lineEditDuration")

        self.gridLayout.addWidget(self.lineEditDuration, 2, 1, 1, 1)

        self.labelCR = QLabel(Form)
        self.labelCR.setObjectName(u"labelCR")

        self.gridLayout.addWidget(self.labelCR, 11, 0, 1, 1)

        self.lineEditLowerLimit = QLineEdit(Form)
        self.lineEditLowerLimit.setObjectName(u"lineEditLowerLimit")

        self.gridLayout.addWidget(self.lineEditLowerLimit, 7, 2, 1, 1)

        self.comboBoxUpperLimit = QComboBox(Form)
        self.comboBoxUpperLimit.addItem("")
        self.comboBoxUpperLimit.addItem("")
        self.comboBoxUpperLimit.setObjectName(u"comboBoxUpperLimit")

        self.gridLayout.addWidget(self.comboBoxUpperLimit, 8, 1, 1, 1)

        self.comboBoxPR = QComboBox(Form)
        self.comboBoxPR.setObjectName(u"comboBoxPR")

        self.gridLayout.addWidget(self.comboBoxPR, 10, 1, 1, 2)

        self.comboBoxBW = QComboBox(Form)
        self.comboBoxBW.setObjectName(u"comboBoxBW")

        self.gridLayout.addWidget(self.comboBoxBW, 12, 1, 1, 2)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 9, 0, 1, 3)

        self.comboBoxCR = QComboBox(Form)
        self.comboBoxCR.setObjectName(u"comboBoxCR")

        self.gridLayout.addWidget(self.comboBoxCR, 11, 1, 1, 2)

        self.labelPR = QLabel(Form)
        self.labelPR.setObjectName(u"labelPR")

        self.gridLayout.addWidget(self.labelPR, 10, 0, 1, 1)

        self.lineEditUpperLimit = QLineEdit(Form)
        self.lineEditUpperLimit.setObjectName(u"lineEditUpperLimit")

        self.gridLayout.addWidget(self.lineEditUpperLimit, 8, 2, 1, 1)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 6, 0, 1, 3)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.comboBoxDuration.setItemText(0, QCoreApplication.translate("Form", u"s", None))
        self.comboBoxDuration.setItemText(1, QCoreApplication.translate("Form", u"min", None))
        self.comboBoxDuration.setItemText(2, QCoreApplication.translate("Form", u"h", None))

        self.lineEditName.setPlaceholderText("")
        self.labelBW.setText(QCoreApplication.translate("Form", u"Bandwidth", None))
        self.lineEditSampleRate.setPlaceholderText(QCoreApplication.translate("Form", u"0.1", None))
        self.lineEditAREnd.setPlaceholderText(QCoreApplication.translate("Form", u"1", None))
        self.labelUpperLimit.setText(QCoreApplication.translate("Form", u"Upper limit", None))
        self.labelAverageRegion.setText(QCoreApplication.translate("Form", u"Average Region", None))
        self.lineEditARBegin.setPlaceholderText(QCoreApplication.translate("Form", u"0", None))
        self.comboBoxLowerLimit.setItemText(0, QCoreApplication.translate("Form", u"V", None))
        self.comboBoxLowerLimit.setItemText(1, QCoreApplication.translate("Form", u"mV", None))

        self.labelAverage.setText(QCoreApplication.translate("Form", u"Average", None))
        self.labelLowerLimit.setText(QCoreApplication.translate("Form", u"Lower limit", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label.setText(QCoreApplication.translate("Form", u"Current / A", None))
        self.lineEditAverage.setPlaceholderText(QCoreApplication.translate("Form", u"1", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Duration / s", None))
        self.labelSampleRate.setText(QCoreApplication.translate("Form", u"Sample rate / per s ", None))
        self.labelCR.setText(QCoreApplication.translate("Form", u"Current Range", None))
        self.lineEditLowerLimit.setPlaceholderText(QCoreApplication.translate("Form", u"pass", None))
        self.comboBoxUpperLimit.setItemText(0, QCoreApplication.translate("Form", u"V", None))
        self.comboBoxUpperLimit.setItemText(1, QCoreApplication.translate("Form", u"mV", None))

        self.labelPR.setText(QCoreApplication.translate("Form", u"Potential Range", None))
        self.lineEditUpperLimit.setPlaceholderText(QCoreApplication.translate("Form", u"pass", None))
    # retranslateUi

