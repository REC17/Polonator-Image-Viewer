import os, sys, math, numpy #,png, itertools
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class QuadView(QGraphicsItem):
    def __init__(self, mainWin, image, zero, alpha, view, channel, selectedbrowser, livebrowser):
        super(QuadView, self).__init__(parent = None)
        self.image = image
        self.channel = channel
        self.zero = zero
        self.alpha = alpha
        self.view = view
        self.livebrowser = livebrowser
        self.selectedbrowser = selectedbrowser
        self.rect = QRectF(0, 0, 1000, 1000)
        self.mainWin = mainWin
        self.COL = self.mainWin.compinstanceL
        self.COL.append(self)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setCursor(QCursor(Qt.CrossCursor))

    def hoverMoveEvent(self, event):
        
        x = int(event.pos().x())
        y = int(event.pos().y())
        pixloc = x + y*1000
        self.livebrowser.setText(QString("X..." + str(x) + "    Y..." + str(y) + "    Pixel Value..." + str(self.image[y, x])))
        
        
    def mousePressEvent(self, event):
        
        x = event.pos().x()
        y = event.pos().y()

        if self.mainWin.enableQuadMag == True:   
            for i in self.COL:
                i.matrixresize(x, y)
        self.selectedbrowser.append(QString(str(x) + "\t" + str(y) + "\t" + str(self.image[y, x])))
        
    def matrixresize(self, x, y):
        matrix = self.view.matrix()
        scale = 2.0        
        if matrix.m11() == 256:
            self.view.resetMatrix()
            scale = 0.5**9
        if self.mainWin.zoom == "-":
            if matrix.m11() == 0.5:
                scale = 1
            else:
                scale = 0.5
        matrix.scale(scale, scale)
        self.view.setMatrix(matrix)
        self.view.centerOn(x, y)
     #   limit = 256/matrix.m11()
      #  log = math.log(limit, 2)
       # adjustlim = 1000/(2**(9-log))
        #self.view.ensureVisible(x, y, adjustlim, adjustlim)

    def searchExecuted(self, x, y):
        self.channel.setText(QString(str(self.image[y, x]))) 

 #       self.searchbrowser.setText(QString("Pixel Value..." + str(self.image[y, x])))
    
    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
      #  painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
       # painter.fillRect(self.rect, Qt.transparent)
        image_ARGB_3D1 = numpy.dstack([self.image.astype(numpy.uint8), self.image.astype(numpy.uint8), self.image.astype(numpy.uint8), self.alpha])
        image_ARGB_2D1 = numpy.reshape(image_ARGB_3D1,(-1, 1000*4))
        Image1 = QImage(image_ARGB_2D1.data, 1000, 1000, QImage.Format_ARGB32)
        painter.drawImage(self.rect, Image1, self.rect)
    def paint(self, painter, option, widget=None):
      #  painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
       # painter.fillRect(self.rect, Qt.transparent)
        image_ARGB_3D1 = numpy.dstack([self.image.astype(numpy.uint8), self.image.astype(numpy.uint8), self.image.astype(numpy.uint8), self.alpha])
        image_ARGB_2D1 = numpy.reshape(image_ARGB_3D1,(-1, 1000*4))
        Image1 = QImage(image_ARGB_2D1.data, 1000, 1000, QImage.Format_ARGB32)
        painter.drawImage(self.rect, Image1, self.rect)

