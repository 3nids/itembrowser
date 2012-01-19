# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_connectlayers.ui'
#
# Created: Thu Jan 19 14:51:08 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_connectlayers(object):
    def setupUi(self, connectlayers):
        connectlayers.setObjectName(_fromUtf8("connectlayers"))
        connectlayers.resize(261, 430)
        connectlayers.setWindowTitle(QtGui.QApplication.translate("connectlayers", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(connectlayers)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.layerList = QtGui.QListWidget(connectlayers)
        self.layerList.setObjectName(_fromUtf8("layerList"))
        self.gridLayout.addWidget(self.layerList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(connectlayers)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(connectlayers)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), connectlayers.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), connectlayers.reject)
        QtCore.QMetaObject.connectSlotsByName(connectlayers)

    def retranslateUi(self, connectlayers):
        pass

