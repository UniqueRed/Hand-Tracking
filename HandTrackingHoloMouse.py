#Import essentials
import cv2
import HandTrackingModule as htm
import numpy as np
import pyautogui as pyag
#from pynput.mouse import Button, Controller

#pyag = Controller()

#Define the camera and set it's size
camW, camH = 1080, 720

cam = cv2.VideoCapture(0)
cam.set(3, camW)
cam.set(4, camH)

#Get screen size for mapping
scrW, scrH = 1920, 1080
fr = 200

#Smoothening
smooth = 2

pLocX, pLocY = 0, 0
cLocX, xLocY = 0, 0

#Scroll speed
scrSpeed = 50

#Reference the detector
detector = htm.handDetector()

while True:
    success, img = cam.read()
    img = detector.trackHands(img)
    lmList, bbox = detector.findPos(img)

    if len(lmList) != 0:
        #Get the x and y coordinates of the pointer and middle fingertips
        x1, y1 = lmList[9][1:]
        x2, y2 = lmList[12][1:]

        #Check which fingers are up or down
        finger = detector.fingerCount()

        #Create a mapping range
        cv2.rectangle(img, (fr, fr), (camW - fr, camH - fr), (0, 0, 255), 2)

        #MOVE MOUSE

        #Check if the pointer is up and the middle finger is down
        if finger[1] == 1: #and finger[2] == 0:
            #Convert coordinates to screen
            x3 = np.interp(x1, (fr, camW - fr), (0, scrW))
            y3 = np.interp(y1, (fr, camH - fr), (0, scrH))

            #Smoothening
            cLocX = pLocX + (x3 - pLocX) / smooth
            cLocY = pLocY + (y3 - pLocY) / smooth

            #Move the mouse
            pyag.moveTo(scrW - cLocX, cLocY)

            #Show that you are in movement mode
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)

            #Reset current and previous locations
            pLocX, pLocY = cLocX, cLocY

        #LEFT CLICK
        
        #Check to see if pointer and middle finger is up
        if finger[0] == 1 and finger[1] == 1:
            #Find the distance between the given fingers
            l, img, lineInfo = detector.findDist(4, 8, img)

            #Check to see if the distance between the 2 points is less than a certain value
            if l < 15:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 255, 0), cv2.FILLED)
                pyag.click()

        #RIGHT CLICK
        
        #Check to see if pointer, middle, and ring finger is up and pinky is down
        if finger[0] == 1 and finger[2] == 1:
            #Find the distance between the given fingers
            l, img, lineInfo = detector.findDist(4, 12, img)

            #Check to see if the distance between the 2 points is less than a certain value
            if l < 15:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 255, 0), cv2.FILLED)
                pyag.rightClick()

        #DOUBLE CLICK
        
        #Check to see if pointer, middle, ring finger, and pinky is up
        if finger[1] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1:
            #Find the distance between the given fingers
            l, img, lineInfo = detector.findDist(8, 12, img)

            #Check to see if the distance between the 2 points is less than a certain value
            if l < 25:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 255, 0), cv2.FILLED)
                pyag.doubleClick()

        if finger[1] == 1 and finger[4] == 1:
            pyag.drag()

        #SCROLL

        #UP
        
        #Check to see if thumb, pointer, and ring finger is down and pinky finger is up
        if finger[0] == 0 and finger[1] == 0 and finger[4] == 1 and finger[3] == 0:
            pyag.scroll(scrSpeed)

        #DOWN

        #Check to see if thumb and pinky is up and ring finger is down
        if finger[0] == 1 and finger[1] == 0 and finger[4] == 1 and finger[3] == 0:
            pyag.scroll(-scrSpeed)

    #Flip the image
    img = cv2.flip(img, 1)

    #Display on the camera
    cv2.imshow("Holo Mouse Tracker", img)
    if cv2.waitKey(1) == ord("q"):
        break