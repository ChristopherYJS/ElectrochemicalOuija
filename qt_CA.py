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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QPlainTextEdit, QRadioButton, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 404)
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
        self.comboBoxDuration = QComboBox(Form)
        self.comboBoxDuration.addItem("")
        self.comboBoxDuration.addItem("")
        self.comboBoxDuration.addItem("")
        self.comboBoxDuration.setObjectName(u"comboBoxDuration")

        self.gridLayout.addWidget(self.comboBoxDuration, 3, 2, 1, 1)

        self.radioButtonOCP = QRadioButton(Form)
        self.buttonGroup = QButtonGroup(Form)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButtonOCP)
        self.radioButtonOCP.setObjectName(u"radioButtonOCP")
        self.radioButtonOCP.setAutoExclusive(False)

        self.gridLayout.addWidget(self.radioButtonOCP, 2, 2, 1, 1)

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setObjectName(u"lineEditName")

        self.gridLayout.addWidget(self.lineEditName, 0, 1, 1, 2)

        self.labelDuration = QLabel(Form)
        self.labelDuration.setObjectName(u"labelDuration")

        self.gridLayout.addWidget(self.labelDuration, 3, 0, 1, 1)

        self.lineEditARBegin = QLineEdit(Form)
        self.lineEditARBegin.setObjectName(u"lineEditARBegin")

        self.gridLayout.addWidget(self.lineEditARBegin, 6, 1, 1, 1)

        self.labelBW = QLabel(Form)
        self.labelBW.setObjectName(u"labelBW")

        self.gridLayout.addWidget(self.labelBW, 13, 0, 1, 1)

        self.comboBoxBW = QComboBox(Form)
        self.comboBoxBW.setObjectName(u"comboBoxBW")

        self.gridLayout.addWidget(self.comboBoxBW, 13, 1, 1, 2)

        self.labelAverage = QLabel(Form)
        self.labelAverage.setObjectName(u"labelAverage")

        self.gridLayout.addWidget(self.labelAverage, 8, 0, 1, 1)

        self.lineEditLowerLimit = QLineEdit(Form)
        self.lineEditLowerLimit.setObjectName(u"lineEditLowerLimit")

        self.gridLayout.addWidget(self.lineEditLowerLimit, 10, 2, 1, 1)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 4, 0, 1, 3)

        self.comboBoxLowerLimit = QComboBox(Form)
        self.comboBoxLowerLimit.addItem("")
        self.comboBoxLowerLimit.addItem("")
        self.comboBoxLowerLimit.addItem("")
        self.comboBoxLowerLimit.addItem("")
        self.comboBoxLowerLimit.setObjectName(u"comboBoxLowerLimit")

        self.gridLayout.addWidget(self.comboBoxLowerLimit, 10, 1, 1, 1)

        self.labelLowerLimit = QLabel(Form)
        self.labelLowerLimit.setObjectName(u"labelLowerLimit")

        self.gridLayout.addWidget(self.labelLowerLimit, 10, 0, 1, 1)

        self.labelSampleRate = QLabel(Form)
        self.labelSampleRate.setObjectName(u"labelSampleRate")

        self.gridLayout.addWidget(self.labelSampleRate, 5, 0, 1, 1)

        self.labelCR = QLabel(Form)
        self.labelCR.setObjectName(u"labelCR")

        self.gridLayout.addWidget(self.labelCR, 11, 0, 1, 1)

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.labelAverageRegion = QLabel(Form)
        self.labelAverageRegion.setObjectName(u"labelAverageRegion")

        self.gridLayout.addWidget(self.labelAverageRegion, 6, 0, 1, 1)

        self.lineEditSampleRate = QLineEdit(Form)
        self.lineEditSampleRate.setObjectName(u"lineEditSampleRate")

        self.gridLayout.addWidget(self.lineEditSampleRate, 5, 1, 1, 2)

        self.labelPotentialRef = QLabel(Form)
        self.labelPotentialRef.setObjectName(u"labelPotentialRef")

        self.gridLayout.addWidget(self.labelPotentialRef, 2, 0, 1, 1)

        self.lineEditAREnd = QLineEdit(Form)
        self.lineEditAREnd.setObjectName(u"lineEditAREnd")

        self.gridLayout.addWidget(self.lineEditAREnd, 6, 2, 1, 1)

        self.comboBoxCR = QComboBox(Form)
        self.comboBoxCR.setObjectName(u"comboBoxCR")

        self.gridLayout.addWidget(self.comboBoxCR, 11, 1, 1, 2)

        self.radioButtonRE = QRadioButton(Form)
        self.buttonGroup.addButton(self.radioButtonRE)
        self.radioButtonRE.setObjectName(u"radioButtonRE")
        self.radioButtonRE.setChecked(True)
        self.radioButtonRE.setAutoExclusive(False)

        self.gridLayout.addWidget(self.radioButtonRE, 2, 1, 1, 1)

        self.labelPotential = QLabel(Form)
        self.labelPotential.setObjectName(u"labelPotential")

        self.gridLayout.addWidget(self.labelPotential, 1, 0, 1, 1)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 7, 0, 1, 3)

        self.lineEditAverage = QLineEdit(Form)
        self.lineEditAverage.setObjectName(u"lineEditAverage")

        self.gridLayout.addWidget(self.lineEditAverage, 8, 1, 1, 2)

        self.lineEditPotential = QLineEdit(Form)
        self.lineEditPotential.setObjectName(u"lineEditPotential")

        self.gridLayout.addWidget(self.lineEditPotential, 1, 1, 1, 2)

        self.lineEditUpperLimit = QLineEdit(Form)
        self.lineEditUpperLimit.setObjectName(u"lineEditUpperLimit")

        self.gridLayout.addWidget(self.lineEditUpperLimit, 9, 2, 1, 1)

        self.labelUpperLimit = QLabel(Form)
        self.labelUpperLimit.setObjectName(u"labelUpperLimit")

        self.gridLayout.addWidget(self.labelUpperLimit, 9, 0, 1, 1)

        self.comboBoxUpperLimit = QComboBox(Form)
        self.comboBoxUpperLimit.addItem("")
        self.comboBoxUpperLimit.addItem("")
        self.comboBoxUpperLimit.addItem("")
        self.comboBoxUpperLimit.addItem("")
        self.comboBoxUpperLimit.setObjectName(u"comboBoxUpperLimit")

        self.gridLayout.addWidget(self.comboBoxUpperLimit, 9, 1, 1, 1)

        self.lineEditDuration = QLineEdit(Form)
        self.lineEditDuration.setObjectName(u"lineEditDuration")

        self.gridLayout.addWidget(self.lineEditDuration, 3, 1, 1, 1)

        self.labelPR = QLabel(Form)
        self.labelPR.setObjectName(u"labelPR")

        self.gridLayout.addWidget(self.labelPR, 12, 0, 1, 1)

        self.comboBoxPR = QComboBox(Form)
        self.comboBoxPR.setObjectName(u"comboBoxPR")

        self.gridLayout.addWidget(self.comboBoxPR, 12, 1, 1, 2)


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
        self.comboBoxDuration.setItemText(0, QCoreApplication.translate("Form", u"s", None))
        self.comboBoxDuration.setItemText(1, QCoreApplication.translate("Form", u"min", None))
        self.comboBoxDuration.setItemText(2, QCoreApplication.translate("Form", u"h", None))

        self.radioButtonOCP.setText(QCoreApplication.translate("Form", u"OCP", None))
        self.lineEditName.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
        self.labelDuration.setText(QCoreApplication.translate("Form", u"Duration / s", None))
        self.lineEditARBegin.setPlaceholderText(QCoreApplication.translate("Form", u"<float, 0 to 1>", None))
        self.labelBW.setText(QCoreApplication.translate("Form", u"Bandwidth", None))
        self.labelAverage.setText(QCoreApplication.translate("Form", u"Average", None))
        self.lineEditLowerLimit.setPlaceholderText(QCoreApplication.translate("Form", u"<float or pass>", None))
        self.comboBoxLowerLimit.setItemText(0, QCoreApplication.translate("Form", u"A", None))
        self.comboBoxLowerLimit.setItemText(1, QCoreApplication.translate("Form", u"mA", None))
        self.comboBoxLowerLimit.setItemText(2, QCoreApplication.translate("Form", u"uA", None))
        self.comboBoxLowerLimit.setItemText(3, QCoreApplication.translate("Form", u"nA", None))

        self.labelLowerLimit.setText(QCoreApplication.translate("Form", u"Lower limit", None))
        self.labelSampleRate.setText(QCoreApplication.translate("Form", u"Sample rate / per s ", None))
        self.labelCR.setText(QCoreApplication.translate("Form", u"Current Range", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name", None))
        self.labelAverageRegion.setText(QCoreApplication.translate("Form", u"Average Region", None))
        self.lineEditSampleRate.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.labelPotentialRef.setText(QCoreApplication.translate("Form", u"Potential Ref", None))
        self.lineEditAREnd.setPlaceholderText(QCoreApplication.translate("Form", u"<float, 0 to 1>", None))
        self.radioButtonRE.setText(QCoreApplication.translate("Form", u"RE", None))
        self.labelPotential.setText(QCoreApplication.translate("Form", u"Potential / V", None))
        self.lineEditAverage.setPlaceholderText(QCoreApplication.translate("Form", u"<int>", None))
        self.lineEditPotential.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditUpperLimit.setPlaceholderText(QCoreApplication.translate("Form", u"<float or pass>", None))
        self.labelUpperLimit.setText(QCoreApplication.translate("Form", u"Upper limit", None))
        self.comboBoxUpperLimit.setItemText(0, QCoreApplication.translate("Form", u"A", None))
        self.comboBoxUpperLimit.setItemText(1, QCoreApplication.translate("Form", u"mA", None))
        self.comboBoxUpperLimit.setItemText(2, QCoreApplication.translate("Form", u"uA", None))
        self.comboBoxUpperLimit.setItemText(3, QCoreApplication.translate("Form", u"nA", None))

        self.lineEditDuration.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.labelPR.setText(QCoreApplication.translate("Form", u"Potential Range", None))
    # retranslateUi

