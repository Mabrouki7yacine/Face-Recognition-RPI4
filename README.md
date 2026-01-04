# Raspberry Pi Face Recognition Access System

This project is a real-time face recognition system built for Raspberry Pi using the official camera module.  
It captures images, extracts face encodings, stores known faces, and continuously scans for matches.  
Based on the result, it triggers GPIO outputs to control LEDs (or any other connected hardware) and optionally sends the detected name to a local server.

The goal of the project is to work as a lightweight **access authorization layer** — a person stands near the device, the IR proximity sensor activates the camera, and the system decides whether the face is recognized or not.

## How it works

1. The Pi camera captures a frame when the proximity sensor detects someone nearby.
2. The frame is processed using `face_recognition` to locate faces and extract encodings.
3. Extracted encodings are compared against stored known face data.
4. If a match is found, the system marks the person as **authorized** and turns on the green LED.
5. If no match is found, the person is treated as **unauthorized** and the red LED turns on.
6. The detected name and current time can be sent to a local API for logging.

## Project components

| File | Purpose |
|------|--------|
| `take_pic.py` | Opens camera preview and saves a photo with a person’s name as filename |
| `encoded_faces.py` | Reads saved face images, extracts encodings, and stores them in `my_faces.txt` |
| `face_detection.py` | Runs face recognition loop using PiCamera and IR proximity sensor |
| `my_faces.txt` | Database file containing face encodings and associated names |
| `RPi.GPIO` integration | Controls LEDs or other hardware depending on recognition result |

## Setup

After installing **Raspbian OS** and installing the camera driver  
(forget how I managed to do that — I’ll update this as soon as I remember)

Then run:

```bash
sudo apt update
sudo apt install python3-opencv python3-picamera2 #not sure this will work from first try for you
pip3 install face_recognition numpy requests
