# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_EIS.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(692, 614)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelSweep = QLabel(Form)
        self.labelSweep.setObjectName(u"labelSweep")

        self.gridLayout.addWidget(self.labelSweep, 9, 0, 1, 1)

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setObjectName(u"lineEditName")

        self.gridLayout.addWidget(self.lineEditName, 0, 1, 1, 1)

        self.checkBoxSweep = QCheckBox(Form)
        self.checkBoxSweep.setObjectName(u"checkBoxSweep")

        self.gridLayout.addWidget(self.checkBoxSweep, 9, 1, 1, 1)

        self.lineEditAverage = QLineEdit(Form)
        self.lineEditAverage.setObjectName(u"lineEditAverage")

        self.gridLayout.addWidget(self.lineEditAverage, 12, 1, 1, 1)

        self.labelAverage = QLabel(Form)
        self.labelAverage.setObjectName(u"labelAverage")

        self.gridLayout.addWidget(self.labelAverage, 12, 0, 1, 1)

        self.labelAmp = QLabel(Form)
        self.labelAmp.setObjectName(u"labelAmp")

        self.gridLayout.addWidget(self.labelAmp, 10, 0, 1, 1)

        self.labelFreqFin = QLabel(Form)
        self.labelFreqFin.setObjectName(u"labelFreqFin")

        self.gridLayout.addWidget(self.labelFreqFin, 8, 0, 1, 1)

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.lineEditSampleTime = QLineEdit(Form)
        self.lineEditSampleTime.setObjectName(u"lineEditSampleTime")

        self.gridLayout.addWidget(self.lineEditSampleTime, 4, 1, 1, 1)

        self.labelSampleTime = QLabel(Form)
        self.labelSampleTime.setObjectName(u"labelSampleTime")

        self.gridLayout.addWidget(self.labelSampleTime, 4, 0, 1, 1)

        self.checkBoxCorrect = QCheckBox(Form)
        self.checkBoxCorrect.setObjectName(u"checkBoxCorrect")

        self.gridLayout.addWidget(self.checkBoxCorrect, 13, 1, 1, 1)

        self.labelPotential = QLabel(Form)
        self.labelPotential.setObjectName(u"labelPotential")

        self.gridLayout.addWidget(self.labelPotential, 1, 0, 1, 1)

        self.lineEditDuration = QLineEdit(Form)
        self.lineEditDuration.setObjectName(u"lineEditDuration")

        self.gridLayout.addWidget(self.lineEditDuration, 2, 1, 1, 1)

        self.lineEditFreqFin = QLineEdit(Form)
        self.lineEditFreqFin.setObjectName(u"lineEditFreqFin")

        self.gridLayout.addWidget(self.lineEditFreqFin, 8, 1, 1, 1)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 3, 0, 1, 2)

        self.labelSampleCurrent = QLabel(Form)
        self.labelSampleCurrent.setObjectName(u"labelSampleCurrent")

        self.gridLayout.addWidget(self.labelSampleCurrent, 5, 0, 1, 1)

        self.lineEditPotential = QLineEdit(Form)
        self.lineEditPotential.setObjectName(u"lineEditPotential")

        self.gridLayout.addWidget(self.lineEditPotential, 1, 1, 1, 1)

        self.labelDuration = QLabel(Form)
        self.labelDuration.setObjectName(u"labelDuration")

        self.gridLayout.addWidget(self.labelDuration, 2, 0, 1, 1)

        self.labelFreqInit = QLabel(Form)
        self.labelFreqInit.setObjectName(u"labelFreqInit")

        self.gridLayout.addWidget(self.labelFreqInit, 7, 0, 1, 1)

        self.lineEditFreqInit = QLineEdit(Form)
        self.lineEditFreqInit.setObjectName(u"lineEditFreqInit")

        self.gridLayout.addWidget(self.lineEditFreqInit, 7, 1, 1, 1)

        self.lineEditAmp = QLineEdit(Form)
        self.lineEditAmp.setObjectName(u"lineEditAmp")

        self.gridLayout.addWidget(self.lineEditAmp, 10, 1, 1, 1)

        self.labelNumber = QLabel(Form)
        self.labelNumber.setObjectName(u"labelNumber")

        self.gridLayout.addWidget(self.labelNumber, 11, 0, 1, 1)

        self.lineEditNumber = QLineEdit(Form)
        self.lineEditNumber.setObjectName(u"lineEditNumber")

        self.gridLayout.addWidget(self.lineEditNumber, 11, 1, 1, 1)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 6, 0, 1, 2)

        self.lineEditSampleCurrent = QLineEdit(Form)
        self.lineEditSampleCurrent.setObjectName(u"lineEditSampleCurrent")

        self.gridLayout.addWidget(self.lineEditSampleCurrent, 5, 1, 1, 1)

        self.labelCorrect = QLabel(Form)
        self.labelCorrect.setObjectName(u"labelCorrect")

        self.gridLayout.addWidget(self.labelCorrect, 13, 0, 1, 1)

        self.labelCorrectNum = QLabel(Form)
        self.labelCorrectNum.setObjectName(u"labelCorrectNum")

        self.gridLayout.addWidget(self.labelCorrectNum, 14, 0, 1, 1)

        self.lineEditCorrectNum = QLineEdit(Form)
        self.lineEditCorrectNum.setObjectName(u"lineEditCorrectNum")

        self.gridLayout.addWidget(self.lineEditCorrectNum, 14, 1, 1, 1)


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
        self.labelSweep.setText(QCoreApplication.translate("Form", u"Sweep linearly", None))
        self.lineEditName.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
        self.checkBoxSweep.setText(QCoreApplication.translate("Form", u"Check to sweep linearly otherwise logarithmically", None))
        self.lineEditAverage.setPlaceholderText(QCoreApplication.translate("Form", u"<int>", None))
        self.labelAverage.setText(QCoreApplication.translate("Form", u"Average", None))
        self.labelAmp.setText(QCoreApplication.translate("Form", u"Amplitude / V", None))
        self.labelFreqFin.setText(QCoreApplication.translate("Form", u"Final Freqency / Hz", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name", None))
        self.lineEditSampleTime.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.labelSampleTime.setText(QCoreApplication.translate("Form", u"Sample per time /  s ", None))
        self.checkBoxCorrect.setText(QCoreApplication.translate("Form", u"Allow correction", None))
        self.labelPotential.setText(QCoreApplication.translate("Form", u"Potential / V", None))
        self.lineEditDuration.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditFreqFin.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
        self.labelSampleCurrent.setText(QCoreApplication.translate("Form", u"Sample per current / A", None))
        self.lineEditPotential.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.labelDuration.setText(QCoreApplication.translate("Form", u"Duration / s", None))
        self.labelFreqInit.setText(QCoreApplication.translate("Form", u"Initial Freqency / Hz", None))
        self.lineEditFreqInit.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
        self.lineEditAmp.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
        self.labelNumber.setText(QCoreApplication.translate("Form", u"Number of frequencies", None))
        self.lineEditNumber.setPlaceholderText(QCoreApplication.translate("Form", u"<int>", None))
        self.lineEditSampleCurrent.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.labelCorrect.setText(QCoreApplication.translate("Form", u"Non-stationary correct", None))
        self.labelCorrectNum.setText(QCoreApplication.translate("Form", u"Number of period for correction", None))
        self.lineEditCorrectNum.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
    # retranslateUi

