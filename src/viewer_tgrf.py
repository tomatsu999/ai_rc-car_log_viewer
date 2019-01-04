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
        idx=int(self.idxLine.text())
        if 0<idx<self.data.shape[0]:
            self.slider.setValue(idx)
            self.curIdx=idx
            self.showData()
    def goPrev(self):
        if self.curIdx>0:
            self.curIdx-=1
            self.showData()
    def goNext(self):
        if self.curIdx<self.data.shape[0]-1:
            self.curIdx+=1
            self.showData()
    def quit(self):
        plt.close(self.mapFigure)
        plt.close(self.valFigure)
        self.close()

    def loadData(self,logfilename,pointfilename):
        #data loading
        self.data=np.load(logfilename)
        self.coursePoints=np.loadtxt(pointfilename,delimiter=',')
        self.slider.setRange(0,self.data.shape[0]-1)
        self.curIdx=0
        self.radius=np.zeros(self.data.shape[0])
        self.centerCoord=np.zeros((self.data.shape[0],2))
        #calculate turning radius and speed
        for i in range(2,self.data.shape[0]):
            (self.radius[i],self.centerCoord[i,:])=self.turningRadius(self.data[(i-2):(i+1),9:11])
        self.speed=np.zeros(self.data.shape[0])
        self.speed[2:]=(3600.0/1000.0) * \
                        np.sqrt(np.sum((self.data[2:self.data.shape[0],9:11]-self.data[1:self.data.shape[0]-1,9:11])**2,axis=1))/ \
                        (self.data[2:self.data.shape[0],12]-self.data[1:self.data.shape[0]-1,12])
        self.showData()
    def turningRadius(self,points):
        epsilon=1e-20
        #set invalid value if two points are same
        if np.all(points[0,:]==points[1,:]) or np.all(points[1,:]==points[2,:]):
            return((-1,np.array([-1,-1])))
        #calculate perpendicular bisector(for 2 sets of points)
        #line 1 (point 0 and 1)
        med1=(points[0,:]+points[1,:])/2.0
        vec1=points[0,:]-points[1,:]
        if points[0,1]==points[1,1]:
            vertical1=True
            x1=med1[0]
        else:
            vertical1=False
            a1=-vec1[0]/vec1[1]
            b1=-med1[0]*a1+med1[1]
        #line 1 (point 1 and 2)
        med2=(points[1,:]+points[2,:])/2.0
        vec2=points[1,:]-points[2,:]
        if points[1,1]==points[2,1]:
            vertical2=True
            x2=med2[0]
        else:
            vertical2=False
            a2=-vec2[0]/vec2[1]
            b2=-med2[0]*a2+med2[1]

        #calculate center of circle
        if vertical1==True and vertical2==True:
            #set invalid value if two lines are parallel(vertical)
            return((-1,np.array([-1,-1])))
        elif vertical1==True:
            #case that line 1 is vertical
            result_point=np.array([x1,x1*a2+b2])
            result_radius=np.sqrt(np.sum((result_point-points[0,:])**2))
        elif vertical2==True:
            #case that line 2 is vertical
            result_point=np.array([x2,x2*a1+b1])
            result_radius=np.sqrt(np.sum((result_point-points[2,:])**2))
        elif np.abs(a1-a2)<=epsilon:
            #set invalid value if two lines are parallel
            return((-100,np.array([-1,-1])))
        else:
            tmp_x=-(b1-b2)/(a1-a2)
            result_point=np.array([tmp_x,tmp_x*a1+b1])
            result_radius=np.sqrt(np.sum((result_point-points[0,:])**2))
        return(result_radius,result_point)

    def preparePlotWindow(self):
        self.mapFigure,self.mapAxes=plt.subplots(figsize=(6,4))
        self.mapAxes.set_title('course map')
        self.mapAxes.plot([0],[0])

        #self.mapAxes.title.set_text('course map')
        self.valFigure,self.valAxes=plt.subplots(11,1,figsize=(2,6))
        #self.valFigure=plt.figure(figsize=(2,6))#plt.subplots(9,1,figsize=(2,6))
        #self.valAxes=[None]*9
        for i in range(11):
            #self.valAxes[i]=self.valFigure.add_subplot(5,2,i+1)
            self.valAxes[i].plot([0])
            
        self.valAxes[0].set_title('distance 0')
        self.valAxes[1].set_title('distance 45')
        self.valAxes[2].set_title('distance 90')
        self.valAxes[3].set_title('distance 135')
        self.valAxes[4].set_title('distance 180')
        self.valAxes[5].set_title('distance 110')
        self.valAxes[6].set_title('distance 70')
        self.valAxes[7].set_title('steer')
        self.valAxes[8].set_title('speed')
        plt.show(block=False)
    def sliderChanged(self,value):
        self.curIdx=value
        self.showData()
    def showData(self):
        #print(value)
        car_center=self.data[self.curIdx,9:11]
        if self.data.shape[1]<=13:
            car_center_old=self.data[self.curIdx-1,9:11]
        else:
            car_center_old=self.data[self.curIdx,13:15]
        #(distances,linePoints,sensedPoints)=converter.convert2(car_center,car_center_old)
        MAX_DIST=10
        ANGLES_SENSORS=[0, 45, 90, 135, 180, 110, 70]
        angles=-(np.array(ANGLES_SENSORS)-90.0)*math.pi/180.0
        linePointsMax=converter_tgrf.line(car_center,2*car_center-car_center_old,angles,MAX_DIST)
        linePoints=converter_tgrf.line(car_center,2*car_center-car_center_old,angles,self.data[self.curIdx,:7])
        self.mapAxes.cla()
        self.mapAxes.plot(self.data[:,9],-self.data[:,10],'y--')
        self.mapAxes.plot(self.coursePoints[:,0],-self.coursePoints[:,1],'k.')
        
        #sensed point
        for i in range(7):
            self.mapAxes.plot(linePointsMax[i][:,0],-linePointsMax[i][:,1],'--c')
            self.mapAxes.plot(linePoints[i][:,0],-linePoints[i][:,1],'-b')
        #self.mapAxes.plot(sensedPoints[:,0],-sensedPoints[:,1],'.r')

        #car point
        self.mapAxes.plot(self.data[self.curIdx,9],-self.data[self.curIdx,10],'mo')
        if self.curIdx>=1:
            self.mapAxes.plot(self.data[self.curIdx-1,9],-self.data[self.curIdx-1,10],'g.')
        if self.curIdx>=2:
            self.mapAxes.plot(self.data[self.curIdx-2,9],-self.data[self.curIdx-2,10],'g.')
        if 100>=self.radius[self.curIdx]>=0:
            c=patches.Circle(xy=(self.centerCoord[self.curIdx,0], -self.centerCoord[self.curIdx,1]), radius=self.radius[self.curIdx], ec='#888888',fill=False)
            self.mapAxes.add_patch(c)
        
        #graph
        startIdx=max(0,self.curIdx-30)
        for i in range(7):
            self.valAxes[i].cla()
            self.valAxes[i].plot(self.data[startIdx:self.curIdx+1,i],'b')
        for i in range(7,9):
            self.valAxes[i].cla()
            self.valAxes[i].plot(self.data[startIdx:self.curIdx+1,i],'g')
        self.valAxes[9].cla()
        self.valAxes[9].plot(self.speed[startIdx:self.curIdx+1],'r')
        self.valAxes[10].cla()
        self.valAxes[10].plot(self.radius[startIdx:self.curIdx+1],'r')
        for i in range(9):
            self.outputLine[i].setText("%.4f" % self.data[self.curIdx,i])
        self.outputLine[9].setText("%.4f" % self.data[self.curIdx,12])

        self.outputLine[10].setText("%.4f" % self.speed[self.curIdx])
        self.outputLine[11].setText("%.4f" % self.radius[self.curIdx])

        self.idxLine.setText(str(self.curIdx))
        self.mapAxes.set_xlim([-RADIOUS_INNER,RADIOUS_OUTER*2+STRAIGHT_LEN+RADIOUS_INNER])
        self.mapAxes.set_ylim([-RADIOUS_OUTER*2-RADIOUS_INNER,RADIOUS_INNER])
        self.mapFigure.canvas.draw()
        self.valFigure.canvas.draw()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.preparePlotWindow()
    main_window.loadData(sys.argv[1],"points_tgrf.csv")
    main_window.show()
    sys.exit(app.exec_())