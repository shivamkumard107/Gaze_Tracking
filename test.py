import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

list_x = []
list_y = []

def mean(l):
	sum = 0
	for i in l:
		sum += i
	return int(sum/len(l))		

while True:
    # We get a new frame from the webcam
    i = 0
    _, frame = webcam.read()

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

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
    print(str(left_pupil), "\t", str(right_pupil))

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
    

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
         break
