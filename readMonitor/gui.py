# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

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
        Dialog.resize(619, 468)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.hSlider = QtGui.QSlider(Dialog)
        self.hSlider.setMinimum(1)
        self.hSlider.setMaximum(1000)
        self.hSlider.setOrientation(QtCore.Qt.Horizontal)
        self.hSlider.setInvertedControls(False)
        self.hSlider.setObjectName(_fromUtf8("hSlider"))
        self.gridLayout.addWidget(self.hSlider, 1, 0, 1, 1)
        self.view = QtGui.QGraphicsView(Dialog)
        self.view.setObjectName(_fromUtf8("view"))
        self.gridLayout.addWidget(self.view, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
