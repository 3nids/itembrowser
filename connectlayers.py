"""
Item Browser
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Jan. 2012
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_connectlayers import Ui_connectlayers

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

# create the dialog to connect layers
class connectLayers(QDialog, Ui_connectlayers ):
	def __init__(self,iface):
		self.iface = iface
		QDialog.__init__(self)
		self.setupUi(self)
		QObject.connect(self , SIGNAL( "accepted()" ) , self.applySettings)
				
	def showEvent(self, e):
		self.layerList.clear()
		self.layers = self.iface.mapCanvas().layers()
		for layer in self.layers:
			item = QListWidgetItem()
			item.setText(layer.name())
			if layer.customProperty("itemBrowserConnected", "no").toString() == "yes":
				item.setCheckState(Qt.Checked)
			else:
				item.setCheckState(Qt.Unchecked)
			self.layerList.addItem(item)
				
	def applySettings(self):
		for i,layer in zip(range(len(self.layers)) , self.layers):
			if self.layerList.item(i).checkState() == 2:
				layer.setCustomProperty("itemBrowserConnected", "yes")
			else:
				layer.setCustomProperty("itemBrowserConnected", "no")
		QObject.emit(self , SIGNAL("layerListUpdated()") )
