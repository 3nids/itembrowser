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
from ui_settings import Ui_Settings

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

# create the dialog to connect layers
class settings(QDialog, Ui_Settings ):
	def __init__(self,iface):
		self.iface = iface
		QDialog.__init__(self)
		# Set up the user interface from Designer.
		self.setupUi(self)
		QObject.connect(self , SIGNAL( "accepted()" ) , self.applySettings)
		# load settings
		self.settings = QSettings("ItemBrowser","ItemBrowser")
		
		self.saveSelectionBox.setChecked( self.settings.value("saveSelectionInProject",  1).toInt()[0] )
		self.scaleSpin.setValue(  self.settings.value("scale",5).toInt()[0])
		self.rubberWidth.setValue(self.settings.value("rubber_width",2).toDouble()[0])
		self.colorR = self.settings.value("rubber_colorR",255).toInt()[0]
		self.colorG = self.settings.value("rubber_colorG",0  ).toInt()[0]
		self.colorB = self.settings.value("rubber_colorB",0  ).toInt()[0]
		self.color  = QColor(self.colorR,self.colorG,self.colorB,255)
		self.applyColorStyle()

	def applySettings(self):
		self.settings.setValue( "saveSelectionInProject" , int(self.saveSelectionBox.isChecked()) )
		self.settings.setValue( "scale" , self.scaleSpin.value() )
		self.settings.setValue( "rubber_width"   , self.rubberWidth.value() )	
		self.settings.setValue( "rubber_colorR"  , self.color.red() )
		self.settings.setValue( "rubber_colorG"  , self.color.green() )
		self.settings.setValue( "rubber_colorB"  , self.color.blue() )

	@pyqtSignature("on_rubberColor_clicked()")
	def on_rubberColor_clicked(self):
		self.color = QColorDialog.getColor(self.color)
		self.applyColorStyle()
		
	def applyColorStyle(self):
		self.rubberColor.setStyleSheet("background-color: rgb(%u,%u,%u)" % (self.color.red(),self.color.green(),self.color.blue()))	
