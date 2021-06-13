import cv2
import numpy as np
import time
import math
from hand_tracking import Hand_Detector
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
cap=cv2.VideoCapture(0)
wcam,hcam=640,480
cap.set(3,wcam)
cap.set(4,hcam)
detector=Hand_Detector()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
ptime=0
volRange=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0.0, None)
#print(volRange)
minval=volRange[0]
maxval=volRange[1]
vol=0
volbar=400
volper=0
brightness=0
h=2
while True:
    ret,frame=cap.read()
    frame=detector.find_hands(frame)
    lmlist=detector.findposition(frame,Draw=False)
    if len(lmlist)!=0:
        x0,y0=lmlist[0][1],lmlist[0][2]
        #print(lmlist[4],lmlist[8])
        x,y=lmlist[4][1],lmlist[4][2]
        x1,y1=lmlist[8][1],lmlist[8][2]
        if x>x0:
            h=1
            print('Right Hand')
        elif x<x0:
            h=0
            print('Left Hand')
        cx,cy=(x+x1)//2,(y+y1)//2
        cv2.circle(frame,(x,y),5,(255,0,255),-1)
        cv2.circle(frame, (x1, y1), 5, (255, 0, 255), -1)
        cv2.line(frame,(x,y),(x1,y1),(255,0,255),3)
        cv2.circle(frame, (cx, cy), 10, (255, 0, 255), -1)
        length=math.hypot((x1-x),(y1-y))
        
        
        if h==1:
            vol=np.interp(length,[25,225],[-62.5,0])
            print(f'Volume = {int(100+vol)}')
            #volbar=np.interp(length,[25,200],[400,150])
            volper=np.interp(length,[25,200],[0,100])
            volume.SetMasterVolumeLevel(vol, None)
        elif h==0:
            brightness=int(100+(np.interp(length,[25,225],[-62.5,0])))
            print(f'Brightness = {brightness}')
            sbc.set_brightness(brightness)

        if length<25:
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)


    #cv2.rectangle(frame, (50, 150), (85, 400), (0, 0, 255), 3)
    #cv2.rectangle(frame, (50, int(volbar)), (85, 400), (0, 0, 255), -1)
    text_vol=f"Volume = {int(volper)} %"
    text_brightness=f"Brightness = {brightness} %"
    cv2.putText(frame, text_vol, (50, 430), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, text_brightness, (50, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    ctime=time.time()
    fps=int(1/(ctime-ptime))
    ptime=ctime
    text=f"FPS :{fps}"
    cv2.putText(frame,text,(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    cv2.imshow('frame', frame)

    if cv2.waitKey(5) & 0XFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
