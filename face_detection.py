import cv2 
import face_recognition
import ast
import time
from picamera2 import Picamera2
import numpy as np
import RPi.GPIO as GPIO
import requests
from datetime import datetime

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
red = 26    # Unauthorized
green = 16  # Authorized
sensor_pin = 17 # IR sensor to detect proximity

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(sensor_pin, GPIO.IN)

# Load known faces from file
with open("my_faces.txt", "r") as f:
    content = f.read()
try:
    my_faces = ast.literal_eval(content)
except (SyntaxError, ValueError) as e:
    print(f"Error parsing the file: {e}")
    my_faces = []

def rescale_frame(frame, scale=1.0):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

def run_face_recognition_picamera():
    print("Starting face recognition with PiCamera every 1.5 seconds...")

    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888'}))
    picam2.start()

    last_time = time.time()
    detection_time = None
    last_post_time = 0  # Track the last time a POST was sent

    while True:
        now = time.time()

        # Turn off LEDs if 3 seconds have passed since last detection
        if detection_time and (now - detection_time >= 3):
            GPIO.output(red, False)
            GPIO.output(green, False)
            detection_time = None

        if (now - last_time) >= 1.5 and GPIO.input(sensor_pin) == GPIO.LOW:
            frame = picam2.capture_array()
            frame = frame[:, :, :3]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = rescale_frame(frame, 1.0)

            try:
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)

                for (top, right, bottom, left), unknown_encoding in zip(face_locations, face_encodings):
                    name = "Unknown"
                    for face_data in my_faces:
                        result = face_recognition.compare_faces([face_data['encodings']], unknown_encoding)
                        if result[0]:
                            name = face_data['name']
                            break

                    print(f"Detected: {name}")
                    detection_time = now  # Start/reset timer

                    # Only send POST if 3 seconds have passed since the last one
                    if now - last_post_time >= 3:
                        detected_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        payload = {"name": name, "time": detected_time_str}
                        try:
                            response = requests.post("http://192.168.161.106:3000/data/person", json=payload)
                            print("Posted detection:", payload, "Response status:", response.status_code)
                            last_post_time = now  # Update post time
                        except Exception as post_err:
                            print("Error posting detection info:", post_err)

                    # Control LEDs based on detection result
                    if name == 'Unknown':
                        GPIO.output(red, True)
                        GPIO.output(green, False)
                    else:
                        GPIO.output(red, False)
                        GPIO.output(green, True)

            except Exception as e:
                print(f"Error in face recognition: {e}")

            last_time = now

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    GPIO.output(red, False)
    GPIO.output(green, False)
    GPIO.cleanup()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run_face_recognition_picamera()
