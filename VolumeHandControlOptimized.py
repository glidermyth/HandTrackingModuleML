import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam = 640
hCam = 480
pTime = 0
volBar = 400
volPer = 0
area = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]



cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

while True:
    success, img = cap.read()

    img = detector.findHands(img)

    lmList, bbox = detector.findPosition(img, draw = True)
    if len(lmList) != 0:

        area = (bbox[2]-bbox[0]) * (bbox[3] - bbox[1]) //100
        # print(area)
        if 250<area<1000:

            length, img, lineInfo = detector.findDistance(4,8,img)
            print(length)
            #Hand Range: 50 - 300
            #Volume Range: -65 - 0

            volBar = np.interp(length, [50,300], [400,150])
            volPer = np.interp(length, [50,300], [0,100])
            # print(vol)
            # volume.SetMasterVolumeLevel(vol, None)

            #Reduce the resolution to make it smoother
            smoothness = 2
            volPer = smoothness * round(volPer/smoothness)

            #if pinky finger is down set volume
            fingers = detector.fingersUp()
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)

            if length<50:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0,255,0), cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(255,0,0),2)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)

    #frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS:{int(fps)}',(40,70),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),2)
    cv2.imshow("Image",img)
    cv2.waitKey(1)