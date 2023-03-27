#Import essentials
import cv2
import mediapipe as mp
import math
import numpy as np

#Create a class
class handDetector():
    def __init__(self, mode = False, maxHands = 1, complexity = 1, detectCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectCon = detectCon
        self.trackCon = trackCon

        #Get the hand data from mediapipe in order for the AI to know what a hand looks like
        self.handData = mp.solutions.hands
        self.hands = self.handData.Hands(self.mode, self.maxHands, self.complexity, self.detectCon, self.trackCon)
        self.draw = mp.solutions.drawing_utils

        #Get the ID data for how many fingers are up
        self.tipID = [4, 8, 12, 16, 20]

    def trackHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        #Compute the position of the hands
        self.result = self.hands.process(imgRGB)

        #Checks for multiple hands
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    #Draw the skeleton overlay on the hands
                    self.draw.draw_landmarks(img, handLms, self.handData.HAND_CONNECTIONS)
        return img
    
    def findPos(self, img, handNo = 0, draw = True, r = 8, marginErr = 50):
    #Create a list in order to keep track of the landmarks and coordinates
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        
        #Check for details about the hands
        if self.result.multi_hand_landmarks:
            hand = self.result.multi_hand_landmarks[handNo]
        
            for id, lm in enumerate(hand.landmark):
                #Convert floats to pixel values to accurately track the position of each landmark
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                #Draw extra dots on the landmarks for better visualization
                #if draw:
                    #cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)

            xMin, xMax = min(xList), max(xList)
            yMin, yMax = min(yList), max(yList)
            bbox = xMin, yMin, xMax, yMax

            if draw:
                cv2.rectangle(img, (xMin - marginErr, yMin - marginErr), (xMax + marginErr, yMax + marginErr), (0, 0, 255), 2)
        
        return self.lmList, bbox
    
    def fingerCount(self):
        #Define the finger with landmarks and check if they are open or closed
        finger = []

        #Fingers
        if len(self.lmList) != 0:
            #Thumb
            if self.lmList[self.tipID[0]][1] > self.lmList[self.tipID[0] - 1][1]:
                finger.append(1)
            else:
                finger.append(0)

            #Fingers
            for id in range(1,5):
                if self.lmList[self.tipID[id]][2] < self.lmList[self.tipID[id] - 2][2]:
                    finger.append(1)
                else:
                    finger.append(0)
        return finger

    def findDist(self, p1, p2, img, draw = True, r = 15, t = 3):
        #Get the x, y and center cooridnates of the fingertips
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        #Draw the connecting line
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), t)

            cv2.circle(img, (x1, y1), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        
        l = math.hypot(x2 - x1, y2 - y1)

        return l, img, [x1, y1, x2, y2, cx, cy]


def main():
    #Define the camera and set it's size
    camW, camH = 1080, 720

    cam = cv2.VideoCapture(0)
    cam.set(3, camW)
    cam.set(4, camH)

    #Reference the class
    detector = handDetector()
    
    while True:
        success, img = cam.read()
        img = detector.trackHands(img)

        #Find and print the position of landmarks
        lmList = detector.findPos(img)
        #if len(lmList) != 0:
            #print(lmList[8])

        #Flip the image
        img = cv2.flip(img, 1)

        #Display on the camera
        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) == ord("1"):
            break

if __name__ == "__main__":
    main()