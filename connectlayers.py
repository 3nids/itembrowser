#-----------------------------------------------------------
#
# Item Browser is a QGIS plugin which allows you to browse a multiple selection.
#
# Copyright    : (C) 2013 Denis Rouzaud
# Email        : denis.rouzaud@gmail.com
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this progsram; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4.QtGui import QDialog, QListWidgetItem
from ui.ui_connectlayers import Ui_connectlayers


class connectLayers(QDialog, Ui_connectlayers):
    def __init__(self, iface):
        self.iface = iface
        QDialog.__init__(self)
        self.setupUi(self)
        QObject.connect(self, SIGNAL("accepted()"), self.applySettings)
                    
    def showEvent(self, e):
        self.layerList.clear()
        self.layers = self.iface.legendInterface().layers()
        for layer in self.layers:
            item = QListWidgetItem()
            item.setText(layer.name())
            if layer.customProperty("itemBrowserConnected", "no") == "yes":
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.layerList.addItem(item)
                    
    def applySettings(self):
        for i, layer in zip(range(len(self.layers)), self.layers):
            if self.layerList.item(i).checkState() == 2:
                layer.setCustomProperty("itemBrowserConnected", "yes")
            else:
                layer.setCustomProperty("itemBrowserConnected", "no")
        QObject.emit(self, SIGNAL("layerListUpdated()"))
