import cv2
import serial
import time
from flask import Flask, render_template, Response, request, redirect, url_for
data='open'
read="___"

data='open'
arduino = serial.Serial('COM10',9600)
cap=cv2.VideoCapture(0)
print("connected camera")
def sendmessage():
    count=0
    global read
    while (count<1):
        arduino.write(data.encode())
        print ("Send message")
        read=str(arduino.readline())
        print(read)
        time.sleep(1)
        count=count+1
    count=0
def encode_string():
    global read
    point1=0
    if read != "___":
        for i in read:
            if read[i]=="*":
                point1=i

app = Flask(__name__)
def gen_frames():
    while True:
        success,frame=cap.read()
        font = cv2.FONT_HERSHEY_COMPLEX
        if read!="___":
            print("print teleometry")
            cv2.putText(frame, read, (10, 50), font, 2, color=(0, 255, 255), thickness=2)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update_telemetry')
def update_telemetry():
    sendmessage()
    return ("nothing")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
