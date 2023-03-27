#Import essentials
import cv2
import mediapipe as mp

#Define the camera
cam = cv2.VideoCapture(0)

#Get the hand data from mediapipe in order for the AI to know what a hand looks like
handData = mp.solutions.hands
hands = handData.Hands(max_num_hands = 2)
draw = mp.solutions.drawing_utils

#Start a while loop in order to keep the image running along with the skeletal overlay
while True:
    success, img = cam.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    #Compute the position of the hands
    result = hands.process(imgRGB)
    #print(result.multi_hand_landmarks)

    #Checks for multiple hands
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id, lm)
                #Convert floats to pixel values to accurately track the position of each landmark
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, ":", cx, cy)

                #Detect certain landmarks and identify them with different colors

                #Wrist
                if id == 0:
                    cv2.circle(img, (cx, cy), 10, (255, 255, 0), cv2.FILLED)
                if id == 1:
                    cv2.circle(img, (cx, cy), 10, (255, 255, 0), cv2.FILLED)

                #Knuckle
                if id == 2:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                if id == 5:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                if id == 9:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                if id == 13:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                if id == 17:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

                #Joint 1
                if id == 3:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                if id == 6:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                if id == 10:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                if id == 14:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                if id == 18:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

                #Joint 2
                if id == 3:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)
                if id == 7:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)
                if id == 11:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)
                if id == 15:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)
                if id == 19:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)

                #Fingertips
                if id == 4:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                if id == 8:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                if id == 12:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                if id == 16:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                if id == 20:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

            #Draw the skeleton overlay on the hands
            draw.draw_landmarks(img, handLms, handData.HAND_CONNECTIONS)

    #Flip the image
    img = cv2.flip(img, 1)
    
    #Display on the camera
    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) == ord("q"):
        break