import cv2
from gaze_tracking import GazeTracking
import imutils
from loss import losses
import numpy as np
import math

# from gaze_tracking import loss

loss = losses()

# losses = loss.losses()
gaze = GazeTracking()


list_x = []
list_y = []


def mean(l):
    sum = 0
    for i in l:
        sum += i
    return (sum/len(l))


def helper(frames, url):
    # print("url: " + url)
    cap = cv2.VideoCapture(url)
    focused = []
    j = 0
    print("ML starts")
    while(cap.isOpened()):
        # We get a new frame from the webcam
        i = 0
        ret, frame = cap.read()
        if(ret == True and j % frames == 0):
            frame = imutils.rotate(frame, 90)
            # _, frame = webcam.read()

            # We send this frame to GazeTracking to analyze it
            gaze.refresh(frame)

            frame = gaze.annotated_frame()
            text = ""

            if gaze.is_blinking():
                text = "Blinking"
            elif gaze.is_right():
                text = "Looking right"
            elif gaze.is_left():
                text = "Looking left"
            elif gaze.is_center():
                text = "Looking center"

            # cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 255, 0), 2)

            if(1):
                left_pupil = gaze.pupil_left_coords()
                right_pupil = gaze.pupil_right_coords()
                x_cords = gaze.x_cords()
                y_cords = gaze.y_cords()
                if(left_pupil == None):
                    left_pupil = (0, 0)
                if(right_pupil == None):
                    right_pupil = (0, 0)
                if(x_cords == None):
                    x_cords = (0, 0)
                if(y_cords == None):
                    y_cords = (0, 0)

                print(str(left_pupil), "\t", str(right_pupil),
                      "\t", str(x_cords), "\t", str(y_cords), "\n")

                left_l = loss.net_loss(
                    left_pupil, tuple((x_cords[0], y_cords[0])))
                right_l = loss.net_loss(
                    right_pupil, tuple((x_cords[1], y_cords[1])))
                focus = 1-(left_l+right_l)/2
                print(str(focus), "\n")
                focused.append(focus)
            else:
                continue
            
        else:
            pass

        j += 1

        # cv2.imshow("Demo", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or ret == False:
            break
    
    for i in range(len(focused)):
        if(focused[i] > 0.75):
            focused[i] = 1.00
        else:
            focused[i] = 0
        print(focused[i])
    # calculating the root mean square of all focus values  
    focused = np.array(focused)
    return np.sqrt((focused**2).mean())
