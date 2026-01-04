import cv2
import os
import face_recognition

def load_images_from_folder(folder):
    images = []
    persons = []
    for filename in os.listdir(folder):
        person = {'name': None, 'encodings': None}
        img = cv2.imread(os.path.join(folder, filename))
        name = filename.replace(".jpg", "")
        print(name)
        if img is not None:
            face_encodings = face_recognition.face_encodings(img)
            if len(face_encodings) == 0:
                print("No face found in the known image.")
                exit()
            else:
                face_encoding = face_encodings[0].tolist()
                person = {'name': name, 'encodings': face_encoding}
                persons.append(person)

    # Write the actual content of persons to the file
    with open('my_faces.txt', 'w') as f:
        f.write(f"{repr(persons)}\n")

    return persons

my_people = load_images_from_folder("faces/")

