from PyQt4.QtCore import *
from PyQt4.QtGui import *

class VidImage(QGraphicsItem):
    def __init__(self, target, Image, source, parent=None):
        super(VidImage, self).__init__(parent)
        self.target = target
        self.Image = Image
        self.source = source
        
    def boundingRect(self):
        return self.source

    def paint(self, painter, option, widget=None):  
        painter.drawRect(self.target)
        painter.drawImage(self.target, self.Image, self.source)

