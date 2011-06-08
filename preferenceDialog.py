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
preferenceDialog.py

Created by Roger Conturie and Nick Conway on 2011-06-03.
"""


import os, sys, ui_preferenceDialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ConfigParser
"""
cParser = ConfigParser.ConfigParser()
cParser.read(currentDir+"/.polImgPro.cfg")
"""

class PreferenceDialog(QDialog, ui_preferenceDialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(PreferenceDialog, self).__init__(parent)
        self.setupUi(self)
        self.okButton = self.buttonBox.buttons()[0]
        self.cancelButton = self.buttonBox.buttons()[1]
        self.path = QDir.homePath()
        self.configure()
        self.establishConnections()

    def configure(self):

        self.currentDir = os.getcwd()
        self.cParser = ConfigParser.ConfigParser()
        self.cParser.read(self.currentDir+"/.config"+"/.polImgPro.cfg")
        self.path1 = self.cParser.get('PREFIMGPATHS','Path1')
        self.path2 = self.cParser.get('PREFIMGPATHS','Path2')
        self.path3 = self.cParser.get('PREFIMGPATHS','Path3')
        self.path4 = self.cParser.get('PREFIMGPATHS','Path4')
        self.ch1LineEdit.setText(self.path1)
        self.ch2LineEdit.setText(self.path2)
        self.ch3LineEdit.setText(self.path3)
        self.ch4LineEdit.setText(self.path4)        

    def establishConnections(self):
        self.okButton.released.connect(self.okButtonPress)
        self.cancelButton.released.connect(self.cancelButtonPress)
        self.browseCh1Button.released.connect(self.browseCh1Pressed)
        self.browseCh2Button.released.connect(self.browseCh2Pressed)
        self.browseCh3Button.released.connect(self.browseCh3Pressed)
        self.browseCh4Button.released.connect(self.browseCh4Pressed)

    def updateConfig(self):
        with open(self.currentDir+"/.config"+"/.polImgPro.cfg", 'w') as config:
            self.cParser.write(config)

    def okButtonPress(self):
        print "ok"

    def cancelButtonPress(self):
        print "cancel"

    def browseCh1Pressed(self):
        self.path1 = QFileDialog.getOpenFileName(self,
                "Open File", self.path , str("Images (*raw)"))  #*.png *.xpm *.jpg
        self.cParser.read(self.currentDir+"/.config"+"/.polImgPro.cfg")
        self.cParser.set('PREFIMGPATHS','Path1',self.path1)
        self.ch1LineEdit.setText(self.path1)
        self.updateConfig()

    def browseCh2Pressed(self):
        self.path2 = QFileDialog.getOpenFileName(self,
                "Open File", self.path , str("Images (*raw)"))  #*.png *.xpm *.jpg
        self.cParser.read(self.currentDir+"/.config"+"/.polImgPro.cfg")
        self.cParser.set('PREFIMGPATHS','Path2',self.path2)
        self.ch2LineEdit.setText(self.path2)
        self.updateConfig()

    def browseCh3Pressed(self):
        self.path3 = QFileDialog.getOpenFileName(self,
                "Open File", self.path , str("Images (*raw)"))  #*.png *.xpm *.jpg
        self.cParser.read(self.currentDir+"/.config"+"/.polImgPro.cfg")
        self.cParser.set('PREFIMGPATHS','Path3',self.path3)
        self.ch3LineEdit.setText(self.path3)
        self.updateConfig()

    def browseCh4Pressed(self):
        self.path4 = QFileDialog.getOpenFileName(self,
                "Open File", self.path , str("Images (*raw)"))  #*.png *.xpm *.jpg
        self.cParser.read(self.currentDir+"/.config"+"/.polImgPro.cfg")
        self.cParser.set('PREFIMGPATHS','Path4',self.path4)
        self.ch4LineEdit.setText(self.path4)
        self.updateConfig()

def main():
    app = QApplication(sys.argv)
    window = PreferenceDialog()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

