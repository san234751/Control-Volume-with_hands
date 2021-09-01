import cv2
import hand_detection_module
import time
import math
import numpy as np
from subprocess import call
video=cv2.VideoCapture(0)
past=0
detector=hand_detection_module.hand_detect(min_detection_confidence=0.75)
firstvol=100
while True:
    suc,frame=video.read()
    frame=detector.findHands(frame)
    lmlist=detector.findPosition(frame,draw=False)
    if len(lmlist)!=0:
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(frame,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(frame,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.circle(frame,(cx,cy),15,(255,0,255),cv2.FILLED)
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,255),3)
        length=math.hypot(x2-x1,y2-y1)
        vol=int(np.interp(length,[50,300],[0,100]))
        if vol<firstvol:
            ans=str(firstvol-vol)+"%-"
            call(["amixer", "-D", "pulse", "sset", "Master", ans])
        else:
            volnew=str(vol-firstvol)+"%+"
            call(["amixer", "-D", "pulse", "sset", "Master", volnew])
        firstvol=vol
        if length<50:
            cv2.circle(frame,(cx,cy),15,(0,255,0),cv2.FILLED)
    curr=time.time()
    rate=1/(curr-past)
    past=curr
    cv2.putText(frame,f'Frame: {int(rate)}',(20,40),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
    cv2.imshow("Camera",frame)
    cv2.waitKey(1)