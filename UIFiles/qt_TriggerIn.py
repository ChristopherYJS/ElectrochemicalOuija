# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_TriggerIn.ui'
##
## Created manually to match the existing generated qt_*.py pattern in this repo
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject
from PySide6.QtWidgets import QFormLayout, QLabel, QLineEdit, QWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)

        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")

        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")
        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelName)

        self.lineEditName = QLineEdit(Form)
        self.lineEditName.setObjectName(u"lineEditName")
        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEditName)

        self.labelIter = QLabel(Form)
        self.labelIter.setObjectName(u"labelIter")
        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelIter)

        self.lineEditIter = QLineEdit(Form)
        self.lineEditIter.setObjectName(u"lineEditIter")
        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineEditIter)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name", None))
        self.lineEditName.setPlaceholderText(QCoreApplication.translate("Form", u"<string>", None))
        self.labelIter.setText(QCoreApplication.translate("Form", u"Logic", None))
        self.lineEditIter.setText(QCoreApplication.translate("Form", u"1", None))
        self.lineEditIter.setPlaceholderText(QCoreApplication.translate("Form", u"<0 or 1>", None))