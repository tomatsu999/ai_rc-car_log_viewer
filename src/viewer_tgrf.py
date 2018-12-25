#Nobuyuki Tomatsu 181028
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton,QSlider)
import PyQt5
import matplotlib.pyplot as plt
import numpy as np
import sys
import converter_tgrf
import math
import matplotlib.patches as patches

STRAIGHT_LEN=5.40#m
RADIOUS_OUTER=1.27+1.5#m
RADIOUS_INNER=1.27#m
ROAD_WIDTH=RADIOUS_OUTER-RADIOUS_INNER#m
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.slider = QSlider(PyQt5.QtCore.Qt.Horizontal)
        self.slider.valueChanged[int].connect(self.sliderChanged)
        self.idxLine = QLineEdit()
        self.idxLine.setAlignment(PyQt5.QtCore.Qt.AlignRight)
        self.outputLine = [QLineEdit() for x in range(12)]
        for i in self.outputLine:
            i.setReadOnly(True)
            i.setAlignment(PyQt5.QtCore.Qt.AlignRight)

        self.prevButton = QPushButton("&<")
        self.prevButton.clicked.connect(self.goPrev)
        self.nextButton = QPushButton("&>")
        self.nextButton.clicked.connect(self.goNext)
        self.quitButton = QPushButton("&quit")
        self.quitButton.clicked.connect(self.quit)
        self.jumpButton = QPushButton("&jump")
        self.jumpButton.clicked.connect(self.jump)

        lineLayout = QGridLayout()
        lineLayout.addWidget(QLabel("slider"), 0, 0)
        lineLayout.addWidget(self.slider, 0, 1)
        lineLayout.addWidget(self.prevButton, 1, 0)
        lineLayout.addWidget(self.nextButton, 1, 1)
        lineLayout.addWidget(QLabel("idx"), 2, 0)
        lineLayout.addWidget(self.idxLine, 2, 1)
        for i in range(10):
            lineLayout.addWidget(self.outputLine[i], i+3, 1)
        lineLayout.addWidget(QLabel("distance 0"), 3, 0)
        lineLayout.addWidget(QLabel("distance 45"), 4, 0)
        lineLayout.addWidget(QLabel("distance 90"), 5, 0)
        lineLayout.addWidget(QLabel("distance 135"), 6, 0)
        lineLayout.addWidget(QLabel("distance 180"), 7, 0)
        lineLayout.addWidget(QLabel("distance 110"), 8, 0)
        lineLayout.addWidget(QLabel("distance 70"), 9, 0)
        lineLayout.addWidget(QLabel("steer"), 10, 0)
        lineLayout.addWidget(QLabel("speed"), 11, 0)
        lineLayout.addWidget(QLabel("time"), 12, 0)
        
        lineLayout.addWidget(QLabel("speed(km/h)"), 13, 0)
        lineLayout.addWidget(QLabel("turning radius(m)"), 14, 0)
        lineLayout.addWidget(self.outputLine[10], 13, 1)
        lineLayout.addWidget(self.outputLine[11], 14, 1)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.jumpButton)
        buttonLayout.addWidget(self.quitButton)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(lineLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Log Viewer")
    def jump(self):
        pass
    def goPrev(self):
        pass
    def goNext(self):
        pass
    def quit(self):
        pass

    def loadData(self,logfilename,pointfilename):
        #data loading
        self.data=np.load(logfilename)
        self.coursePoints=np.loadtxt(pointfilename,delimiter=',')
        self.slider.setRange(0,self.data.shape[0]-1)
        self.curIdx=0
        self.radius=np.zeros(self.data.shape[0])
        self.centerCoord=np.zeros((self.data.shape[0],2))
        #calculate turning radius and speed
        self.radius=0#need to be implemented
        self.speed=0#need to be implemented

        self.showData()
    def preparePlotWindow(self):
        pass
    def sliderChanged(self,value):
        pass
    def showData(self):
        pass
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.preparePlotWindow()
    main_window.loadData(sys.argv[1],"points_tgrf.csv")
    main_window.show()
    sys.exit(app.exec_())