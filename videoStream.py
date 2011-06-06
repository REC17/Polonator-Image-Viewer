import os, sys, math, numpy #,png, itertools
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon as phonon


"""
class VideoStream(QGraphicsItem):
    def __init__(self, Image, count, parent=None):
        super(VideoStream, self).__init__(parent)
        self.count = count
        self.pic = Image
        self.source = QRectF(0, 0, 1000, 1000)

    def boundingRect(self):
        return self.source

    def paint(self, painter, option, widget=None):

        shape = (1000, 1000)
        
        alpha_array = 255*(numpy.ones(shape, dtype=numpy.uint8))        
        Red = 0*alpha_array
        Green = 0*alpha_array
        Blue = 0*alpha_array
        if self.count%3 == 1:
            Green = self.pic
        elif self.count%3 == 2: 
            Blue = self.pic
        elif self.count%3 == 0:
            Red = self.pic 
        width = 1000
        
        image_ARGB_3D = numpy.dstack([Blue, Red, Green, alpha_array])
        image_ARGB_2D = numpy.reshape(image_ARGB_3D,(-1,width*4))

        ImageQ = QImage(image_ARGB_2D.data, 1000, 1000, QImage.Format_ARGB32)
        painter.drawImage(self.source, ImageQ, self.source)        
"""
