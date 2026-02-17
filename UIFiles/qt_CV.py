# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_CV.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(734, 332)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelPotentialSecond = QLabel(Form)
        self.labelPotentialSecond.setObjectName(u"labelPotentialSecond")

        self.gridLayout.addWidget(self.labelPotentialSecond, 3, 0, 1, 1)

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setObjectName(u"lineEditName")

        self.gridLayout.addWidget(self.lineEditName, 0, 1, 1, 1)

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.labelPotentialFirst = QLabel(Form)
        self.labelPotentialFirst.setObjectName(u"labelPotentialFirst")

        self.gridLayout.addWidget(self.labelPotentialFirst, 2, 0, 1, 1)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 8, 0, 1, 2)

        self.labelSamplePotential = QLabel(Form)
        self.labelSamplePotential.setObjectName(u"labelSamplePotential")

        self.gridLayout.addWidget(self.labelSamplePotential, 6, 0, 1, 1)

        self.lineEditRepeat = QLineEdit(Form)
        self.lineEditRepeat.setObjectName(u"lineEditRepeat")

        self.gridLayout.addWidget(self.lineEditRepeat, 7, 1, 1, 1)

        self.lineEditSamplePotential = QLineEdit(Form)
        self.lineEditSamplePotential.setObjectName(u"lineEditSamplePotential")

        self.gridLayout.addWidget(self.lineEditSamplePotential, 6, 1, 1, 1)

        self.lineEditStepBegin = QLineEdit(Form)
        self.lineEditStepBegin.setObjectName(u"lineEditStepBegin")

        self.gridLayout.addWidget(self.lineEditStepBegin, 10, 1, 1, 1)

        self.checkBoxAverage = QCheckBox(Form)
        self.checkBoxAverage.setObjectName(u"checkBoxAverage")

        self.gridLayout.addWidget(self.checkBoxAverage, 9, 1, 1, 1)

        self.labelAverage = QLabel(Form)
        self.labelAverage.setObjectName(u"labelAverage")

        self.gridLayout.addWidget(self.labelAverage, 9, 0, 1, 1)

        self.labelRepeat = QLabel(Form)
        self.labelRepeat.setObjectName(u"labelRepeat")

        self.gridLayout.addWidget(self.labelRepeat, 7, 0, 1, 1)

        self.labelScanRate = QLabel(Form)
        self.labelScanRate.setObjectName(u"labelScanRate")

        self.gridLayout.addWidget(self.labelScanRate, 5, 0, 1, 1)

        self.labelStepBegin = QLabel(Form)
        self.labelStepBegin.setObjectName(u"labelStepBegin")

        self.gridLayout.addWidget(self.labelStepBegin, 10, 0, 1, 1)

        self.lineEditPotentialInit = QLineEdit(Form)
        self.lineEditPotentialInit.setObjectName(u"lineEditPotentialInit")

        self.gridLayout.addWidget(self.lineEditPotentialInit, 1, 1, 1, 1)

        self.lineEditPotentialFirst = QLineEdit(Form)
        self.lineEditPotentialFirst.setObjectName(u"lineEditPotentialFirst")

        self.gridLayout.addWidget(self.lineEditPotentialFirst, 2, 1, 1, 1)

        self.lineEditPotentialFin = QLineEdit(Form)
        self.lineEditPotentialFin.setObjectName(u"lineEditPotentialFin")

        self.gridLayout.addWidget(self.lineEditPotentialFin, 4, 1, 1, 1)

        self.lineEditRate = QLineEdit(Form)
        self.lineEditRate.setObjectName(u"lineEditRate")

        self.gridLayout.addWidget(self.lineEditRate, 5, 1, 1, 1)

        self.lineEditPotentialSecond = QLineEdit(Form)
        self.lineEditPotentialSecond.setObjectName(u"lineEditPotentialSecond")

        self.gridLayout.addWidget(self.lineEditPotentialSecond, 3, 1, 1, 1)

        self.labelStepEnd = QLabel(Form)
        self.labelStepEnd.setObjectName(u"labelStepEnd")

        self.gridLayout.addWidget(self.labelStepEnd, 11, 0, 1, 1)

        self.lineEditStepEnd = QLineEdit(Form)
        self.lineEditStepEnd.setObjectName(u"lineEditStepEnd")

        self.gridLayout.addWidget(self.lineEditStepEnd, 11, 1, 1, 1)

        self.labelPotentialFin = QLabel(Form)
        self.labelPotentialFin.setObjectName(u"labelPotentialFin")

        self.gridLayout.addWidget(self.labelPotentialFin, 4, 0, 1, 1)

        self.labelPotentialInit = QLabel(Form)
        self.labelPotentialInit.setObjectName(u"labelPotentialInit")

        self.gridLayout.addWidget(self.labelPotentialInit, 1, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.horizontalLayout.setStretch(0, 2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelPotentialSecond.setText(QCoreApplication.translate("Form", u"Second potential / V", None))
        self.lineEditName.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name", None))
        self.labelPotentialFirst.setText(QCoreApplication.translate("Form", u"First potential / V", None))
        self.labelSamplePotential.setText(QCoreApplication.translate("Form", u"Sample per potential / V", None))
        self.lineEditRepeat.setPlaceholderText(QCoreApplication.translate("Form", u"<int>", None))
        self.lineEditSamplePotential.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditStepBegin.setPlaceholderText(QCoreApplication.translate("Form", u"<float: 0-1>", None))
        self.checkBoxAverage.setText(QCoreApplication.translate("Form", u"Average Current", None))
        self.labelAverage.setText(QCoreApplication.translate("Form", u"Average", None))
        self.labelRepeat.setText(QCoreApplication.translate("Form", u"Repeat", None))
        self.labelScanRate.setText(QCoreApplication.translate("Form", u"Scan rate / V/s", None))
        self.labelStepBegin.setText(QCoreApplication.translate("Form", u"Begin step", None))
        self.lineEditPotentialInit.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditPotentialFirst.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditPotentialFin.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditRate.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.lineEditPotentialSecond.setPlaceholderText(QCoreApplication.translate("Form", u"<float>", None))
        self.labelStepEnd.setText(QCoreApplication.translate("Form", u"End step", None))
        self.lineEditStepEnd.setPlaceholderText(QCoreApplication.translate("Form", u"<float: 0-1>", None))
        self.labelPotentialFin.setText(QCoreApplication.translate("Form", u"Final potential / V", None))
        self.labelPotentialInit.setText(QCoreApplication.translate("Form", u"Initial potentia / V ", None))
    # retranslateUi

