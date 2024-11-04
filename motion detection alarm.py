import threading
import winsound
import cv2
import pyttsx3
import imutils

cap=cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
_, start_frame = cap.read()

start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0

# Video recording settings
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        winsound.Beep(2500, 1000)
        print ("Intruder Detected")
    alarm = False
    
while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5,5), 0)


        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > 100000:
            alarm_counter +=1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1
        cv2.imshow("cam", threshold)
    else:
        cv2.imshow("cam",frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.setProperty('rate', 150)
            engine.say("Intruder Detected")
            engine.runAndWait()
     # Record the frame to the video
    out.write(frame)
    
    key_pressed = cv2.waitKey(30)
    
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break
# Release the video writer and capture resources
out.release()
cap.release()
cv2.destroyAllWindows()
