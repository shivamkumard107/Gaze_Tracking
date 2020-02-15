import cv2
from gaze_tracking import GazeTracking
import pyrebase
#from gaze_tracking import loss

config = {
    "apiKey" : "AIzaSyB1OyBIvLggIAGWoCDjQK4PId9WJfXnREE",
    "authDomain": "mcandlefocus.firebaseapp.com",
    "databaseURL": "https://mcandlefocus.firebaseio.com",
    "projectId": "mcandlefocus",
    "storageBucket": "mcandlefocus.appspot.com",
    "messagingSenderId": "140073311865",
    "appId": "1:140073311865:web:12426f96cae1f3c88a7ea8",
    "measurementId": "G-H6DWEDR9Z7"
};

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

storage.child("images/new.mp4").download("video.mp4")

#losses = loss.losses()
gaze = GazeTracking()

# webcam = cv2.VideoCapture(0)

list_x = []
list_y = []

def mean(l):
	sum = 0
	for i in l:
		sum += i
	return int(sum/len(l))

def helper():
    cap = cv2.VideoCapture("video.mp4")
    while(cap.isOpened()):
        # We get a new frame from the webcam
        i = 0
        # _, frame = webcam.read()
        ret, frame = cap.read()

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

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 255, 0), 2)

        try:
            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()
            x_cords = gaze.x_cords()
            y_cords = gaze.y_cords()
        
            cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
            cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)

            #pupil_loss = tuple(losses.pupil_error(left_pupil), losses.pupil_error(right_pupil, 0))
        	#iris_loss = tuple(losses.iris_error(tuple(x_cords[0], y_cords[0])), losses.iris_error(tuple(x_cords[1], y_cords[1]), 0))
            #print(str(pupil_loss), "\t", str(iris_loss))
            print(str(left_pupil), "\t", str(right_pupil), "\t" ,str(x_cords), "\t", str(y_cords))

        except:
            continue

        """
        try:
            focus_x = (left_pupil[0] + right_pupil[0])/2
            focus_y = (left_pupil[1] + right_pupil[1])/2
            list_x.append(focus_x)
            list_y.append(focus_y)

            if focus_x > mean(list_x) - 30 and focus_x < mean(list_x) + 30:
                if focus_y > mean(list_y) - 20 and focus_y < mean(list_y) - 20:
                        print("Well Focused")
        except:
            pass
        """

        cv2.imshow("Demo", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

helper()
