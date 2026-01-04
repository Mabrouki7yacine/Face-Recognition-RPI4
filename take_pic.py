import cv2
import os
from picamera2 import Picamera2
import re

output_folder = "faces/"
os.makedirs(output_folder, exist_ok=True)

cv2.startWindowThread()
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888'}))
picam2.start()

print("Press 'q' to quit, 's' to save image")

def clean_name(name):
    name = re.sub(r'[^a-zA-Z0-9_\- ]', '', name)
    name = name.strip().replace(" ", "_")
    return name if name else "unknown"

while True:
    image = picam2.capture_array()
    cv2.imshow("Camera", image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        person_name = input("Enter person name: ")
        person_name = clean_name(person_name)

        filename = os.path.join(output_folder, f"{person_name}.jpg")
        cv2.imwrite(filename, image)
        print(f"Saved: {filename}")

    elif key == ord('q'):
        break

cv2.destroyAllWindows()

