# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CA.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
    QGridLayout, QLabel, QLineEdit, QRadioButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 487)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBoxLowerLimit = QComboBox(Form)
        self.comboBoxLowerLimit.addItem("")
        self.comboBoxLowerLimit.addItem("")
        self.comboBoxLowerLimit.addItem("")
        self.comboBoxLowerLimit.addItem("")
        self.comboBoxLowerLimit.setObjectName(u"comboBoxLowerLimit")

        self.gridLayout.addWidget(self.comboBoxLowerLimit, 10, 1, 1, 1)

        self.lineEditLowerLimit = QLineEdit(Form)
        self.lineEditLowerLimit.setObjectName(u"lineEditLowerLimit")

        self.gridLayout.addWidget(self.lineEditLowerLimit, 10, 2, 1, 1)

        self.lineEditUpperLimit = QLineEdit(Form)
        self.lineEditUpperLimit.setObjectName(u"lineEditUpperLimit")

        self.gridLayout.addWidget(self.lineEditUpperLimit, 9, 2, 1, 1)

        self.radioButtonRE = QRadioButton(Form)
        self.buttonGroup = QButtonGroup(Form)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButtonRE)
        self.radioButtonRE.setObjectName(u"radioButtonRE")
        self.radioButtonRE.setChecked(True)
        self.radioButtonRE.setAutoExclusive(False)

        self.gridLayout.addWidget(self.radioButtonRE, 2, 2, 1, 1)

        self.labelAverage = QLabel(Form)
        self.labelAverage.setObjectName(u"labelAverage")

        self.gridLayout.addWidget(self.labelAverage, 7, 0, 1, 1)

        self.radioButtonOCP = QRadioButton(Form)
        self.buttonGroup.addButton(self.radioButtonOCP)
        self.radioButtonOCP.setObjectName(u"radioButtonOCP")
        self.radioButtonOCP.setAutoExclusive(False)

        self.gridLayout.addWidget(self.radioButtonOCP, 3, 2, 1, 1)

        self.labelDuration = QLabel(Form)
        self.labelDuration.setObjectName(u"labelDuration")

        self.gridLayout.addWidget(self.labelDuration, 4, 0, 1, 1)

        self.lineEditDuration = QLineEdit(Form)
        self.lineEditDuration.setObjectName(u"lineEditDuration")

        self.gridLayout.addWidget(self.lineEditDuration, 4, 2, 1, 1)

        self.labelPotentialRef = QLabel(Form)
        self.labelPotentialRef.setObjectName(u"labelPotentialRef")

        self.gridLayout.addWidget(self.labelPotentialRef, 2, 0, 1, 1)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 5, 0, 1, 3)

        self.labelPotential = QLabel(Form)
        self.labelPotential.setObjectName(u"labelPotential")

        self.gridLayout.addWidget(self.labelPotential, 1, 0, 1, 1)

        self.labelSampleRate = QLabel(Form)
        self.labelSampleRate.setObjectName(u"labelSampleRate")

        self.gridLayout.addWidget(self.labelSampleRate, 6, 0, 1, 1)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 8, 0, 1, 3)

        self.labelUpperLimit = QLabel(Form)
        self.labelUpperLimit.setObjectName(u"labelUpperLimit")

        self.gridLayout.addWidget(self.labelUpperLimit, 9, 0, 1, 1)

        self.lineEditAverage = QLineEdit(Form)
        self.lineEditAverage.setObjectName(u"lineEditAverage")

        self.gridLayout.addWidget(self.lineEditAverage, 7, 2, 1, 1)

        self.lineEditPotential = QLineEdit(Form)
        self.lineEditPotential.setObjectName(u"lineEditPotential")

        self.gridLayout.addWidget(self.lineEditPotential, 1, 2, 1, 1)

        self.lineEditSampleRate = QLineEdit(Form)
        self.lineEditSampleRate.setObjectName(u"lineEditSampleRate")

        self.gridLayout.addWidget(self.lineEditSampleRate, 6, 2, 1, 1)

        self.comboBoxUpperLimit = QComboBox(Form)
        self.comboBoxUpperLimit.addItem("")
        self.comboBoxUpperLimit.addItem("")
        self.comboBoxUpperLimit.addItem("")
        self.comboBoxUpperLimit.addItem("")
        self.comboBoxUpperLimit.setObjectName(u"comboBoxUpperLimit")

        self.gridLayout.addWidget(self.comboBoxUpperLimit, 9, 1, 1, 1)

        self.labelLowerLimit = QLabel(Form)
        self.labelLowerLimit.setObjectName(u"labelLowerLimit")

        self.gridLayout.addWidget(self.labelLowerLimit, 10, 0, 1, 1)

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setObjectName(u"lineEditName")

        self.gridLayout.addWidget(self.lineEditName, 0, 2, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.comboBoxLowerLimit.setItemText(0, QCoreApplication.translate("Form", u"A", None))
        self.comboBoxLowerLimit.setItemText(1, QCoreApplication.translate("Form", u"mA", None))
        self.comboBoxLowerLimit.setItemText(2, QCoreApplication.translate("Form", u"uA", None))
        self.comboBoxLowerLimit.setItemText(3, QCoreApplication.translate("Form", u"nA", None))

        self.lineEditLowerLimit.setPlaceholderText(QCoreApplication.translate("Form", u"pass", None))
        self.lineEditUpperLimit.setPlaceholderText(QCoreApplication.translate("Form", u"pass", None))
        self.radioButtonRE.setText(QCoreApplication.translate("Form", u"RE", None))
        self.labelAverage.setText(QCoreApplication.translate("Form", u"Average", None))
        self.radioButtonOCP.setText(QCoreApplication.translate("Form", u"OCP", None))
        self.labelDuration.setText(QCoreApplication.translate("Form", u"Duration / s", None))
        self.lineEditDuration.setPlaceholderText(QCoreApplication.translate("Form", u"60", None))
        self.labelPotentialRef.setText(QCoreApplication.translate("Form", u"Potential Ref", None))
        self.labelPotential.setText(QCoreApplication.translate("Form", u"Potential / V", None))
        self.labelSampleRate.setText(QCoreApplication.translate("Form", u"Sample rate / per s ", None))
        self.labelUpperLimit.setText(QCoreApplication.translate("Form", u"Upper limit", None))
        self.lineEditAverage.setPlaceholderText(QCoreApplication.translate("Form", u"1", None))
        self.lineEditPotential.setPlaceholderText(QCoreApplication.translate("Form", u"0.0", None))
        self.lineEditSampleRate.setPlaceholderText(QCoreApplication.translate("Form", u"0.1", None))
        self.comboBoxUpperLimit.setItemText(0, QCoreApplication.translate("Form", u"A", None))
        self.comboBoxUpperLimit.setItemText(1, QCoreApplication.translate("Form", u"mA", None))
        self.comboBoxUpperLimit.setItemText(2, QCoreApplication.translate("Form", u"uA", None))
        self.comboBoxUpperLimit.setItemText(3, QCoreApplication.translate("Form", u"nA", None))

        self.labelLowerLimit.setText(QCoreApplication.translate("Form", u"Lower limit", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name", None))
        self.lineEditName.setPlaceholderText("")
    # retranslateUi

