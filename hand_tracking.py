
import cv2
import mediapipe as mp
import time

class Hand_Detector():
    def __init__(self,mode=False,max_hands=2,detectioncon=0.5,trackingcon=0.5):
        self.mode=mode
        self.max_hands=max_hands
        self.detectioncon=detectioncon
        self.trackingcon=trackingcon
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.max_hands,self.detectioncon,self.trackingcon)
        self.mpDraw=mp.solutions.drawing_utils


    def find_hands(self,frame,Draw=True):
        frame_RGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(frame_RGB)
    
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
            
                self.mpDraw.draw_landmarks(frame,hand_landmarks,self.mpHands.HAND_CONNECTIONS)
        return frame
    
    def findposition(self,frame,hand_number=0,Draw=True):
        lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[hand_number]
            for id,lm in enumerate(myhand.landmark):
                h,w,c=frame.shape
                cx=int(lm.x*w)
                cy=int(lm.y*h)
                lmlist.append([id,cx,cy])
                if Draw:
                    cv2.circle(frame,(cx,cy),5,(255,0,255),-1)
        return lmlist





def main():
    ptime=0
    ctime=0
    cap=cv2.VideoCapture(0)
    detector=Hand_Detector()
    while True:
        ret,frame=cap.read()
        frame=detector.find_hands(frame)
        pos=detector.findposition(frame)
        if len(pos)!=0:
            print(pos[4])

        
        ctime=time.time()
        fps=int(1/(ctime-ptime))
        ptime=ctime
        cv2.putText(frame,str(fps),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),6)

        cv2.imshow('frame',frame)  

        if cv2.waitKey(5) & 0XFF==ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()


if __name__=='__main__':
    main()