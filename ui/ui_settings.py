# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_settings.ui'
#
# Created: Thu Jul 11 08:13:37 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName(_fromUtf8("Settings"))
        Settings.resize(292, 201)
        self.gridLayout = QtGui.QGridLayout(Settings)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(Settings)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label = QtGui.QLabel(Settings)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.saveSelectionInProject = QtGui.QCheckBox(Settings)
        self.saveSelectionInProject.setChecked(True)
        self.saveSelectionInProject.setObjectName(_fromUtf8("saveSelectionInProject"))
        self.gridLayout.addWidget(self.saveSelectionInProject, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.rubberWidth = QtGui.QDoubleSpinBox(Settings)
        self.rubberWidth.setToolTip(_fromUtf8(""))
        self.rubberWidth.setDecimals(1)
        self.rubberWidth.setSingleStep(1.0)
        self.rubberWidth.setProperty("value", 2.0)
        self.rubberWidth.setObjectName(_fromUtf8("rubberWidth"))
        self.gridLayout.addWidget(self.rubberWidth, 3, 1, 1, 1)
        self.scale = QtGui.QSpinBox(Settings)
        self.scale.setMinimum(1)
        self.scale.setMaximum(15)
        self.scale.setProperty("value", 5)
        self.scale.setObjectName(_fromUtf8("scale"))
        self.gridLayout.addWidget(self.scale, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Settings)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)
        self.rubberColor = QtGui.QLabel(Settings)
        self.rubberColor.setText(_fromUtf8(""))
        self.rubberColor.setObjectName(_fromUtf8("rubberColor"))
        self.gridLayout.addWidget(self.rubberColor, 4, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Settings)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.dockArea = QtGui.QComboBox(Settings)
        self.dockArea.setObjectName(_fromUtf8("dockArea"))
        self.dockArea.addItem(_fromUtf8(""))
        self.dockArea.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.dockArea, 0, 1, 1, 1)

        self.retranslateUi(Settings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Settings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QtGui.QApplication.translate("Settings", "Triangulation :: settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Settings", "Rubberband size", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Settings", "Rubberband color", None, QtGui.QApplication.UnicodeUTF8))
        self.saveSelectionInProject.setText(QtGui.QApplication.translate("Settings", "save selection in project", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Settings", "Scaling", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Settings", "Dock area", None, QtGui.QApplication.UnicodeUTF8))
        self.dockArea.setItemText(0, QtGui.QApplication.translate("Settings", "left", None, QtGui.QApplication.UnicodeUTF8))
        self.dockArea.setItemText(1, QtGui.QApplication.translate("Settings", "right", None, QtGui.QApplication.UnicodeUTF8))

