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
				self.layers[layer.id()] = layerItemBrowser( self.iface , layer )
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

class layerItemBrowser( QDockWidget , Ui_itembrowser ):
	def __init__(self,iface,layer):
		self.iface = iface
		self.layer = layer
		self.renderer = self.iface.mapCanvas().mapRenderer()
		self.settings = QSettings("ItemBrowser","ItemBrowser")
		# UI setup
		QDockWidget.__init__(self)
		self.setupUi(self)
		self.setWindowTitle("ItemBrowser: %s" % layer.name())
		if layer.hasGeometryType() is False:
			self.panCheck.setChecked(False)
			self.panCheck.setEnabled(False)
			self.scaleCheck.setChecked(False)
			self.scaleCheck.setEnabled(False)
		self.iface.addDockWidget(Qt.LeftDockWidgetArea,self)
		self.browseFrame.setEnabled(False)
		self.setVisible(False)
		# Connect SIGNAL
		QObject.connect(self.layer , SIGNAL("selectionChanged ()"), self.selectionChanged )
		QObject.connect(self.layer , SIGNAL("layerDeleted()") , self.unload )
		QObject.connect(self.layer , SIGNAL("layerDeleted()") , self.emitLayerDeleted )
		# create rubber band to emphasis the current selected feature (over the whole selection)
		self.rubber = QgsRubberBand(self.iface.mapCanvas())
		
	def emitLayerDeleted(self):
		self.emit(SIGNAL("layerDeleted(QgsMapLayer)"),self.layer)
				
	def unload(self):
		self.rubber.reset()
		self.iface.removeDockWidget(self)	
		
	def selectionChanged(self):
		self.browseFrame.setEnabled(False)
		self.cleanBrowserFields()
		self.rubber.reset()
		nItems = self.layer.selectedFeatureCount()
		if nItems == 0:	
			if self.settings.value("saveSelectionInProject", 1 ).toInt()[0] == 1:
				self.layer.setCustomProperty("itemBrowserSelection",repr([]))
			self.setVisible(False)
			self.layer.emit(SIGNAL("browserNoItem()"))
			return
		if nItems > 0:  self.setVisible(True) # set to 1 ?
		self.browseFrame.setEnabled(True)
		self.subset = self.layer.selectedFeaturesIds()
		if self.settings.value("saveSelectionInProject", 1 ).toInt()[0] == 1:
			self.layer.setCustomProperty("itemBrowserSelection",repr(self.subset))
		l = 0
		for id in self.subset:
			self.listCombo.addItem(_fromUtf8(""))
			self.listCombo.setItemText(l, "%u" % id)
			l+= 1
		self.on_listCombo_currentIndexChanged(0)		

	def cleanBrowserFields(self):
		self.currentPosLabel.setText('0/0')
		self.listCombo.clear()
		
	def panScaleToItem(self,feature):
		if self.panCheck.isChecked() is False: return
		featBobo = feature.geometry().boundingBox()
		# if scaling and bobo has width and height (i.e. not a point)
		if self.scaleCheck.isChecked() and featBobo.width() != 0 and featBobo.height() != 0:
			featBobo.scale( self.settings.value("scale",5).toInt()[0] )
			ul = self.renderer.layerToMapCoordinates( self.layer, QgsPoint( featBobo.xMinimum() , featBobo.yMaximum() ) )
			ur = self.renderer.layerToMapCoordinates( self.layer, QgsPoint( featBobo.xMaximum() , featBobo.yMaximum() ) )
			ll = self.renderer.layerToMapCoordinates( self.layer, QgsPoint( featBobo.xMinimum() , featBobo.yMinimum() ) )
			lr = self.renderer.layerToMapCoordinates( self.layer, QgsPoint( featBobo.xMaximum() , featBobo.yMinimum() ) )
			x = ( ul.x() , ur.x() , ll.x() , lr.x() )
			y = ( ul.y() , ur.y() , ll.y() , lr.y() )
			x0 = min(x)
			y0 = min(y)
			x1 = max(x)
			y1 = max(y)
		else:
			panTo = self.renderer.layerToMapCoordinates( self.layer, featBobo.center() )
			mapBobo  = self.iface.mapCanvas().extent()
			xshift = panTo.x() - mapBobo.center().x()
			yshift = panTo.y() - mapBobo.center().y()
			x0 = mapBobo.xMinimum() + xshift
			y0 = mapBobo.yMinimum() + yshift
			x1 = mapBobo.xMaximum() + xshift
			y1 = mapBobo.yMaximum() + yshift
		self.iface.mapCanvas().setExtent( QgsRectangle(x0,y0,x1,y1) )
		self.iface.mapCanvas().refresh()	

	def getCurrentItem(self):
		i = self.listCombo.currentIndex()
		if i == -1: return False
		feature = QgsFeature()
		self.layer.featureAtId(self.subset[i],feature)
		return feature	
		
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
		feature = self.getCurrentItem()
		if feature is False: return
		if self.settings.value("saveSelectionInProject", 1 ).toInt()[0] == 1:
			self.layer.setCustomProperty("itemBrowserCurrentItem",i)
		# update rubber band (only if more than 1 feature is selected)
		self.rubber.reset()
		if self.listCombo.count() > 1:
			width = self.settings.value("rubber_width",2).toDouble()[0]
			colorR = self.settings.value("rubber_colorR",255).toInt()[0]
			colorG = self.settings.value("rubber_colorG",0  ).toInt()[0]
			colorB = self.settings.value("rubber_colorB",0  ).toInt()[0]
			color  = QColor(colorR,colorG,colorB,255)
			self.rubber.setColor(color)
			self.rubber.setWidth(width)
			self.rubber.addGeometry(feature.geometry(),self.layer)
		# scale to feature
		self.panScaleToItem(feature)
		# Update browser
		self.currentPosLabel.setText('%u/%u' % (i+1,len(self.subset)) )
		# emit signal
		self.layer.emit(SIGNAL("browserCurrentItem(int)"),feature.id())
		
	@pyqtSignature("on_panCheck_stateChanged(int)")
	def on_panCheck_stateChanged(self,i):
		if self.panCheck.isChecked():
			self.scaleCheck.setEnabled(True)
			# Extract feature
			feature = self.getCurrentItem()
			if feature is False: return
			# scale
			self.panScaleToItem(feature)
		else:
			self.scaleCheck.setEnabled(False)
			
	@pyqtSignature("on_scaleCheck_stateChanged(int)")
	def on_scaleCheck_stateChanged(self,i):
		if self.scaleCheck.isChecked():
			# Extract feature
			feature = self.getCurrentItem()
			if feature is False: return
			# scale
			self.panScaleToItem(feature)

	@pyqtSignature("on_editFormButton_clicked()")
	def on_editFormButton_clicked(self):
		# launch edit form
		self.iface.openFeatureForm(self.layer, self.getCurrentItem() )
		
