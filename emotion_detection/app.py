from flask import Flask, render_template, Response, jsonify
import cv2
from deepface import DeepFace

app = Flask(__name__)

video_capture = None
emotion = ""

def detect_emotion(frame):
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except Exception as e:
        print("Error during emotion detection:", e)
        return None

def generate_frames():
    global video_capture, emotion
    while True:
        success, frame = video_capture.read()
        if not success:
            break

        emotion = detect_emotion(frame)
        cv2.putText(frame, f'Emotion: {emotion}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/meeting')
def meeting():
    global video_capture
    video_capture = cv2.VideoCapture(0)  
    return render_template('meeting.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_emotion')
def get_emotion():
    return jsonify({'emotion': emotion})

@app.route('/leave', methods=['POST'])
def leave():
    global video_capture
    if video_capture is not None and video_capture.isOpened():
        video_capture.release()
        video_capture = None
    return "Left Meeting"

if __name__ == '__main__':
    app.run(debug=True)
