# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_LSV.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(955, 721)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelStepHeight = QLabel(Form)
        self.labelStepHeight.setObjectName(u"labelStepHeight")

        self.gridLayout.addWidget(self.labelStepHeight, 5, 0, 1, 1)

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.labelPotentialEnd = QLabel(Form)
        self.labelPotentialEnd.setObjectName(u"labelPotentialEnd")

        self.gridLayout.addWidget(self.labelPotentialEnd, 2, 0, 1, 1)

        self.labelStepLength = QLabel(Form)
        self.labelStepLength.setObjectName(u"labelStepLength")

        self.gridLayout.addWidget(self.labelStepLength, 6, 0, 1, 1)

        self.labelScanRate = QLabel(Form)
        self.labelScanRate.setObjectName(u"labelScanRate")

        self.gridLayout.addWidget(self.labelScanRate, 3, 0, 1, 1)

        self.labelPotentialStart = QLabel(Form)
        self.labelPotentialStart.setObjectName(u"labelPotentialStart")

        self.gridLayout.addWidget(self.labelPotentialStart, 1, 0, 1, 1)

        self.labelSampleRange = QLabel(Form)
        self.labelSampleRange.setObjectName(u"labelSampleRange")

        self.gridLayout.addWidget(self.labelSampleRange, 8, 0, 1, 1)

        self.labelAverageRange = QLabel(Form)
        self.labelAverageRange.setObjectName(u"labelAverageRange")

        self.gridLayout.addWidget(self.labelAverageRange, 9, 0, 1, 1)

        self.labelAverageRegion = QLabel(Form)
        self.labelAverageRegion.setObjectName(u"labelAverageRegion")

        self.gridLayout.addWidget(self.labelAverageRegion, 10, 0, 1, 1)

        self.lineEditARBegin = QLineEdit(Form)
        self.lineEditARBegin.setObjectName(u"lineEditARBegin")

        self.gridLayout.addWidget(self.lineEditARBegin, 10, 1, 1, 1)

        self.lineEditAREnd = QLineEdit(Form)
        self.lineEditAREnd.setObjectName(u"lineEditAREnd")

        self.gridLayout.addWidget(self.lineEditAREnd, 10, 2, 1, 1)

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setObjectName(u"lineEditName")

        self.gridLayout.addWidget(self.lineEditName, 0, 1, 1, 2)

        self.lineEditPotentialStart = QLineEdit(Form)
        self.lineEditPotentialStart.setObjectName(u"lineEditPotentialStart")

        self.gridLayout.addWidget(self.lineEditPotentialStart, 1, 1, 1, 2)

        self.lineEditPotentialEnd = QLineEdit(Form)
        self.lineEditPotentialEnd.setObjectName(u"lineEditPotentialEnd")

        self.gridLayout.addWidget(self.lineEditPotentialEnd, 2, 1, 1, 2)

        self.lineEditScanRate = QLineEdit(Form)
        self.lineEditScanRate.setObjectName(u"lineEditScanRate")

        self.gridLayout.addWidget(self.lineEditScanRate, 3, 1, 1, 2)

        self.lineEditStepHeight = QLineEdit(Form)
        self.lineEditStepHeight.setObjectName(u"lineEditStepHeight")

        self.gridLayout.addWidget(self.lineEditStepHeight, 5, 1, 1, 2)

        self.lineEditStepLength = QLineEdit(Form)
        self.lineEditStepLength.setObjectName(u"lineEditStepLength")

        self.gridLayout.addWidget(self.lineEditStepLength, 6, 1, 1, 2)

        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_3, 7, 0, 1, 3)

        self.lineEditSampleRange = QLineEdit(Form)
        self.lineEditSampleRange.setObjectName(u"lineEditSampleRange")

        self.gridLayout.addWidget(self.lineEditSampleRange, 8, 1, 1, 2)

        self.lineEditAverageRange = QLineEdit(Form)
        self.lineEditAverageRange.setObjectName(u"lineEditAverageRange")

        self.gridLayout.addWidget(self.lineEditAverageRange, 9, 1, 1, 2)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 4, 0, 1, 3)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelStepHeight.setText(QCoreApplication.translate("Form", u"Step Height / mV", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name", None))
        self.labelPotentialEnd.setText(QCoreApplication.translate("Form", u"Ending Potential / V ", None))
        self.labelStepLength.setText(QCoreApplication.translate("Form", u"Step Length / ms", None))
        self.labelScanRate.setText(QCoreApplication.translate("Form", u"Scan rate / V per s", None))
        self.labelPotentialStart.setText(QCoreApplication.translate("Form", u"Starting Potential / V ", None))
        self.labelSampleRange.setText(QCoreApplication.translate("Form", u"Sample per voltage", None))
        self.labelAverageRange.setText(QCoreApplication.translate("Form", u"Average per voltage", None))
        self.labelAverageRegion.setText(QCoreApplication.translate("Form", u"Average Region", None))
        self.lineEditARBegin.setPlaceholderText(QCoreApplication.translate("Form", u"<float, 0 to 1>", None))
        self.lineEditAREnd.setPlaceholderText(QCoreApplication.translate("Form", u"<float, 0 to 1>", None))
        self.lineEditName.setPlaceholderText("")
        self.lineEditPotentialStart.setPlaceholderText("")
        self.lineEditPotentialEnd.setPlaceholderText("")
        self.lineEditScanRate.setPlaceholderText("")
        self.lineEditStepHeight.setPlaceholderText("")
        self.lineEditStepLength.setPlaceholderText("")
        self.lineEditSampleRange.setPlaceholderText("")
        self.lineEditAverageRange.setPlaceholderText("")
    # retranslateUi

