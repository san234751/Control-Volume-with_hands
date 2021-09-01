import cv2
import time
import mediapipe as mp
class hand_detect():
    def __init__(self,mode=False,maxhand=2,min_detection_confidence=0.5,min_tracking_confidence=0.5):
        self.mode=mode
        self.maxHands=maxhand
        self.detectionCon=min_detection_confidence
        self.trackCon=min_tracking_confidence
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands=self.mp_hands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.positions=[4,8,12,16,20]
    def findHands(self,frame,draw=True):
        framergb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(framergb)
        if self.result.multi_hand_landmarks:
            if draw:
                for hand_landmarks in self.result.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame,hand_landmarks,self.mp_hands.HAND_CONNECTIONS)
        return frame
    def findPosition(self,frame,handno=0,draw=True):
        self.lmlist=[]
        if self.result.multi_hand_landmarks:
            myhand=self.result.multi_hand_landmarks[handno]
            for id,lm in enumerate(myhand.landmark):
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),10,(255,0,255),cv2.FILLED)
        return self.lmlist
    def countfinger(self):
        finger=[]
        if self.lmlist[self.positions[0]][1]>self.lmlist[self.positions[0]-1][1]:
            finger.append(1)
        else:
            finger.append(0)
        for id in range(1,5):
            if self.lmlist[self.positions[id]][2]<self.lmlist[self.positions[id]-2][2]:
                finger.append(1)
            else:
                finger.append(0)
        return finger
def main():
    video=cv2.VideoCapture(0)
    past=0
    detector=hand_detect()
    while True:
        suc,frame=video.read()
        frame=detector.findHands(frame)
        curr=time.time()
        rate=1/(curr-past)
        past=curr
        cv2.putText(frame,f'Frame: {int(rate)}',(20,40),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
        cv2.imshow("Camera",frame)
        cv2.waitKey(1)

if __name__=="__main__":
    main()