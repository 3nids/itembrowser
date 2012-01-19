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

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class itemBrowser():
	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		self.layers = {}
		
	def initGui(self):
		self.connectLayersDlg = connectLayers(self.iface)
		# CONNECTLAYERS
		self.connectLayerAction = QAction(QIcon(":/plugins/itembrowser/icons/connect.png"), "connect layers", self.iface.mainWindow())
		QObject.connect(self.connectLayerAction, SIGNAL("triggered()"), self.connectLayersDlg.exec_)
		QObject.connect(self.connectLayersDlg,   SIGNAL("accepted()"),  self.connect)
		self.iface.addToolBarIcon(self.connectLayerAction)
		self.iface.addPluginToMenu("&Item Browser", self.connectLayerAction)
		# run connection when plugin started
		self.connect()
				
	def unload(self):
		# Remove the plugin menu item and icon
		self.iface.removePluginMenu("&Item Browser",self.connectLayerAction)
		self.iface.removeToolBarIcon(self.connectLayerAction)
		
	def connect(self):
		for layer in self.iface.mapCanvas().layers():
			if layer.customProperty("itemBrowserConnected", "no").toString() == "yes":
				self.layers[layer.id()] = layerItemBrowser( self.iface , layer )
			elif self.layers.has_key(layer.id):
				QObject.disconnect(self.layer , SIGNAL("selectionChanged ()"), self.layers.get(layer.id()).selectionChanged )	

class layerItemBrowser( QDockWidget , Ui_itembrowser ):
	def __init__(self,iface,layer):
		self.iface = iface
		self.layer = layer
		# UI setup
		QDockWidget.__init__(self)
		self.setupUi(self)
		self.setWindowTitle(layer.name())
		self.iface.addDockWidget(Qt.LeftDockWidgetArea,self)
		self.setVisible(False)
		# Connect SIGNAL
		QObject.connect(self.layer , SIGNAL("selectionChanged ()"), self.selectionChanged )
		# create rubber band to emphasis the current selected item (over the whole selection)
		self.rubber = QgsRubberBand(self.iface.mapCanvas())
		# initial style for rubber band
		self.symbol = QgsLineSymbolV2()
		self.symbol.setColor( QColor(255,0,0,255) )
		self.symbol.setWidth( 1.3 )
		self.applySymbolStyle()
		
	def unload(self):
		self.iface.removeDockWidget(self)
		
	def selectionChanged(self):
		self.browseFrame.setEnabled(False)
		self.cleanBrowserFields()
		self.rubber.reset()
		nItems = self.layer.selectedFeatureCount()
		if nItems == 0:	return
		if nItems > 1:  self.setVisible(True)
		self.browseFrame.setEnabled(True)
		self.subset = self.layer.selectedFeaturesIds()
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
		bobo.scale(5)
		self.iface.mapCanvas().setExtent(bobo)
		self.iface.mapCanvas().refresh()	

	def getCurrentItem(self):
		i = self.listCombo.currentIndex()
		if i == -1: return False
		item = QgsFeature()
		self.layer.featureAtId(self.subset[i],item)
		return item	
		
	def applySymbolStyle(self):
		color = self.symbol.color()
		self.rubber.setColor(color)
		self.rubber.setWidth(self.symbol.width())
		self.colorButton.setStyleSheet("background-color: rgb(%u,%u,%u)" % (color.red(),color.green(),color.blue()))	

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
		if item is False:
			self.emit(SIGNAL("browserNoItem()"))
			return
		# update rubber band
		self.rubber.reset()
		self.rubber.addGeometry(item.geometry(),self.layer)
		# zoom to item
		if self.zoomCheck.isChecked():
			self.zoomToItem(item)
		# Update browser
		self.currentPosLabel.setText('%u/%u' % (i+1,len(self.subset)) )
		# emit signal
		self.emit(SIGNAL("browserCurrentItem(QgsVectorLayer,QgsFeatureId)"),self.layer,item.id())
		
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
			
	@pyqtSignature("on_colorButton_clicked()")
	def on_colorButton_clicked(self):
		if QgsSymbolV2PropertiesDialog(self.symbol,self.layer).exec_():
			self.applySymbolStyle()
