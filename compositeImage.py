import os, sys, math, numpy #,png, itertools
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class CompImage(QGraphicsItem):
    def __init__(self, mainWin, target, Image, source, selectedbrowser, livebrowser, searchbrowser, image_8bit, parent=None):
        super(CompImage, self).__init__(parent)
        self.target = target
        self.mainWin = mainWin
        self.Image = Image
        self.source = source
        self.searchbrowser = searchbrowser
        self.rawimage = image_8bit
        self.selectedbrowser = selectedbrowser
        self.livebrowser = livebrowser
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setCursor(QCursor(Qt.CrossCursor))
        
    def hoverMoveEvent(self, event):
        x = int(event.pos().x())
        y = int(event.pos().y())
        pixloc = x + y*1000
        self.livebrowser.setText(QString("X..." + str(x) + "    Y..." + str(y) + "    Pixel Value..." + str(self.rawimage[y, x])))
        
        for i in range(3):
            for j in range(3):
                pass
          #      print self.rawimage[y + i-1, x + j-1].astype(numpy.uint8)
            
    
    def searchExecuted(self, x, y):
        self.searchbrowser.setText(QString("Pixel Value..." + str(self.rawimage[y, x])))
        
    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()      
        self.selectedbrowser.append(QString(str(x) + "\t" + str(y) + "\t" + str(self.rawimage[y, x])))

        if self.mainWin.dotpermission == True:
            cm = CircleMarker(self.mainWin, QPointF(x, y), self)
            cm.setParentItem(self)
        
    def boundingRect(self):
        return self.source

    def paint(self, painter, option, widget=None):
        painter.drawImage(self.target, self.Image, self.source)
        painter.drawRect(self.target)



class CircleMarker(QGraphicsItem):
    def __init__(self, mainWin, position, futureparent):
        super(CircleMarker, self).__init__()
        self.mainWin = mainWin
        self.futureparent = futureparent
        self.fill = QColor(100, 204, 150)
        self.stroke = QColor(153, 204, 255)
        self.setPos(position)
        self.mainWin.ClearDots.setEnabled(True)
        
        
        if len(self.mainWin.lastcircle) > 0:
            DL = DistanceLine(self.mainWin, self.mainWin.lastcircle[0], self.mainWin.lastcircle[1], position.x(), position.y())
            DL.setParentItem(self.futureparent)        
        
        self.futureparent.update()
        self.mainWin.lastcircle = []
        self.mainWin.lastcircle.append(position.x())
        self.mainWin.lastcircle.append(position.y())
        
    def boundingRect(self):
        return QRectF(-6,-6,12,12)
    
    def paint(self, painter, option, widget=None):
    #    painter.setBrush(QBrush(self.fill))
        painter.setPen(QPen(self.stroke))
        painter.drawEllipse(QRectF(-5, -5, 10, 10))
        painter.drawEllipse(QRectF(-6,-6,12,12))

class DistanceLine(QGraphicsItem):
    def __init__(self, mainWin, x1, y1, x2, y2):
        super(DistanceLine, self).__init__()
        self.mainWin = mainWin
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        
        self.stroke = QColor(255, 204, 153)
        self.rect = QRectF(0,0,100,100)


        if self.mainWin.lastline is not None:
            try:
                LLS = self.mainWin.lastline.scene()
                LLS.removeItem(self.mainWin.lastline)
            except:
                return
        self.mainWin.lastline = self

    def boundingRect(self):
        return self.rect
    
    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(self.stroke))
        for i in range(9):
            x = (i+1)%3 -1
            y = (i+1)/3 -1
            line = QLine(self.x2 + x , self.y2 + y, self.x1 + x, self.y1 + y)
            painter.drawLine(line)
