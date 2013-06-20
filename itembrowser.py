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

from PyQt4.QtCore import QUrl, Qt
from PyQt4.QtGui import QAction, QIcon, QDesktopServices
from qgis.core import QgsMapLayer

from core.mysettings import MySettings
from gui.mysettingsdialog import MySettingsDialog
from gui.itembrowserdock import ItemBrowserDock

import resources


class itemBrowser():
    def __init__(self, iface):
        self.iface = iface
        self.settings = MySettings()
        self.docks = {}

    def initGui(self):
        # browse action
        self.browserAction = QAction(QIcon(":/plugins/itembrowser/icons/itembrowser.png"),
                                     "Browse selected items of current layer", self.iface.mainWindow())
        self.browserAction.setEnabled(False)
        self.browserAction.triggered.connect(self.openBrowserDock)
        self.iface.addToolBarIcon(self.browserAction)
        self.iface.addPluginToMenu("&Item Browser", self.browserAction)
        # settings
        self.uisettingsAction = QAction("settings", self.iface.mainWindow())
        self.uisettingsAction.triggered.connect(self.showSettings)
        self.iface.addPluginToMenu("&Item Browser", self.uisettingsAction)     
        # help
        self.helpAction = QAction(QIcon(":/plugins/itembrowser/icons/help.png"), "Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(lambda: QDesktopServices().openUrl(QUrl("https://github.com/3nids/itembrowser/wiki")))
        self.iface.addPluginToMenu("&Item Browser", self.helpAction)

        self.iface.currentLayerChanged.connect(self.currentLayerChanged)
        self.iface.mapCanvas().selectionChanged.connect(self.currentLayerChanged)
        self.currentLayerChanged(self.iface.legendInterface().currentLayer())
              
    def unload(self):
        self.iface.removePluginMenu("&Item Browser", self.browserAction)
        self.iface.removePluginMenu("&Item Browser", self.uisettingsAction)
        self.iface.removePluginMenu("&Item Browser", self.helpAction)
        self.iface.removeToolBarIcon(self.browserAction)
        
    def currentLayerChanged(self, layer):
        enable = (layer is not None
                  and layer.type() == QgsMapLayer.VectorLayer
                  and layer.hasGeometryType()
                  and len(layer.selectedFeaturesIds()) > 1)
        self.browserAction.setEnabled(enable)

    def openBrowserDock(self):
        layer = self.iface.legendInterface().currentLayer()
        if layer.id() in self.docks:
            return
        dock = ItemBrowserDock(self.iface, layer)
        dock.dockRemoved.connect(self.dockRemoved)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.docks[layer.id()] = dock

    def dockRemoved(self, layerid):
        del self.docks[layerid]

    def showSettings(self):
        MySettingsDialog().exec_()




