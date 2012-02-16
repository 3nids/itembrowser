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

from ui_itembrowser import Ui_itembrowser
from connectlayers import connectLayers
from settings import settings

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
				
	def unload(self):
		# Remove the plugin menu item and icon
		self.iface.removePluginMenu("&Item Browser",self.connectLayerAction)
		self.iface.removePluginMenu("&Item Browser",self.uisettingsAction)
		self.iface.removeToolBarIcon(self.connectLayerAction)
		
	def connect(self):
		for layer in self.iface.legendInterface().layers():
			if layer.customProperty("itemBrowserConnected", "no").toString() == "yes":
				self.layers[layer.id()] = layerItemBrowser( self.iface , layer )
				if QSettings("ItemBrowser","ItemBrowser").value("saveSelectionInProject", 1 ).toInt()[0] == 1 and layer.selectedFeatureCount() == 0:
					exec("selection = %s" % layer.customProperty("itemBrowserSelection","[]").toString() )
					if len(selection)>0: 
						i = layer.customProperty("itemBrowserCurrentItem",0).toInt()[0]
						layer.setSelectedFeatures(selection)
						self.layers[layer.id()].listCombo.setCurrentIndex(i)
			elif self.layers.has_key(layer.id()): # if the layer is removed and was previously connected
				QObject.disconnect(layer , SIGNAL("selectionChanged ()"), self.layers.get(layer.id()).selectionChanged )
				self.layers.get(layer.id()).unload()
				self.layers.pop(layer.id())	
	

class layerItemBrowser( QDockWidget , Ui_itembrowser ):
	def __init__(self,iface,layer):
		self.iface = iface
		self.layer = layer
		self.settings = QSettings("ItemBrowser","ItemBrowser")
		# UI setup
		QDockWidget.__init__(self)
		self.setupUi(self)
		self.setWindowTitle(layer.name())
		if layer.hasGeometryType() is False:
			self.zoomCheck.setChecked(False)
			self.zoomCheck.setEnabled(False)
		self.iface.addDockWidget(Qt.LeftDockWidgetArea,self)
		self.setVisible(False)
		# Connect SIGNAL
		QObject.connect(self.layer , SIGNAL("selectionChanged ()"), self.selectionChanged )
		# create rubber band to emphasis the current selected item (over the whole selection)
		self.rubber = QgsRubberBand(self.iface.mapCanvas())
				
	def unload(self):
		self.iface.removeDockWidget(self)
		
	def selectionChanged(self):
		self.browseFrame.setEnabled(False)
		self.cleanBrowserFields()
		self.rubber.reset()
		nItems = self.layer.selectedFeatureCount()
		if nItems == 0:	
			if self.settings.value("saveSelectionInProject", 1 ).toInt()[0] == 1:
				self.layer.setCustomProperty("itemBrowserSelection",repr("[]"))
			self.setVisible(False)
			self.layer.emit(SIGNAL("browserNoItem()"))
			return
		if nItems > 0:  self.setVisible(True) # set to 1 ?
		self.browseFrame.setEnabled(True)
		self.subset = self.layer.selectedFeaturesIds()
		if self.settings.value("saveSelectionInProject", 1 ).toInt()[0] == 1:
			self.layer.setCustomProperty("itemBrowserSelection",repr(self.subset))
			self.layer.setCustomProperty("itemBrowserCurrentItem",0)
		l = 0
		for id in self.subset:
			self.listCombo.addItem(_fromUtf8(""))
			self.listCombo.setItemText(l, "%u" % id)
			l+= 1		

	def cleanBrowserFields(self):
		self.currentPosLabel.setText('0/0')
		self.listCombo.clear()
		
	def zoomToItem(self,item):
		bobo = item.geometry().boundingBox()
		bobo.scale( self.settings.value("scale",5).toInt()[0] )
		self.iface.mapCanvas().setExtent(bobo)
		self.iface.mapCanvas().refresh()	

	def getCurrentItem(self):
		i = self.listCombo.currentIndex()
		if i == -1: return False
		item = QgsFeature()
		self.layer.featureAtId(self.subset[i],item)
		return item	
		
	@pyqtSignature("on_previousButton_clicked()")
	def on_previousButton_clicked(self):
		i = self.listCombo.currentIndex()
		n = max(0,i-1)
		self.listCombo.setCurrentIndex(n)
		
	@pyqtSignature("on_nextButton_clicked()")
	def on_nextButton_clicked(self):
		i = self.listCombo.currentIndex()
		c = self.listCombo.count()
		n = min(i+1,c-1)
		self.listCombo.setCurrentIndex(n)

	@pyqtSignature("on_listCombo_currentIndexChanged(int)")
	def on_listCombo_currentIndexChanged(self,i):
		item = self.getCurrentItem()
		if item is False: return
		if self.settings.value("saveSelectionInProject", 1 ).toInt()[0] == 1:
			self.layer.setCustomProperty("itemBrowserCurrentItem",i)
		# update rubber band (only if more than 1 item is selected)
		self.rubber.reset()
		if self.listCombo.count() > 1:
			width = self.settings.value("rubber_width",2).toDouble()[0]
			colorR = self.settings.value("rubber_colorR",255).toInt()[0]
			colorG = self.settings.value("rubber_colorG",0  ).toInt()[0]
			colorB = self.settings.value("rubber_colorB",0  ).toInt()[0]
			color  = QColor(colorR,colorG,colorB,255)
			self.rubber.setColor(color)
			self.rubber.setWidth(width)
			self.rubber.addGeometry(item.geometry(),self.layer)
		# zoom to item
		if self.zoomCheck.isChecked():
			self.zoomToItem(item)
		# Update browser
		self.currentPosLabel.setText('%u/%u' % (i+1,len(self.subset)) )
		# emit signal
		self.layer.emit(SIGNAL("browserCurrentItem(int)"),item.id())
		
	@pyqtSignature("on_zoomCheck_stateChanged(int)")
	def on_zoomCheck_stateChanged(self,i):
		if self.zoomCheck.isChecked():
			# Extract item
			item = self.getCurrentItem()
			# zoom
			self.zoomToItem(item)

	@pyqtSignature("on_editFormButton_clicked()")
	def on_editFormButton_clicked(self):
		# launch edit form
		self.iface.openFeatureForm(self.layer, self.getCurrentItem() )
		
