import cv2
from gaze_tracking import GazeTracking
import pyrebase
import imutils
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from loss import losses
import math

# from gaze_tracking import loss

loss = losses()

config = {
    "apiKey": "AIzaSyB1OyBIvLggIAGWoCDjQK4PId9WJfXnREE",
    "authDomain": "mcandlefocus.firebaseapp.com",
    "databaseURL": "https://mcandlefocus.firebaseio.com",
    "projectId": "mcandlefocus",
    "storageBucket": "mcandlefocus.appspot.com",
    "messagingSenderId": "140073311865",
    "appId": "1:140073311865:web:12426f96cae1f3c88a7ea8",
    "measurementId": "G-H6DWEDR9Z7"
}


ref = db.reference('/coordinates')

ref.set({
    'eye':
        {
            'left': {
                'x': {},
                'y': {}
            },
            'right': {
                'x': {},
                'y': {}
            }
        },
    'pupil':
        {
            'left': {
                'x': {},
                'y': {}
            },
            'right': {
                'x': {},
                'y': {}
            }
        }
})

eye_ref_l = ref.child('eye/left')
pupil_ref_l = ref.child('pupil/left')
eye_ref_r = ref.child('eye/right')
pupil_ref_r = ref.child('pupil/right')
focus_ref = ref.child('focussed/')

# firebase = pyrebase.initialize_app(config)


# losses = loss.losses()
gaze = GazeTracking()

# webcam = cv2.VideoCapture(0)

list_x = []
list_y = []


def mean(l):
    sum = 0
    for i in l:
        sum += i
    return int(sum/len(l))


def helper(frames, url):
    # print("url: " + url)
    cap = cv2.VideoCapture(url)
    focussed = []
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
                focussed.append(focus)
            else:
                continue
            # upload to firebase database
            # eye_ref_l.push({'x':int(left_pupil[0]), 'y':int(left_pupil[1])})
            # eye_ref_r.push({'x':int(right_pupil[0]), 'y':int(right_pupil[1])})
            # pupil_ref_l.push({'x':str(x_cords[0]), 'y':str(y_cords[0])})
            # pupil_ref_r.push({'x':str(x_cords[1]), 'y':str(y_cords[1])})
            # focus_ref.push({'focus':str(1-(left_l+right_l)/2)})
        else:
            pass

        j += 1

        # cv2.imshow("Demo", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or ret == False:
            break
        # calculating the root mean square of all focus values
        mean_focus = 0
        for i in focussed:
            mean_focus = mean_focus + i**2
        if(len(focussed) == 0):
            root_mean_focus = 0
        else:
            root_mean_focus = mean_focus/len(focussed)
        root_mean_focus = (math.sqrt(mean_focus))
        
    return root_mean_focus
