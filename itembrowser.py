"""
Item Browser
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Jan. 2012
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import resources

from connectlayers import connectLayers
from settings import settings
from layeritembrowser import LayerItemBrowser

class itemBrowser():
	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		self.layers = {}
		# run connection when new layers are loaded
		QObject.connect(self.iface.mapCanvas() , SIGNAL("layersChanged ()") , self.connect ) 
		
	def initGui(self):
		self.connectLayersDlg = connectLayers(self.iface)
		# CONNECTLAYERS
		self.connectLayerAction = QAction(QIcon(":/plugins/itembrowser/icons/connect.png"), "connect layers to item browser", self.iface.mainWindow())
		QObject.connect(self.connectLayerAction, SIGNAL("triggered()")       , self.connectLayersDlg.exec_)
		QObject.connect(self.connectLayersDlg,   SIGNAL("layerListUpdated()"), self.connect)
		self.iface.addToolBarIcon(self.connectLayerAction)
		self.iface.addPluginToMenu("&Item Browser", self.connectLayerAction)
		# settings
		self.uisettings = settings(self.iface)
		self.uisettingsAction = QAction("settings", self.iface.mainWindow())
		QObject.connect(self.uisettingsAction, SIGNAL("triggered()"), self.uisettings.exec_)
		self.iface.addPluginToMenu("&Item Browser", self.uisettingsAction)	
		# help
		self.helpAction = QAction(QIcon(":/plugins/itembrowser/icons/help.png"), "Help", self.iface.mainWindow())
		QObject.connect(self.helpAction, SIGNAL("triggered()"), lambda: QDesktopServices.openUrl(QUrl("https://github.com/3nids/itembrowser/wiki")))
		self.iface.addPluginToMenu("&Item Browser", self.helpAction)
				
	def unload(self):
		# Remove the plugin menu item and icon
		self.iface.removePluginMenu("&Item Browser",self.connectLayerAction)
		self.iface.removePluginMenu("&Item Browser",self.uisettingsAction)
		self.iface.removePluginMenu("&Item Browser",self.helpAction)
		self.iface.removeToolBarIcon(self.connectLayerAction)
		
	def connect(self):
		for layer in self.iface.legendInterface().layers():
			if layer.customProperty("itemBrowserConnected", "no").toString() == "yes":
				if self.layers.has_key(layer.id()):	continue
				self.layers[layer.id()] = LayerItemBrowser( self.iface , layer )
				QObject.connect(self.layers[layer.id()],SIGNAL("layerDeleted(QgsMapLayer)"),self.disconnectLayer)
				if QSettings("ItemBrowser","ItemBrowser").value("saveSelectionInProject", 1 ).toInt()[0] == 1 and layer.selectedFeatureCount() == 0:
					exec("selection = %s" % layer.customProperty("itemBrowserSelection","[]").toString() )
					if len(selection)>0: 
						i = layer.customProperty("itemBrowserCurrentItem",0).toInt()[0]
						layer.setSelectedFeatures(selection)
						self.layers[layer.id()].listCombo.setCurrentIndex(i)
				self.layers[layer.id()].selectionChanged()
			elif self.layers.has_key(layer.id()): 
				# if the layer is disconnected but was previously connected
				QObject.disconnect(layer , SIGNAL("selectionChanged ()"), self.layers.get(layer.id()).selectionChanged )
				self.layers[layer.id()].unload()
				self.disconnectLayer(layer)
				
	def disconnectLayer(self,layer):
		self.layers.pop(layer.id())	


