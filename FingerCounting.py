import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

folderPath = "FingerImages"
mylist = os.listdir(folderPath)
# print(mylist)
overlayList = []
for imPath in mylist:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))
pTime=0

detector = htm.handDetector(detectionCon=0.75)
tipIds = [4,8,12,16,20]

while True:
    sucess, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    # print(lmList)
    if len(lmList) != 0:
        fingers = []

        #Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            # print("index finger open")
            fingers.append(1)
        else:
            fingers.append(0)

        #4 Fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                # print("index finger open")
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
            totalFingers = fingers.count(1)
            # print(totalFingers)
            h, w, c = overlayList[totalFingers-1].shape
            img[0:h, 0:w] = overlayList[totalFingers-1]

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(540,60),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)