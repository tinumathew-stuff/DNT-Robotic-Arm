import cv2
import mediapipe as mp
import time
import math
from pyfirmata import Arduino, SERVO
import inspect



def motion(servopin,servo_position,servo_reading):
    
    if servo_reading != servo_position :
        if servo_reading > servo_position:
            diff = servo_reading - servo_position
            if diff <= 5:
                servo_position += diff
                rotate(servopin,servo_position)
                #print("hello1")
            else :
                servo_position += 5
                rotate(servopin,servo_position)
                #print("hello2")
        elif servo_reading < servo_position:
            diff = servo_position - servo_reading
            if diff <=5:
                servo_position -= diff
                rotate(servopin,servo_position)
                #print("hello3")
            else:
                servo_position -= 5
                rotate(servopin,servo_position)
                #print("hello4")
    else:
        pass


if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

port='COM7'
pin=10
board=Arduino(port)
board.digital[pin].mode=SERVO
board.digital[9].mode=SERVO
board.digital[11].mode=SERVO
board.digital[5].mode=SERVO
board.digital[3].mode=SERVO

def rotate(pin,angle):
    board.digital[pin].write(angle)

'''
for i in range(180):
    rotate(9,i)
    print(i)
    time.sleep(0.1)
'''

def bootsequence():
        rotate(5,30)
        rotate(11,90)
        rotate(3,55)
        rotate(9,85)
        rotate(10,180)


        for i in range(180,90,-1):
            rotate(10,i)
            print(i)
            time.sleep(0.01)
        for i in range(90,134):
            rotate(10,i)
            print(i)
            time.sleep(0.01)
        
        for m in range(85,180,1):
            rotate(9,m)
            print(m)
            time.sleep(0.01)
        for m in range(180,85,-1):
            rotate(9,m)
            print(m)
            time.sleep(0.01)
        rotate(11,90)
        for z in range(30,130):
            rotate(5,z)
            time.sleep(0.01)
        for z in range(130,30,-1):
            rotate(5,z)
            time.sleep(0.01)
        for z in range(55,180):
            rotate(3,z)
            print(z)
            time.sleep(0.01)
        for z in range(180,0,-1):
            rotate(3,z)
            print(z)
            time.sleep(0.01)


bootsequence() 

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands= 1, min_detection_confidence= 0.5, min_tracking_confidence= 0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

global finalangle5a
global finalangle1a
global finalangle2a
global angle3a
global finalangle4a

finalangle1a = 85
finalangle2a = 134
finalangle4a = 55
finalangle5a = 30
angle3a = 90


finalangle1 = 0
finalangle2 = 0
angle3 = 0
finalangle4 = 0
finalangle5 = 0

angle1=0
angle2=0
angle3=0
angle4=0
angleyolo=90
#rotate(10,90)
#rotate(11,90)


finalangle1=20
finalangle2=0
def anglefinder(C,A=50,B=50):
    cos_a=((-(A**2))+(B**2)+(C**2))/(2*B*C)
    cos_b=((A**2)+(-(B**2))+(C**2))/(2*A*C)
    cos_c=((A**2)+(B**2)+(-(C**2)))/(2*A*B)

    alpha=math.degrees(math.acos(cos_a))
    beta=math.degrees(math.acos(cos_b))
    gamma=math.degrees(math.acos(cos_c))
    anglelist=[gamma,alpha,beta,C]
    return anglelist
    #return A,B,C,cos_a

def anglecorrector(y,angle,maxangle=90,range=400):
    #if y<0:
        #y=y*-1
    return((y/range)*maxangle)+angle
def gripangle(pointA,pointB):

    y=int(distcalc(pointA,pointB,1))+20
    if y>=130:
        y=130
    return y

    #x=pointA[2]
    #z=int((y**(1/x)*1000)-1000)
    #print(z)
    #y=z
    #z=int(((y**(1/x)*1000)-1000))


    #print(z,pointA[2],pointB[2])

def bruhh(x):
    y=(((100-x)/60)*90)+125
    #print(int(y))
    return int(y)
def planeanglefinder(pointA,pointB,pointC):
    x1,y1,z1=pointA[0],pointA[1],pointA[2]
    x2,y2,z2=pointB[0],pointB[1],pointB[2]
    x3,y3,z3=pointC[0],pointC[1],pointC[2]
    a1 = x2 - x1
    b1 = y2 - y1
    c1 = z2 - z1
    a2 = x3 - x1
    b2 = y3 - y1
    c2 = z3 - z1
    a = b1 * c2 - b2 * c1
    b = a2 * c1 - a1 * c2
    c = a1 * b2 - b1 * a2
    d = (- a * x1 - b * y1 - c * z1)
    #print(a1,b1,c1,a2,b2,c2)
    #print(pointA,pointB,pointC,a,b,c)

    cosa=(c*1300)/(1300*(((a**2)+(b**2)+(c**2))**1/2))
    x=math.acos(cosa)
    angle=math.degrees(x)
    angle=((angle-89)*10000)-9960
    if angle<0:
        angle=angle*-1
    return int(angle)

'''def planeanglefinder2(pointA,pointB):
    x1,y1,z1=pointA[0],pointA[1],pointA[2]
    x2,y2,z2=pointB[0],pointB[1],pointB[2]
    A=x2-x1
    B=y2-y1
    C=z2-z1
    cosa=(C/((A**2)+(B**2)+(C**2))**1/2)
    x=math.acos(cosa)
    angle=math.degrees(x)
    #print(angle)
    angle=((angle-89)*100)

    print(angle)
    #angle correction part
    angle=int(((145-angle)/75)*180)
    if angle<=0:
        angle=0
    if angle>=180:
        angle=180
    angle=180-angle
    #print(angle)
    return  angle
'''

def tilt(pointA,pointB):
    x=int(distcalc(pointA,pointB,1))
    #print(x)
    if x>=180:
        x=180
    return x

def anglesmoother(x,y,z):
    for i in range(x,y):
        rotate(z,i)

def distcalc(point1,point2,sel=0):
    x2=point2[0]
    x1=point1[0]
    y2=point2[1]
    y1=point1[1]
    z2=point2[2]
    z1=point1[2]
    if sel==1:
        z2,z1=0,0
    distance=(((x2-x1)**2)+((y2-y1)**2)+((z2-z1)**2))**(1/2)
    return distance

initcordinate=[2,33,69]
angle1,angle2,angle3,angle4=[0,0,0],[0,0,0],[0,0,0],[0,0,0]
pointA,pointB,pointC=[1,1,1],[2,2,2],[4,5,6]
pointgripA,pointgripB=[1,1,1],[1,1,1]
pointextraB=[0,0,0]

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    try:
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy,cz = (int(lm.x * w)-300)*-1, (int(lm.y * h)-500)*-1,(lm.z*5000)*-1
            

                    #print(img.shape)
                    if id==9:
                        coordinate=[cx,cy,cz]
                        yolo=anglefinder((distcalc(coordinate,initcordinate))/5)
                        #print(int(yolo[0]),int(anglecorrector(cy,yolo[1])),(int(anglecorrector(cx,0,90,300)))+90)
                        angle1=int(yolo[0])
                        angle2=int(anglecorrector(cy,yolo[1]))
                        angle3=(int(anglecorrector(cx,0,90,300)))+90
                    if id==5:
                        pointA=[cx,cy,int(cz)]
                    if id==17:
                        pointB=[cx,cy,int(cz)]
                    if id==1:
                        pointC=[cx,cy,int(cz)]
                    if id==4:
                        pointgripA=[cx,cy,int(cz)]
                    if id==8:
                        pointgripB=[cx,cy,int(cz)]
                    if id==12:
                        pointextraB=[cx,cy,int(cz)]
                    
                    #print(pointA,pointB,pointC)
                    angle4=planeanglefinder(pointA,pointB,pointC)
                    #print(angle1,angle2,angle3,angle4)
                    if type(angle1) is list:
                        angle1=25
                    if type(angle2) is list:
                        angle2=120
                    if type(angle3) is list:
                        angle3=0
                    if type(angle4) is list:
                        angle4=0 

                    #anglesmoother(angleyolo,angle2,10)
                    finalangle5 = gripangle(pointgripA,pointgripB)
                    motion(5,finalangle5,finalangle5a)
                    #rotate(5,finalangle5)
                    motion(11,angle3,angle3a)
                    #rotate(11,angle3)
                    finalangle2=bruhh(angle2)
                    finalangle1=angle1-15
                    if finalangle1<=0:
                        finalangle1=0
                    #x=planeanglefinder2(pointA,pointextraB)
                    #tilt smoothening
                    #anglesmoother(angleyolo,x,3)
                    #angleyolo=x
                    finalangle4=tilt(pointgripA,pointextraB)
                    motion(3,finalangle4,finalangle4a)
                    #rotate(3,finalangle4)
                    #rotate(3,planeanglefinder2(pointA,pointC))
                    motion(10,finalangle2,finalangle2a)
                    #rotate(10,finalangle2)
                    motion(9,finalangle1+30,finalangle1a)
                    #rotate(9,finalangle1)

                    #print(finalangle1,finalangle2,angle3,angle4)

                    #rotate(7,angle4)


                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", cv2.flip(img, 1))
        cv2.waitKey(1)
    except Exception as e:
        print("EXCEPTION FKERR")
        pass
