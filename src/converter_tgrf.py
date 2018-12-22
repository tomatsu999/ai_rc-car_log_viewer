#Nobuyuki Tomatsu 181222
import numpy as np
import math

import matplotlib.pyplot as plt
EPSILON=0.0001
STRAIGHT_LEN=5.40#meter
RADIOUS_OUTER=1.27+1.5#meter
RADIOUS_INNER=1.27#meter
ROAD_WIDTH=RADIOUS_OUTER-RADIOUS_INNER#meter
ANGLES_SENSORS=[0, 45, 90, 135, 180, 110, 70]
MAX_SENSING_LENGTH=10

def crossPoint(linePoints):
    allPointList=np.zeros((0,2))
    for i in range(len(linePoints)):
        sourcePoint=linePoints[i][0,:]
        targetPoint=linePoints[i][1,:]

        '''
        sourceAreaID=0
        # 1:left semicircle of center wall
        # 2:right semicircle of center wall
        # 3:top square of center wall
        # 4:bottom square of center wall
        # 0:other area
        if RADIOUS_OUTER<sourcePoint[0]<RADIOUS_OUTER+STRAIGHT_LEN:
            if ROAD_WIDTH<sourcePoint[1]<=RADIOUS_OUTER:
                sourceAreaID=3
            elif RADIOUS_OUTER<sourcePoint[1]<RADIOUS_OUTER+RADIOUS_INNER:
                sourceAreaID=4
        elif (sourcePoint[0]-RADIOUS_OUTER)**2+(sourcePoint[1]-RADIOUS_OUTER)**2<=0.5**2:
            sourceAreaID=1
        elif (sourcePoint[0]-(RADIOUS_OUTER+STRAIGHT_LEN))**2+(sourcePoint[1]-RADIOUS_OUTER)**2<=0.5**2:
            sourceAreaID=2
        '''

        #calculate parameters of line
        a=(linePoints[i][1,1]-linePoints[i][0,1])/(linePoints[i][1,0]-linePoints[i][0,0])
        b=linePoints[i][0,1]-linePoints[i][0,0]*a
        #check if line is vertical or horizontal
        vertical=0
        vertical_x=linePoints[i][0,0]
        if abs(linePoints[i][0,0]-linePoints[i][1,0])<EPSILON:
            vertical=1
        horizontal=0
        if abs(linePoints[i][0,1]-linePoints[i][1,1])<EPSILON:
            horizontal=1
        #print(vertical,horizontal,linePoints[i][0,0],linePoints[i][1,0])
        pointList=np.zeros((0,2))

        if horizontal==0:
            #line outer top
            x=(0-b)/a
            if x>=RADIOUS_OUTER and x<RADIOUS_OUTER+STRAIGHT_LEN:
                if sourcePoint[1]>0:
                    pointList=np.concatenate((pointList,np.array([[x,0]])),axis=0)
            #line inner top
            x=(ROAD_WIDTH-b)/a
            if x>=RADIOUS_OUTER and x<RADIOUS_OUTER+STRAIGHT_LEN:
                if sourcePoint[1]<ROAD_WIDTH:
                    print(pointList)
                    pointList=np.concatenate((pointList,np.array([[x,ROAD_WIDTH]])),axis=0)
                    print(pointList)
            #line inner bottom
            x=(RADIOUS_OUTER+RADIOUS_INNER-b)/a
            if x>=RADIOUS_OUTER and x<RADIOUS_OUTER+STRAIGHT_LEN:
                if sourcePoint[1]>RADIOUS_OUTER+RADIOUS_INNER:
                    pointList=np.concatenate((pointList,np.array([[x,RADIOUS_OUTER+RADIOUS_INNER]])),axis=0)
            #line outer bottom
            x=(RADIOUS_OUTER*2-b)/a
            if x>=RADIOUS_OUTER and x<RADIOUS_OUTER+STRAIGHT_LEN:
                if sourcePoint[1]<RADIOUS_OUTER*2:
                    pointList=np.concatenate((pointList,np.array([[x,RADIOUS_OUTER*2]])),axis=0)

            #dummy wall
            x=(RADIOUS_OUTER-b)/a
            if x>=RADIOUS_OUTER and x<RADIOUS_OUTER+STRAIGHT_LEN:
                pointList=np.concatenate((pointList,np.array([[x,RADIOUS_OUTER]])),axis=0)

        #arc outer left
        xc,yc=RADIOUS_OUTER,RADIOUS_OUTER
        point=crossPointLineAndCircle(a,b,vertical,vertical_x,xc,yc,RADIOUS_OUTER)
        if point.shape[0]==2:
            point=point[np.argsort(point[:,1]),:]
            onLineIdx=np.where(point[:,0]<=RADIOUS_OUTER)[0]
            if onLineIdx.shape[0]==1 and sourcePoint[0]>targetPoint[0]:
                pointList=np.concatenate((pointList,point[onLineIdx[0],:][np.newaxis,:]),axis=0)
            elif onLineIdx.shape[0]==2:
                if sourcePoint[1]>targetPoint[1]:
                    pointList=np.concatenate((pointList,point[0,:][np.newaxis,:]),axis=0)
                else:
                    pointList=np.concatenate((pointList,point[1,:][np.newaxis,:]),axis=0)

        #arc inner left
        xc,yc=RADIOUS_OUTER,RADIOUS_OUTER
        point=crossPointLineAndCircle(a,b,vertical,vertical_x,xc,yc,RADIOUS_INNER)
        if point.shape[0]==2:
            point=point[np.argsort(point[:,1]),:]
            onLineIdx=np.where(point[:,0]<=RADIOUS_OUTER)[0]
            if onLineIdx.shape[0]==1 and sourcePoint[0]<targetPoint[0]:
                pointList=np.concatenate((pointList,point[onLineIdx[0],:][np.newaxis,:]),axis=0)
            elif onLineIdx.shape[0]==2:
                if sourcePoint[1]<targetPoint[1]:
                    pointList=np.concatenate((pointList,point[0,:][np.newaxis,:]),axis=0)
                else:
                    pointList=np.concatenate((pointList,point[1,:][np.newaxis,:]),axis=0)


        #arc inner right
        xc,yc=STRAIGHT_LEN+RADIOUS_OUTER,RADIOUS_OUTER
        point=crossPointLineAndCircle(a,b,vertical,vertical_x,xc,yc,RADIOUS_INNER)
        if point.shape[0]==2:
            point=point[np.argsort(point[:,1]),:]
            onLineIdx=np.where(point[:,0]>=RADIOUS_OUTER+STRAIGHT_LEN)[0]
            if onLineIdx.shape[0]==1 and sourcePoint[0]>targetPoint[0]:
                pointList=np.concatenate((pointList,point[onLineIdx[0],:][np.newaxis,:]),axis=0)
            elif onLineIdx.shape[0]==2:
                if sourcePoint[1]<targetPoint[1]:
                    pointList=np.concatenate((pointList,point[0,:][np.newaxis,:]),axis=0)
                else:
                    pointList=np.concatenate((pointList,point[1,:][np.newaxis,:]),axis=0)

        #arc outer right
        xc,yc=STRAIGHT_LEN+RADIOUS_OUTER,RADIOUS_OUTER
        point=crossPointLineAndCircle(a,b,vertical,vertical_x,xc,yc,RADIOUS_OUTER)
        if point.shape[0]==2:
            point=point[np.argsort(point[:,1]),:]
            onLineIdx=np.where(point[:,0]>=RADIOUS_OUTER+STRAIGHT_LEN)[0]
            if onLineIdx.shape[0]==1 and sourcePoint[0]<targetPoint[0]:
                pointList=np.concatenate((pointList,point[onLineIdx[0],:][np.newaxis,:]),axis=0)
            elif onLineIdx.shape[0]==2:
                if sourcePoint[1]>targetPoint[1]:
                    pointList=np.concatenate((pointList,point[0,:][np.newaxis,:]),axis=0)
                else:
                    pointList=np.concatenate((pointList,point[1,:][np.newaxis,:]),axis=0)

        #check if points are in line
        area=np.sort(linePoints[i],axis=0)
        larger=np.logical_and(pointList[:,0]>=area[0,0],pointList[:,1]>=area[0,1])
        smaller=np.logical_and(pointList[:,0]<=area[1,0],pointList[:,1]<=area[1,1])
        inAreaIdx=np.where(np.logical_and(larger,smaller))[0]
        pointListArea=pointList[inAreaIdx,:]
        #set max distant point if there is no cross point
        if pointListArea.shape[0]==0:
            #pointListArea=linePoints[i][1,:][np.newaxis,:]
            pointListArea=linePoints[i][0,:][np.newaxis,:]
        #select cross point of shortest distance
        distances=np.sqrt((pointListArea[:,0]-linePoints[i][0,0])**2+(pointListArea-linePoints[i][0,1])[:,1]**2)
        minIdx=np.argmin(distances)
        nearestPoint=pointListArea[minIdx,:]
        if RADIOUS_OUTER<nearestPoint[0]<RADIOUS_OUTER+STRAIGHT_LEN and nearestPoint[1]==RADIOUS_OUTER:
            nearestPoint=sourcePoint
        
        allPointList=np.concatenate((allPointList,nearestPoint[np.newaxis,:]),axis=0)
    return allPointList

def crossPointLineAndCircle(a,b,vertical,vertical_x,xc,yc,r):
    #calculate cross point (line and circle)
    if vertical==0:
        #(x-xc)^2+(y-yc)^2=r^2
        #x^2-2*xc*x+xc^2+y^2-2*yc*y+yc^2=r^2
        #y=a*x+b
        #x^2-2*xc*x+xc^2+(a*x+b)^2-2*yc*(a*x+b)+yc^2=r^2
        #x^2-2*xc*x+xc^2 +a^2*x^2+2*a*b*x+b^2 -2*yc*a*x-2*yc*b+yc^2=r^2
        #(1+a^2)*x^2+(-2*xc+2*a*b-2*yc*a)*x+xc^2+b^2-2*yc*b+yc^2-r^2=0

        #AX^2+BX+C=0 => X=(-B+-sqrt(B^2-4*A*C))/2*A
        A=1+a**2
        B=-2*xc+2*a*b-2*yc*a
        C=xc**2+b**2-2*yc*b+yc**2-r**2
        if B**2-4*A*C<0:
            return np.array([])
        x1=(-B+math.sqrt(B**2-4*A*C))/(2*A)
        x2=(-B-math.sqrt(B**2-4*A*C))/(2*A)
        y1=a*x1+b
        y2=a*x2+b
        return np.array([[x1,y1],[x2,y2]])
    else:
        #(x-xc)^2+(y-yc)^2=r^2
        #(xline-xc)^2+(y-yc)^2=r^2
        #y^2-2*yc*y+yc^2+(xline-xc)^2-r^2=0
        A=1
        B=-2*yc
        C=yc**2+(vertical_x-xc)**2-r**2
        #print(B**2-4*A*C)
        if B**2-4*A*C<0:
            return np.array([])
        y1=(-B+math.sqrt(B**2-4*A*C))/(2*A)
        y2=(-B-math.sqrt(B**2-4*A*C))/(2*A)
        x1=vertical_x
        x2=vertical_x
        return np.array([[x1,y1],[x2,y2]])

def line(pointCenter,pointFront,angles,length):
    #calculate line for sensors
    vec=pointFront-pointCenter
    cosVal=vec[0]/math.sqrt(vec[0]**2+vec[1]**2)
    angle=math.acos(cosVal)
    if vec[1]<0:
        angle=-angle
    lineAngles=angle+angles
    lineStart=pointCenter
    lineEnd=np.zeros((len(angles),2))
    lineEnd[:,0]=lineStart[0]+np.cos(lineAngles)*length
    lineEnd[:,1]=lineStart[1]+np.sin(lineAngles)*length
    linePointList=[]
    for i in range(lineEnd.shape[0]):
        tmp=np.zeros((2,2))
        tmp[0,:]=lineStart
        tmp[1,:]=lineEnd[i,:]
        linePointList.append(tmp)
    return linePointList

def convert(pointCenter,pointFront):
    

    angles=(np.array(ANGLES_SENSORS)-90.0)*math.pi/180.0

    #calculate line of sensors
    linePoints=line(pointCenter,pointFront,angles,MAX_SENSING_LENGTH)

    #calculate coordinates of sensed points
    sensedPoints=crossPoint(linePoints)

    #calculate distances of sensed points
    vecToPoints=sensedPoints-np.tile(pointCenter,(sensedPoints.shape[0],1))
    distances=np.sqrt(vecToPoints[:,0]**2+vecToPoints[:,1]**2)
    return (distances,linePoints,sensedPoints)
def convert2(pointCenter,pointCenterOld):
    
    pointFront=(pointCenter-pointCenterOld)+pointCenter

    angles=-(np.array(ANGLES_SENSORS)-90.0)*math.pi/180.0

    #calculate line of sensors	
    linePoints=line(pointCenter,pointFront,angles,MAX_SENSING_LENGTH)

    #calculate coordinates of sensed points
    sensedPoints=crossPoint(linePoints)

    #calculate distances of sensed points
    vecToPoints=sensedPoints-np.tile(pointCenter,(sensedPoints.shape[0],1))
    distances=np.sqrt(vecToPoints[:,0]**2+vecToPoints[:,1]**2)
    return (distances,linePoints,sensedPoints)
def createRLInput(distances):
    RLInput=np.zeros(distances.shape[0]*4)
    for i, dis in enumerate(distances):
        RLInput[i*4+1]=1.0
        RLInput[i*4+3]=dis/MAX_SENSING_LENGTH
    return np.array(RLInput)
if __name__=="__main__":
    #demo

    #setting car center coordinate
    car_center=np.array([0.8,1])
    #setting old car center coordinate
    car_center_old=np.array([0.6,0.5])

    car_center=np.array([2.5,-0.2])
    car_center_old=np.array([2.0,-0.205])

    car_center=np.array([2.1,1.2])
    car_center_old=np.array([2.0,1.21])

    


    (distances,linePoints,sensedPoints)=convert2(car_center,car_center_old)
    RLInput=createRLInput(distances)

    #loading course point
    points=np.loadtxt("points_tgrf.csv",delimiter=',')
    #displaying
    print("distances")
    print(distances)
    print("RL model Input")
    print(RLInput)
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(points[:,0],-points[:,1],color='#888888',marker='.',ls='')
    for i in range(len(linePoints)):
        ax.plot(linePoints[i][:,0],-linePoints[i][:,1],'--c')
    
    for i in range(7):
        ax.plot([linePoints[i][0,0],sensedPoints[i,0]],[-linePoints[i][0,1],-sensedPoints[i,1]],'-b')

    #ax.plot(sensedPoints[:,0],-sensedPoints[:,1],'^r')

    ax.set_xlim([-RADIOUS_INNER,RADIOUS_OUTER*2+STRAIGHT_LEN+RADIOUS_INNER])
    ax.set_ylim([-RADIOUS_OUTER*2-RADIOUS_INNER,RADIOUS_INNER])
    plt.show()