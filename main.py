import os
import sys
import ui_16bitimagewindow #,png, itertools
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from widgetSetup import WidgetSetup
import ConfigParser

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

        setup = self.WidgetSetup(self)
        WidgetSetup.apportionDuties()

def main():
    app = QApplication(sys.argv)
    window = STBimageviewer()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
