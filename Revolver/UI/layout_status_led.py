# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout_status_led.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(281, 27)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.formLayout = QtGui.QFormLayout(Form)
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.formLayout.setMargin(5)
        self.formLayout.setSpacing(5)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.status_led = QLed(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_led.sizePolicy().hasHeightForWidth())
        self.status_led.setSizePolicy(sizePolicy)
        self.status_led.setMinimumSize(QtCore.QSize(15, 15))
        self.status_led.setMaximumSize(QtCore.QSize(15, 15))
        self.status_led.setObjectName(_fromUtf8("status_led"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.status_led)
        self.device_name = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_name.sizePolicy().hasHeightForWidth())
        self.device_name.setSizePolicy(sizePolicy)
        self.device_name.setMinimumSize(QtCore.QSize(100, 0))
        self.device_name.setMaximumSize(QtCore.QSize(250, 16777215))
        self.device_name.setStyleSheet(_fromUtf8("font-weight:bold"))
        self.device_name.setObjectName(_fromUtf8("device_name"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.device_name)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Device led status", None))
        self.device_name.setText(_translate("Form", "Device name", None))

from taurus.qt.qtgui.display import QLed
