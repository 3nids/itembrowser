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

from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QAction, QIcon, QDesktopServices

from core.mysettings import MySettings
from gui.mysettingsdialog import MySettingsDialog

from connectlayers import connectLayers
from layeritembrowser import LayerItemBrowser

import resources


class itemBrowser():
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.layers = {}
        self.settings = MySettings()
        # run connection when new layers are loaded
        self.iface.mapCanvas().layersChanged.connect(self.connect)
        
    def initGui(self):

        # CONNECTLAYERS
        self.connectLayerAction = QAction(QIcon(":/plugins/itembrowser/icons/connect.png"),
                                          "connect layers to item browser", self.iface.mainWindow())
        self.connectLayerAction.triggered.connect(self.connectLayersDialog)
        self.iface.addToolBarIcon(self.connectLayerAction)
        self.iface.addPluginToMenu("&Item Browser", self.connectLayerAction)
        # settings
        self.uisettingsAction = QAction("settings", self.iface.mainWindow())
        self.uisettingsAction.triggered.connect(self.showSettings)
        self.iface.addPluginToMenu("&Item Browser", self.uisettingsAction)     
        # help
        self.helpAction = QAction(QIcon(":/plugins/itembrowser/icons/help.png"), "Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(lambda: QDesktopServices().openUrl(QUrl("https://github.com/3nids/itembrowser/wiki")))
        self.iface.addPluginToMenu("&Item Browser", self.helpAction)
              
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&Item Browser", self.connectLayerAction)
        self.iface.removePluginMenu("&Item Browser", self.uisettingsAction)
        self.iface.removePluginMenu("&Item Browser", self.helpAction)
        self.iface.removeToolBarIcon(self.connectLayerAction)
        
    def connect(self):
        for layer in self.iface.legendInterface().layers():
            if layer.customProperty("itemBrowserConnected", "no") == "yes":
                if layer.id() in self.layers:
                    continue
                self.layers[layer.id()] = LayerItemBrowser(self.iface, layer)
                self.layers[layer.id()].layerDeleted.connect(self.disconnectLayer)
                if self.settings.value("saveSelectionInProject") and layer.selectedFeatureCount() == 0:
                    exec("selection = %s" % layer.customProperty("itemBrowserSelection", "[]"))
                    if len(selection) > 0:
                        i = layer.customProperty("itemBrowserCurrentItem", 0).toInt()[0]
                        layer.setSelectedFeatures(selection)
                        self.layers[layer.id()].listCombo.setCurrentIndex(i)
                self.layers[layer.id()].selectionChanged()
            elif self.layers.has_key(layer.id()):
                # if the layer is disconnected but was previously connected
                layer.selectionChanged.disconnect(self.layers.get(layer.id()).selectionChanged)
                self.layers[layer.id()].unload()
                self.disconnectLayer(layer)
              
    def disconnectLayer(self, layer):
        self.layers.pop(layer.id())

    def showSettings(self):
        MySettingsDialog().exec_()

    def connectLayersDialog(self):
        dlg = connectLayers(self.iface)
        if dlg.exec_():
            self.connect()


