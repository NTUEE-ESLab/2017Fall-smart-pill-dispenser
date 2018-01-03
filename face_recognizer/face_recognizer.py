import face_recognition
import picamera
import numpy as np
import glob
from person import Person
import os
import pdb

class face_recognizer:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (320, 240)
        output = np.empty((240, 320, 3), dtype=np.uint8)
        self.people = []
    def set_gallery(self, gallery_folder):
        if gallery_folder[-1] == "/":
            gallery_folder = gallery_folder[:-1]
        for folder in glob.glob(gallery_folder + "/*/"):
            self.set_person(folder)
    def set_person(self, folder):
        name = os.path.basename(folder)
        try:
            person = Person(name, folder)
        except AssertionError:
            print("WARNING: {}'s face not found in gallery".format(name))
        self.people.append(person)
    def recognize(self):
        print("Start Recognizing...")
        output = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(output, format="rgb")
        face_locations = face_recognition.face_locations(output)
        print("Found {} faces in image.".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(output, face_locations)
        faces_detected = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces([person.face_encoding for person in self.people], face_encoding)

            for i, match in enumerate(matches):
                if match:
                    name = people[i].name
                    faces_detected.append(name)
                    print("I see someone named {}!".format(name))
        return faces_detected

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gallery", help="gallery location")
    args = parser.parse_args()
    print("initializing face recognizer...")
    pdb.set_trace()
    recognizer = face_recognizer()
    print("setting gallery")
    recognizer.set_gallery(args.gallery)
    while True:
        recognizer.recognize()
        print("Sleep for 2s")
        sleep(2)
