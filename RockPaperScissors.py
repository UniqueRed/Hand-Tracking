#Import essentials
import cv2
import HandTrackingModule as htm

#Define the camera and its size
camW, camH = 1080, 720

cam = cv2.VideoCapture(0)
cam.set(3, camW)
cam.set(4, camH)

#Reference the detector
detector = htm.handDetector()

#Get the id for the tips
tipID = [4, 8, 12, 16, 20]

while True:
    success, img = cam.read()
    
    #Track the hands and get the landmarks
    img = detector.trackHands(img)
    lmList, bbox = detector.findPos(img)

    #Define the finger with landmarks and check if they are open or closed
    finger = []

    #Fingers
    if len(lmList) != 0:
        #Thumb
        if lmList[tipID[0]][2] < lmList[tipID[0] - 1][2]:
            finger.append(1)
        else:
            finger.append(0)

        #Fingers
        for id in range(1,5):
            if lmList[tipID[id]][1] < lmList[tipID[id] - 2][1]:
                finger.append(0)
            else:
                finger.append(1)
        
        #Check to see if all fingers are closed
        if finger[0] == 0 and finger[1] == 0 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:
            print("Rock")
        
        #Check to see if all fingers are open
        if finger[0] == 1 and finger[1] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1:
            print("Paper")
        
        #Check to see if the pointer and middle finger is open and the rest are closed
        if finger[0] == 0 and finger[1] == 0 and finger[2] == 1 and finger[3] == 0 and finger[4] == 0:
            print("Scissors")
    
    cv2.imshow("Rock Paper Scissors", img)
    if cv2.waitKey(1) == ord("q"):
        break