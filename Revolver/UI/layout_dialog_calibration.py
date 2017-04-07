# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout_dialog_calibration.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(268, 187)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dsb_rby = QtGui.QDoubleSpinBox(Dialog)
        self.dsb_rby.setMinimumSize(QtCore.QSize(100, 30))
        self.dsb_rby.setMaximumSize(QtCore.QSize(16777215, 25))
        self.dsb_rby.setAlignment(QtCore.Qt.AlignCenter)
        self.dsb_rby.setDecimals(4)
        self.dsb_rby.setMinimum(-100.0)
        self.dsb_rby.setMaximum(100.0)
        self.dsb_rby.setSingleStep(0.01)
        self.dsb_rby.setObjectName(_fromUtf8("dsb_rby"))
        self.gridLayout.addWidget(self.dsb_rby, 2, 2, 1, 1)
        self.dsb_rbx = QtGui.QDoubleSpinBox(Dialog)
        self.dsb_rbx.setMinimumSize(QtCore.QSize(100, 30))
        self.dsb_rbx.setMaximumSize(QtCore.QSize(16777215, 25))
        self.dsb_rbx.setAlignment(QtCore.Qt.AlignCenter)
        self.dsb_rbx.setDecimals(4)
        self.dsb_rbx.setMinimum(-100.0)
        self.dsb_rbx.setMaximum(100.0)
        self.dsb_rbx.setSingleStep(0.01)
        self.dsb_rbx.setObjectName(_fromUtf8("dsb_rbx"))
        self.gridLayout.addWidget(self.dsb_rbx, 1, 2, 1, 1)
        self.btn_rbz = QtGui.QPushButton(Dialog)
        self.btn_rbz.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_rbz.setObjectName(_fromUtf8("btn_rbz"))
        self.gridLayout.addWidget(self.btn_rbz, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 2, 1, 1)
        self.btn_rbx = QtGui.QPushButton(Dialog)
        self.btn_rbx.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_rbx.setObjectName(_fromUtf8("btn_rbx"))
        self.gridLayout.addWidget(self.btn_rbx, 1, 0, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 5)
        self.dsb_rbz = QtGui.QDoubleSpinBox(Dialog)
        self.dsb_rbz.setMinimumSize(QtCore.QSize(100, 30))
        self.dsb_rbz.setMaximumSize(QtCore.QSize(16777215, 25))
        self.dsb_rbz.setAlignment(QtCore.Qt.AlignCenter)
        self.dsb_rbz.setDecimals(4)
        self.dsb_rbz.setMinimum(-100.0)
        self.dsb_rbz.setMaximum(100.0)
        self.dsb_rbz.setSingleStep(0.01)
        self.dsb_rbz.setObjectName(_fromUtf8("dsb_rbz"))
        self.gridLayout.addWidget(self.dsb_rbz, 3, 2, 1, 1)
        self.btn_rby = QtGui.QPushButton(Dialog)
        self.btn_rby.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_rby.setObjectName(_fromUtf8("btn_rby"))
        self.gridLayout.addWidget(self.btn_rby, 2, 0, 1, 1)
        self.btn_rbx_zero = QtGui.QPushButton(Dialog)
        self.btn_rbx_zero.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_rbx_zero.setObjectName(_fromUtf8("btn_rbx_zero"))
        self.gridLayout.addWidget(self.btn_rbx_zero, 1, 3, 1, 1)
        self.btn_rby_zero = QtGui.QPushButton(Dialog)
        self.btn_rby_zero.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_rby_zero.setObjectName(_fromUtf8("btn_rby_zero"))
        self.gridLayout.addWidget(self.btn_rby_zero, 2, 3, 1, 1)
        self.btn_rbz_zero = QtGui.QPushButton(Dialog)
        self.btn_rbz_zero.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_rbz_zero.setObjectName(_fromUtf8("btn_rbz_zero"))
        self.gridLayout.addWidget(self.btn_rbz_zero, 3, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.btn_rbx, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.actionSetMotorX)
        QtCore.QObject.connect(self.btn_rby, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.actionSetMotorY)
        QtCore.QObject.connect(self.btn_rbz, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.actionSetMotorZ)
        QtCore.QObject.connect(self.btn_rbx_zero, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.actionMotorXzero)
        QtCore.QObject.connect(self.btn_rby_zero, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.actionMotorYzero)
        QtCore.QObject.connect(self.btn_rbz_zero, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.actionMotorZzero)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.btn_rbx, self.dsb_rbx)
        Dialog.setTabOrder(self.dsb_rbx, self.btn_rbx_zero)
        Dialog.setTabOrder(self.btn_rbx_zero, self.btn_rby)
        Dialog.setTabOrder(self.btn_rby, self.dsb_rby)
        Dialog.setTabOrder(self.dsb_rby, self.btn_rby_zero)
        Dialog.setTabOrder(self.btn_rby_zero, self.btn_rbz)
        Dialog.setTabOrder(self.btn_rbz, self.dsb_rbz)
        Dialog.setTabOrder(self.dsb_rbz, self.btn_rbz_zero)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Calibrate Motor Positions", None))
        self.dsb_rby.setToolTip(_translate("Dialog", "Motor Position to be set as current", None))
        self.dsb_rbx.setToolTip(_translate("Dialog", "Motor Position to be set as current", None))
        self.btn_rbz.setToolTip(_translate("Dialog", "Calibrate Motor Position", None))
        self.btn_rbz.setText(_translate("Dialog", "MOTORZ", None))
        self.btn_rbx.setToolTip(_translate("Dialog", "Calibrate Motor Position", None))
        self.btn_rbx.setText(_translate("Dialog", "MOTORX", None))
        self.label.setText(_translate("Dialog", "Calibrate Motor positions (Sardana+Tango).", None))
        self.dsb_rbz.setToolTip(_translate("Dialog", "Motor Position to be set as current", None))
        self.btn_rby.setToolTip(_translate("Dialog", "Calibrate Motor Position", None))
        self.btn_rby.setText(_translate("Dialog", "MOTORY", None))
        self.btn_rbx_zero.setToolTip(_translate("Dialog", "Calibrate Motor Position to 0", None))
        self.btn_rbx_zero.setText(_translate("Dialog", "0", None))
        self.btn_rby_zero.setToolTip(_translate("Dialog", "Calibrate Motor Position to 0", None))
        self.btn_rby_zero.setText(_translate("Dialog", "0", None))
        self.btn_rbz_zero.setToolTip(_translate("Dialog", "Calibrate Motor Position to 0", None))
        self.btn_rbz_zero.setText(_translate("Dialog", "0", None))

