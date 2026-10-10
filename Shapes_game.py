import cv2
import numpy as np
import time
import random

width=700
height=600
gametime=30
score=0
lives=3
shapes=["Circle","Square","Triangle","Rectangle"]
target=random.choice(shapes)
start=time.time()
game=True
mousex=0
mousey=0
clicked=False

def create_screen():
    img=np.ones((height,width,3),dtype=np.uint8)*255
    for i in range(15):
        shape=random.choice(shapes)
        x=random.randint(100,width-50)
        y=random.randint(100,height-50)
        if shape=="Circle":
            cv2.circle(img,(x,y),30,(255,0,255),-1)
        elif shape=="Square":
            cv2.rectangle(img,(x,y),(x+50,y+50),(255,0,255),-1)
        elif shape=="Rectangle":
            cv2.rectangle(img,(x,y),(x+80,y+50),(255,0,255),-1)
        else:
            points=np.array([(x,y),(x-40,y+30),(x+40,y+30)],dtype=np.int32)
            cv2.fillPoly(img,[points],(255,0,255))
    return img

def detect_shapes(image):   
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _,threshold=cv2.threshold(gray,100,255,cv2.THRESH_BINARY_INV)
    contours,_=cv2.findContours(
        threshold,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)
    detected=[]
    for contour in contours:
        area=cv2.contourArea(contour)
        if area<500:
            continue
        perimeter=cv2.arcLength(
            contour,
            True)
        corners=cv2.approxPolyDP(
            contour,
            0.04*perimeter,
            True)
        if len(corners)==3:
            name="Triangle"
        elif len(corners)==4:
            name="Square"
        else:
            name="Circle"
        detected.append({
        "name":name,
        "contour":contour})
    return detected
def mouse_click(event,x,y,flags,param):
    global mousex,mousey,clicked
    if event==cv2.EVENT_LBUTTONDOWN:
        mousex=x
        mousey=y
        clicked=True
        
screen=create_screen()
cv2.namedWindow("Shape Hunter")
cv2.setMouseCallback("Shape Hunter",mouse_click)

while game:
    elapsed=time.time()-start
    if elapsed>gametime:
        game=False
    if clicked==True:
        # detecting shape
        detected_shapes=detect_shapes(screen)
        print(detect_shapes)
        # checking if the detected shape is correct
        # moving to next round
        target=random.choice(shapes)
        screen=create_screen()
        clicked=False
        if lives<=0:
            game=False
    cv2.rectangle(screen,(0,0),(700,50),(255,255,255),-1)
    cv2.putText(screen,f"Time:{int(elapsed)}",(600,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1)
    cv2.putText(screen,f"Score:{int(score)}",(500,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1)
    cv2.putText(screen,f"Lives:{int(lives)}",(400,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1)
    cv2.putText(screen,f"Target:{target}",(40,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1)

    cv2.imshow("Shape Hunter",screen)
    key=cv2.waitKey(30)
    if key==ord("q"):
        break
