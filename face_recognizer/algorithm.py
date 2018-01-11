from person import Person
import sys
import numpy as np
from face_aligner import FaceAligner

class Algorithm:
    def __init__(self, gallery):
        pass
    def recognize(self, photo):
        pass

class DlibAlgorithm(Algorithm):
    def __init__(self, people):
        import face_recognition
        self.people = people
        if sys.version_info[0] == 2:
            items = self.people.iteritems()
        else:
            items = self.people.items()
        for name, person in items:
            person_face_encodings = []
            for image_file in person.image_files:
                image = face_recognition.load_image_file(image_file)
                face_encoding = self.get_face_encodings(image)[0]
                person_face_encodings.append(face_encoding)
            person_face_encoding = sum(person_face_encodings) / len(person_face_encodings)
            self.people[name].face_encoding = person_face_encoding
    def get_face_encodings(self, image):
        import face_recognition
        face_locations = face_recognition.face_locations(image)
        assert len(face_locations) > 0, "WARNING: no faces found in the whole folder {}".format(images_folder)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        return face_encodings

    def recognize(self, photo):
        import face_recognition
        face_encodings = self.get_face_encodings(photo)
        faces_detected = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            gallery = [[name, person.face_encoding] for name, person in self.people.items()]
            matches = face_recognition.compare_faces([i[1] for i in gallery], face_encoding)

            for i, match in enumerate(matches):
                if match:
                    name = gallery[i][0]
                    faces_detected.append(name)
                    print("I see someone named {}!".format(name))
        return faces_detected

class OpenCVAlgorithm(Algorithm):
    def __init__(self, people, face_aligner):
        import cv2
        self.people = people
        self.model = cv2.face.EigenFaceRecognizer_create()
        self.size = (300, 300)
        self.face_aligner = face_aligner
        if len(self.people) > 0:
            self.train()

    def get_face(self, image):
        cropped = self.face_aligner.align(image)
        return cropped

    def train(self):
        X, y = [], []
        for name, person in self.people.items():
            for image_file in person.image_files:
                image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
                face = self.get_face(image)
                if face is None:
                    continue
                X.append(face)
                y.append(person.num)
        y = np.asarray(y, dtype=np.int32)
        self.model.train(np.asarray(X), np.asarray(y))

    def recognize(self, image):
        face = self.get_face(image)
        [p_label, p_confidence] = self.model.predict(face)
        for person in self.people:
            if person.num == p_label:
                return person.name
