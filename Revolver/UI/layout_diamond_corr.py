# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout_diamond_corr.ui'
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
        Form.resize(624, 78)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)
        self.le_sample = QtGui.QLineEdit(Form)
        self.le_sample.setMinimumSize(QtCore.QSize(0, 25))
        self.le_sample.setMaximumSize(QtCore.QSize(150, 16777215))
        self.le_sample.setReadOnly(True)
        self.le_sample.setObjectName(_fromUtf8("le_sample"))
        self.gridLayout.addWidget(self.le_sample, 0, 4, 1, 1)
        self.le_diamond = QtGui.QLineEdit(Form)
        self.le_diamond.setMinimumSize(QtCore.QSize(0, 25))
        self.le_diamond.setMaximumSize(QtCore.QSize(150, 16777215))
        self.le_diamond.setReadOnly(True)
        self.le_diamond.setObjectName(_fromUtf8("le_diamond"))
        self.gridLayout.addWidget(self.le_diamond, 1, 4, 1, 1)
        self.btn_tip = QtGui.QPushButton(Form)
        self.btn_tip.setMinimumSize(QtCore.QSize(0, 25))
        self.btn_tip.setStyleSheet(_fromUtf8("QPushButton {padding-left: 10px; padding-right: 10px;}"))
        self.btn_tip.setObjectName(_fromUtf8("btn_tip"))
        self.gridLayout.addWidget(self.btn_tip, 0, 0, 1, 1)
        self.dsb_dtip = QtGui.QDoubleSpinBox(Form)
        self.dsb_dtip.setMinimumSize(QtCore.QSize(100, 25))
        self.dsb_dtip.setAlignment(QtCore.Qt.AlignCenter)
        self.dsb_dtip.setDecimals(4)
        self.dsb_dtip.setMinimum(-100.0)
        self.dsb_dtip.setMaximum(100.0)
        self.dsb_dtip.setSingleStep(0.01)
        self.dsb_dtip.setObjectName(_fromUtf8("dsb_dtip"))
        self.gridLayout.addWidget(self.dsb_dtip, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setMaximumSize(QtCore.QSize(20, 25))
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setMaximumSize(QtCore.QSize(20, 25))
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.btn_bsurface = QtGui.QPushButton(Form)
        self.btn_bsurface.setMinimumSize(QtCore.QSize(0, 25))
        self.btn_bsurface.setStyleSheet(_fromUtf8("QPushButton {padding-left: 10px; padding-right: 10px;}"))
        self.btn_bsurface.setObjectName(_fromUtf8("btn_bsurface"))
        self.gridLayout.addWidget(self.btn_bsurface, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)
        self.btn_sample = QtGui.QPushButton(Form)
        self.btn_sample.setMinimumSize(QtCore.QSize(0, 60))
        self.btn_sample.setStyleSheet(_fromUtf8("QPushButton {padding-left: 10px; padding-right: 10px;}"))
        self.btn_sample.setObjectName(_fromUtf8("btn_sample"))
        self.gridLayout.addWidget(self.btn_sample, 0, 5, 2, 1)
        self.dsb_bsurface = QtGui.QDoubleSpinBox(Form)
        self.dsb_bsurface.setMinimumSize(QtCore.QSize(100, 25))
        self.dsb_bsurface.setAlignment(QtCore.Qt.AlignCenter)
        self.dsb_bsurface.setDecimals(4)
        self.dsb_bsurface.setMinimum(-100.0)
        self.dsb_bsurface.setMaximum(100.0)
        self.dsb_bsurface.setSingleStep(0.01)
        self.dsb_bsurface.setObjectName(_fromUtf8("dsb_bsurface"))
        self.gridLayout.addWidget(self.dsb_bsurface, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.btn_tip, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.actionDiamondTip)
        QtCore.QObject.connect(self.btn_bsurface, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.actionDiamondBSurface)
        QtCore.QObject.connect(self.btn_sample, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.actionMoveToSample)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.btn_tip, self.btn_bsurface)
        Form.setTabOrder(self.btn_bsurface, self.le_sample)
        Form.setTabOrder(self.le_sample, self.le_diamond)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Sample Position:", None))
        self.le_sample.setToolTip(_translate("Form", "Real sample position after diamond correction", None))
        self.le_diamond.setToolTip(_translate("Form", "Diamond thickness", None))
        self.btn_tip.setToolTip(_translate("Form", "Get position with focused sample (virtual sample position)", None))
        self.btn_tip.setText(_translate("Form", "1. Diamond Tip >>", None))
        self.dsb_dtip.setToolTip(_translate("Form", "Focused sample position (virtual sample position)", None))
        self.btn_bsurface.setToolTip(_translate("Form", "Get position with focused diamond back surface", None))
        self.btn_bsurface.setText(_translate("Form", "2. Diamond B.Surface >>", None))
        self.label_2.setText(_translate("Form", "Diamond Thickness:", None))
        self.btn_sample.setToolTip(_translate("Form", "Move to real sample position (after diamond correction)", None))
        self.btn_sample.setText(_translate("Form", "3. Move To Real\n"
" Sample Position", None))
        self.dsb_bsurface.setToolTip(_translate("Form", "Focused diamond back surface position", None))

