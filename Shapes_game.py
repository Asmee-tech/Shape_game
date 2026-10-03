import cv2
import numpy as np
import time
import random

width=700
height=600
gametime=30
score=0
lives=3
shapes=["Circle","Square","Triangle"]
target=random.choice(shapes)
start=time.time()

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
        else:
            points=np.array([(x,y),(x-40,y+30),(x+40,y+30)],dtype=np.int32)
            cv2.fillPoly(img,[points],(255,0,255))
    return img

while True:
    elapsed=time.time()-start
    if elapsed>gametime:
        break
    screen=create_screen()
    cv2.putText(screen,f"Time:{int(elapsed)}",(600,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1)
    cv2.putText(screen,f"Score:{int(score)}",(500,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1)
    cv2.putText(screen,f"Lives:{int(lives)}",(400,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1)
    cv2.putText(screen,f"Target:{target}",(40,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1)

    if lives<=0:
        break
    cv2.imshow("Shape Hunter",screen)
    key=cv2.waitKey(30)
    if key==ord("q"):
        break