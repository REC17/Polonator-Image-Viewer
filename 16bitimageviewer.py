# The MIT License
# 
# Copyright (c) 2010 Wyss Institute
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 
# http://www.opensource.org/licenses/mit-license.php

"""
16bitimageviewer.py

Created by Roger Conturie and Nick Conway on 2010-10-09.
"""

import os
import sys
import math
import numpy
import time
import v4l2capture
import select
import getpass
import ui_16bitimagewindow #,png, itertools
from rectItem import RectangleSection
from customqgraphicsview import CustomQGraphicsView
from PIL import Image
from compositeImage import CompImage
from preferenceDialog import PreferenceDialog
from quadView import QuadView
from vidImage import VidImage
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import ConfigParser

"""
GLTICH: Enabling GTK threads causes the program to crash when opening files
"""

class STBimageviewer(QMainWindow, ui_16bitimagewindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(STBimageviewer, self).__init__(parent)
        self.setupUi(self)
        self.currentDir = os.getcwd()
        self.cParser = ConfigParser.ConfigParser()
        try:
            os.mkdir(self.currentDir+"/.config")
            file(self.currentDir+"/.config/.polImgPro.cfg", 'w')
            self.cParser.add_section('PREFIMGPATHS')
            self.cParser.set('PREFIMGPATHS','Path1','None')
            self.cParser.set('PREFIMGPATHS','Path2','None')
            self.cParser.set('PREFIMGPATHS','Path3','None')
            self.cParser.set('PREFIMGPATHS','Path4','None')
            with open(self.currentDir+"/.config/.polImgPro.cfg", 'w') as \
                configFile:
                self.cParser.write(configFile)
        except:
            pass

        self.view = self.graphicsView
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.comboBox = self.comboBox
        
        self.compositeview1 = self.graphicsView_2
        self.compositescene1 = QGraphicsScene()
        self.compositeview1.setScene(self.compositescene1)

        self.compositeview2 = self.graphicsView_3
        self.compositescene2 = QGraphicsScene()
        self.compositeview2.setScene(self.compositescene2)

        self.compositeview3 = self.graphicsView_4
        self.compositescene3 = QGraphicsScene()
        self.compositeview3.setScene(self.compositescene3)

        self.compositeview4 = self.graphicsView_5
        self.compositescene4 = QGraphicsScene()
        self.compositeview4.setScene(self.compositescene4)

        
        self.lastcircle = []
        self.lastline = None
        self.compinstanceL = []
        self.zoom = "+"
        self.enableQuadMag = False
        self.process = None
        self.videoview = self.VideoStreamWindow
        self.videoscene = QGraphicsScene()
        self.videoscene.setSceneRect(QRectF(0, 0, 960, 768))
        
        Rectangle = RectangleSection(QPointF(0,0))
        self.videoscene.addItem(Rectangle)

        self.videoview.setScene(self.videoscene)
        self.count = 0
        self.path = QDir.homePath()
        self.connect(self.actionOpen, SIGNAL("triggered()"), self.OpenClicked)


        self.selectedbrowser = self.SelectedTextBrowser
        self.livebrowser = self.LivetextBrowser

        self.pic = None
        
        self.C1Def = self.C1Def
        self.C2Def = self.C2Def
        self.C3Def = self.C3Def
        self.C4Def = self.C4Def
        self.path1 = None
        self.path2 = None
        self.path3 = None
        self.path4 = None

        self.Image = None
        self.dotpermission = False

        self.connect(self.comboBox, SIGNAL( "currentIndexChanged(int)" )\
                        , self.comboChange)
        self.actionPreferences.triggered.connect(self.preferencesTriggered)


        self.size_x = 0
        self.size_y = 0
        self.video = None
        self.devImg = None
        self.dispGI = None
        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"), self.updateVideo)

        self.rs = None
        self.videoview.mousePressEvent = self.videoViewPress
        self.videoview.mouseReleaseEvent = self.videoViewRelease
        self.videoview.mouseMoveEvent = self.videoViewMove



   #     self.videoview.translate(0, 0)
   #     self.videoview.update()





    def videoViewPress(self, event):
        x, y = event.pos().x(), event.pos().y()
        mapScene =  self.videoview.mapToScene(x, y)
        x, y, = mapScene.x(), mapScene.y()

        position = QPointF(x, y)
        self.rs = RectangleSection(position)
  #      self.rs.setPos(position)
        self.videoscene.addItem(self.rs)


    def videoViewRelease(self, event):
        self.videoscene.removeItem(self.rs)
        x = self.rs.position.x()
        y = self.rs.position.y()
        width = self.rs.width
        height = self.rs.height

        matrix = self.videoview.matrix()
#        print matrix.m11()
#        print matrix.m22()
        matrix.reset()

        matrix.scale(1280/width, 1024/height)
        self.videoview.setMatrix(matrix)
   #     self.videoview.centerOn(event.pos().x(), event.pos().y())

        self.videoview.centerOn(x + 0.5*width, y + 0.5*height)

        self.rs = None

    def videoViewMove(self, event):
        x, y = event.pos().x(), event.pos().y()
        mapScene =  self.videoview.mapToScene(x, y)
        x, y, = mapScene.x(), mapScene.y()

        if self.rs != None:
    #        self.rs.width = event.pos().x() - self.rs.x() + 10
     #       self.rs.height = event.pos().y() - self.rs.y() + 10
      #      self.rs.update()
            aspectRatio = self.dispGI.boundingRect().width()/self.dispGI.boundingRect().height()
            appliedRatio = (x - self.rs.x())/(y - self.rs.y())
            if appliedRatio >= aspectRatio:
                self.rs.height = y - self.rs.y()
                self.rs.width = 1.6*(y - self.rs.y())
            if appliedRatio < aspectRatio:
                self.rs.width = x - self.rs.x()
                self.rs.height = (x - self.rs.x())/aspectRatio
            self.rs.update()


    def updateVideo(self):
        try:
            image_data = self.video.read_and_queue()
            self.videoscene.removeItem(self.dispGI)
            select.select((self.video,), (), ())
            self.devImg = QImage(image_data, self.size_x, self.size_y,\
                                                         QImage.Format_RGB888)
            self.devImg.bits() #Necessary to prevent Seg Fault (unknown why)
            target = QRectF(0, 0, self.devImg.width(), self.devImg.height())
            source = QRectF(0, 0, self.devImg.width(), self.devImg.height())
            self.dispGI = VidImage(self, target, self.devImg, source)
            self.scene.clear()
            self.videoscene.addItem(self.dispGI)
            self.dispGI.setZValue(-1)
            self.videoscene.update()
        except:
            pass

    def on_lvStartPB_pressed(self):
        print "LIVE START!"
        self.video = v4l2capture.Video_device("/dev/video1")
        self.size_x, self.size_y = self.video.set_format(1280, 1024)
        self.video.create_buffers(1)
        self.video.queue_all_buffers()
        self.video.start()
        select.select((self.video,), (), ())
        image_data = self.video.read_and_queue()
        self.devImg = QImage(image_data, self.size_x, self.size_y,\
                                                     QImage.Format_RGB888)
        self.devImg.bits() #Necessary to prevent Seg Fault (unknown why)
        target = QRectF(0, 0, self.devImg.width(), self.devImg.height())
        source = QRectF(0, 0, self.devImg.width(), self.devImg.height())
        self.dispGI = VidImage(self, target, self.devImg, source)
        self.scene.clear()
        self.videoscene.addItem(self.dispGI)
        self.dispGI.setZValue(-1)
        self.videoscene.update()
        self.timer.start()

    def on_lvStopPB_pressed(self):
        print "LIVE STOP!"
        self.timer.stop()

    def preferencesTriggered(self):
        prefDialog = PreferenceDialog(self)
        prefDialog.show()

    def process_start(self, cmd):
        self.process = QProcess()
        self.process.start(cmd)
        self.connect(self.process, SIGNAL("readyRead()"),\
                        self.process_readyRead)
        self.connect(self.process, SIGNAL("finished(int)"),\
                        self.process_finished)
        
    def process_readyRead(self):
        self.count = self.count + 1
        try:
            out = self.process.readAll() #readAllStandardOutput()
            self.pic = numpy.fromstring(out, dtype = numpy.uint8)
            #print self.pic
            if len(self.pic) == 1000000:
                self.pic.resize((1000, 1000))
                stream = VideoStream(self.pic, self.count)
                self.videoscene.clear()
                self.videoscene.addItem(stream)
        except:
            print "Empty channel"

    def process_finished(self):
        print "FINISHED!"
        self.count = 0
        
    def on_distancebutton_released(self):
        ##########################################
        ##########################################
        ###         ####   ####    #####    ######
        ####### ###### #### ### ### ### #### #####
        ####### ###### #### ### #### ## #### #####
        ####### ###### #### ### #### ## #### #####
        ####### ###### #### ### ### ### #### #####
        ####### #######    ####    #####    ######
        ##########################################
        ##########################################
        print "To Do: Write Distance Function"
    
    def on_SNRbutton_released(self):
        pathfour = self.path1
        shape = (1000,1000)
        image_file = open(pathfour)
        # load a 1000000 length array
        image_array_1D5 = numpy.fromfile(file=image_file, dtype=numpy.uint16)
        image_file.close()
        image_array_2D5 = image_array_1D5.reshape(shape)
        image_8bit = (image_array_2D5 >> 6)
        
        fourierarray = image_array_1D5
        fourier = numpy.fft.fft(fourierarray, 1000000)
        t = numpy.arange(1000000)
        sp = fourier
        freq = numpy.fft.fftfreq(t.shape[-1])
       # print max(sp.real)
        #print len(freq)
        plt.plot(freq, abs(sp.real))#, freq, sp.imag)
        plt.show()
        ##########################################
        ##########################################
        ###         ####   ####    #####    ######
        ####### ###### #### ### ### ### #### #####
        ####### ###### #### ### #### ## #### #####
        ####### ###### #### ### #### ## #### #####
        ####### ###### #### ### ### ### #### #####
        ####### #######    ####    #####    ######
        ##########################################
        ##########################################
        print "To Do: Write SNR Function"
    
    def on_MagnifyPushButton_released(self):

        if self.enableQuadMag == False:
            self.MagnifyPushButton.setText("Turn Off Magnifying Glass")
            self.enableQuadMag = True
            return
        if self.enableQuadMag == True:
            self.MagnifyPushButton.setText("Turn On Magnifying Glass")
            mag = False
            return
        
    def comboChange(self):
        if str(self.comboBox.currentText()) == "":
            self.ClearButton.setEnabled(False)
        else:
            self.ClearButton.setEnabled(True)
            
    def on_ClearButton_released(self):
        self.scene.clear()
        if self.comboBox.currentText() == "All":
            self.loadinit("A", "Clear")
        if self.comboBox.currentText() == "3 Channels":
            self.loadinit("3C", "Clear")
        if self.comboBox.currentText() == "Channel 1":
            self.loadinit("1", "Clear")
        if self.comboBox.currentText() == "Channel 2":
            self.loadinit("2", "Clear")
        if self.comboBox.currentText() == "Channel 3":
            self.loadinit("3", "Clear")
        if self.comboBox.currentText() == "Channel 4":
            self.loadinit("4", "Clear")
        
    def keyPressEvent(self, event):
        if event.key() == 16777248:

            self.zoom = "-"
    def keyReleaseEvent(self, event):
        if event.key() == 16777248:

            self.zoom = "+"
            
    def on_LoadComposite_released(self):
        if self.comboBox.currentText() == "All":
            self.loadinit("A", "Load")
        if self.comboBox.currentText() == "3 Channels":
            self.loadinit("3C", "Load")
        if self.comboBox.currentText() == "Channel 1":
            self.loadinit("1", "Load")
        if self.comboBox.currentText() == "Channel 2":
            self.loadinit("2", "Load")
        if self.comboBox.currentText() == "Channel 3":
            self.loadinit("3", "Load")
        if self.comboBox.currentText() == "Channel 4":
            self.loadinit("4", "Load")
        
    def loadinit(self, type, mode):
        self.cParser.read(self.currentDir+"/.config/.polImgPro.cfg")
        if mode == "Load":
            if type == "1" or type == "A" or type == "3C":
                if self.C1Def.isChecked() == True:
                    self.path1 = self.cParser.get('PREFIMGPATHS','Path1')
                else:
                    self.path1 = QFileDialog.getOpenFileName(self, \
                            "Open File", self.path , str("Images (*raw)"))
                self.c1label.setText(str(self.path1.split("/")[-1]))
            print "1"
            if type == "2" or type == "A" or type == "3C":
                if self.C2Def.isChecked() == True:
                    self.path2 = self.cParser.get('PREFIMGPATHS','Path2')
                else:     
                    self.path2 = QFileDialog.getOpenFileName(self, \
                            "Open File", self.path , str("Images (*raw)"))
                self.c2label.setText(str(self.path2.split("/")[-1]))
            print "2"
            if type == "3" or type == "A" or type == "3C":
                if self.C3Def.isChecked() == True:
                    self.path3 = self.cParser.get('PREFIMGPATHS','Path3')
                else:
                    self.path3 = QFileDialog.getOpenFileName(self, \
                            "Open File", self.path , str("Images (*raw)"))
                self.c3label.setText(str(self.path3.split("/")[-1]))
            print "3"
            if type == "4" or type == "A":
                if self.C4Def.isChecked() == True:
                    self.path4 = self.cParser.get('PREFIMGPATHS','Path4')
                else:
                    self.path4 = QFileDialog.getOpenFileName(self, \
                            "Open File", self.path , str("Images (*raw)"))
                self.c4label.setText(str(self.path4.split("/")[-1]))
            print "4"
        if mode == "Clear":
            if type == '1' or type == 'A' or type == '3C':
                self.path1 = None
                self.c1label.setText('')
            if type == '2' or type == 'A' or type == '3C':
                self.path2 = None
                self.c2label.setText('')
            if type == '3' or type == 'A' or type == '3C':
                self.path3 = None
                self.c3label.setText('')
            if type == '4' or type == 'A':
                self.path4 = None
                self.c4label.setText('')
        print "5"
        self.ImageGenerator(self.path1, self.path2, self.path3, self.path4)
        print "6"

    def on_DotOn_released(self):
        self.dotpermission = True
        self.DotOff.setEnabled(True)
        self.DotOn.setEnabled(False)

    def on_DotOff_released(self):
        self.dotpermission = False
        self.DotOff.setEnabled(False)
        self.DotOn.setEnabled(True)

    def on_ClearDots_released(self):
        imageitems = self.scene.items()
        for item in imageitems:
            if str(item.__class__.__name__) == "DistanceLine"\
                or str(item.__class__.__name__) == "CircleMarker":
                self.scene.removeItem(item)
        self.scene.update()

        self.lastline = None

        self.lastcircle = []
        
    def on_SearchButton_released(self):
        x = self.xedit.text()
        y = self.yedit.text()
        
        itemlist = self.view.items()
        for item in itemlist:
            if str(item.__class__.__name__) == "GraphicsItem":
                item.searchExecuted(x, y)

    def on_SearchButton2_released(self):
        x = self.xedit2.text()
        y = self.yedit2.text()
        itemlist = self.compositeview1.items() + self.compositeview2.items()\
                        + self.compositeview3.items()\
                        + self.compositeview4.items()
        if x == '' or y == '':
            pass
        else:
            for item in itemlist:
                if str(item.__class__.__name__) == "QuadView":
                    try:
                        item.searchExecuted(x, y)
                    except:
                        print "Invalid Type"
                        break
    
    def OpenClicked(self):

        print "File Open Not Functional"

        
        path = QFileDialog.getOpenFileName(self,
            "Open File", self.path , str("Images (*raw *png)"))

      
        
        ftype = str(path.split(".")[-1])        
        
        if ftype == "raw":
            self.ImageGenerator(path, None, None, None)
      #  image_file = open(path)

        if ftype == "png":
            #import png as numpy array
            Image = mpimg.imread(str(path))
            #scale pixel values which are originally between 0 and 1 so that 
            #their values fall between 0 and 255 
            scaledimage = 255*Image
            #reformat pixel data type from float to numpy.uint8
            scaled_num_array = numpy.array(scaledimage,dtype=numpy.uint8)

            shape = (scaled_num_array.shape[0], scaled_num_array.shape[1])
            channel1 = scaled_num_array[:,:,2]
            channel2 = scaled_num_array[:,:,1]
            channel3 = scaled_num_array[:,:,0]
            alpha_array = 255*(numpy.ones(shape, dtype=numpy.uint8))

            # apparently alpha gets stacked last. load BGRA because the byte 
            #order in memory for each channel is stored in memory as BGRA 
            #0xBBGGRRAA by little-endian CPU's such as intel processors for 
            #future overlay work do  
            #example>>>>> image_ARGB = numpy.dstack(/
            #[image_Blue,image_Green,image_Red,alpha_array])
            image_ARGB_3D = numpy.dstack([channel1,channel2,\
                                            channel3,alpha_array])

            # reshape to a 2D array that has 4 bytes per pixel
            image_ARGB_2D = numpy.reshape(image_ARGB_3D,(-1,\
                                            scaled_num_array.shape[1]*4)) 
            #Reshape does not copy, only manipulates data structure holding the
            #data

            #Numpy buffer QImage declaration
            Image = QImage(image_ARGB_2D.data, scaled_num_array.shape[1],\
                            scaled_num_array.shape[0],\
                            QImage.Format_ARGB32)
            Image.ndarray = image_ARGB_2D  
            # necessary to create a persistant reference to the data per QImage
            #class
            target = QRectF(0, 0, Image.width(), Image.height())
            source = QRectF(0, 0, Image.width(), Image.height())
            compImage = CompImage(target, Image, source, self.selectedbrowser,\
                                    self.livebrowser, self.pixelValueBrowser, channel1) 
            self.scene.clear()
            self.scene.addItem(compImage)
            self.Image = Image
        
    def ImageGenerator(self, path1, path2, path3, path4):
        width = 1000
        height = 1000
        shape = (width, height)
        alpha_array = 255*(numpy.ones(shape, dtype=numpy.uint8))
        zero_array = numpy.zeros(shape, dtype=numpy.uint8)
        
        Red = zero_array
        Blue = zero_array
        Green = zero_array
        Yellow = zero_array
        Cyan = zero_array
        Magenta = zero_array
        White = zero_array
 
        image_array_2D1 = zero_array
        
        #Blue
        try:
            image_file = open(path1)
            # load a 1000000 length array
            image_array_1D1 = numpy.fromfile(file=image_file,\
                                                dtype=numpy.uint16)
            image_file.close()
            image_array_2D1 = image_array_1D1.reshape(shape)
            image_8bit1 = (image_array_2D1 >> 6)

        except:
            image_8bit1 = 0*alpha_array
        
        #Green
        try:
            image_file = open(path2)
            # load a 1000000 length array
            image_array_1D2 = numpy.fromfile(file=image_file,\
                                                dtype=numpy.uint16)
            image_file.close()
            image_array_2D2 = image_array_1D2.reshape(shape)
            image_8bit2 = (image_array_2D2 >> 6)
        except:
            image_8bit2 = 0*alpha_array         
        
        try:
            image_file = open(path3)
            image_array_1D3 = numpy.fromfile(file=image_file,\
                                                dtype=numpy.uint16)
            image_file.close()
            image_array_2D3 = image_array_1D3.reshape(shape)
            image_8bit3 = (image_array_2D3 >> 6)
        except:
            image_8bit3 = 0*alpha_array
            image_array_2D3 = alpha_array.reshape(shape)
        
            
        #Georg

        try:
            image_file = open(path4)
            # load a 1000000 length array
            image_array_1D4 = numpy.fromfile(file=image_file,\
                                                dtype=numpy.uint16)
            image_file.close()
            image_array_2D4 = image_array_1D4.reshape(shape)
            image_8bit4 = (image_array_2D4 >> 6)
        except:
            image_8bit4 = 0*alpha_array


        channelcombolist = [self.channel1combobox, self.channel2combobox,\
                                self.channel3combobox, self.channel4combobox]
        imagelist = [image_8bit1, image_8bit2, image_8bit3, image_8bit4]
        for item in range(4):
            if channelcombolist[item].currentText() == "Red":
                Red = Red + imagelist[item]
            elif channelcombolist[item].currentText() == "Blue":
                Blue = Blue + imagelist[item]
            elif channelcombolist[item].currentText() == "Green":
                Green = Green + imagelist[item]
            elif channelcombolist[item].currentText() == "Yellow":
                Yellow = Yellow + imagelist[item]
            elif channelcombolist[item].currentText() == "Cyan":
                Cyan = Cyan + imagelist[item]
            elif channelcombolist[item].currentText() == "Magenta":
                Magenta = Magenta + imagelist[item]
            elif channelcombolist[item].currentText() == "White":
                White = White + imagelist[item]
       
        
        image_ARGB_3D = numpy.dstack([(Blue + Cyan + Magenta + White)\
                                        .clip(0,255).astype(numpy.uint8),\
                                        (Green + Cyan + Yellow + White)\
                                        .clip(0,255).astype(numpy.uint8),\
                                        (Red + Magenta + Yellow + White)\
                                        .clip(0,255).astype(numpy.uint8),\
                                        alpha_array])
        
        # reshape to a 2D array that has 4 bytes per pixel
        image_ARGB_2D = numpy.reshape(image_ARGB_3D,(-1,width*4))
 
        #Numpy buffer QImage declaration
        Image = QImage(image_ARGB_2D.data, width, height, QImage.Format_ARGB32)
        Image.ndarray = image_ARGB_2D  

        target = QRectF(0, 0, Image.width(), Image.height())
        source = QRectF(0, 0, Image.width(), Image.height())
    
        compImage = CompImage(self, target, Image, source,\
                                self.selectedbrowser, self.livebrowser, \
                                self.pixelValueBrowser, image_array_2D1) 
        self.scene.clear()
        self.scene.addItem(compImage)
        self.Image = Image

        self.compinstanceL = []
        
        QV1 = QuadView(self,image_8bit1, zero_array, alpha_array, \
                            self.compositeview1, self.label11, \
                            self.SelectedTextBrowser_2, self.LivetextBrowser_2)
        self.compositescene1.clear()
        self.compositescene1.addItem(QV1)
        
        self.compositeview1.resetMatrix()
        matrix = self.compositeview1.matrix()
        horizontal = 0.5
        vertical = 0.5
        matrix.scale(horizontal, vertical)
        self.compositeview1.setMatrix(matrix)
        
        QV2 = QuadView(self, image_8bit2, zero_array, alpha_array,\
                            self.compositeview2, self.label12,\
                            self.SelectedTextBrowser_2, self.LivetextBrowser_2)
        self.compositescene2.clear()
        self.compositescene2.addItem(QV2)
        self.compositeview2.setMatrix(matrix)
        

        QV3 = QuadView(self, image_8bit3, zero_array, alpha_array,\
                            self.compositeview3, self.label21,\
                            self.SelectedTextBrowser_2, self.LivetextBrowser_2)
        self.compositescene3.clear()
        self.compositescene3.addItem(QV3)
        self.compositeview3.setMatrix(matrix)
        

        QV4 = QuadView(self, image_8bit4, zero_array, alpha_array,\
                            self.compositeview4, self.label22,\
                            self.SelectedTextBrowser_2, self.LivetextBrowser_2)
        self.compositescene4.clear()
        self.compositescene4.addItem(QV4)
        self.compositeview4.setMatrix(matrix)


def main():
    app = QApplication(sys.argv)
    window = STBimageviewer()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

