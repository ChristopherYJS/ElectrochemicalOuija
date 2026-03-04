# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_Loop.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.labelIter = QLabel(Form)
        self.labelIter.setObjectName(u"labelIter")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelIter)

        self.lineEditIter = QLineEdit(Form)
        self.lineEditIter.setObjectName(u"lineEditIter")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineEditIter)

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelName)

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setObjectName(u"lineEditName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEditName)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelIter.setText(QCoreApplication.translate("Form", u"Number of iteration", None))
        self.lineEditIter.setText(QCoreApplication.translate("Form", u"2", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name", None))
        self.lineEditName.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
    # retranslateUi

