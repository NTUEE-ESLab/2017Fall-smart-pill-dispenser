from person import Person
import sys
import numpy as np
import pdb

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
            pdb.set_trace()
            gallery = [[name, person.face_encoding] for name, person in self.people.items()]
            matches = face_recognition.compare_faces([i[1] for i in gallery], face_encoding)

            for i, match in enumerate(matches):
                if match:
                    name = gallery[i][0]
                    faces_detected.append(name)
                    print("I see someone named {}!".format(name))
        return faces_detected

class OpenCVAlgorithm(Algorithm):
    def __init__(self, people):
        import cv2
        self.people = people
        self.model = cv2.createEigenFaceRecognizer()
        self.size = (300, 300)
        X, y = [], []
        for name, person in self.people.iteritems():
            for image_file in person.image_files:
                image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
                face = self.get_face(image)
                if face is None:
                    continue
                X.append(face)
                y.append(person.num)
        y = np.asarray(y, dtype=np.int32)
        self.model.train(np.asarray(X), np.asarray(y))
    def get_face(self, image): 
        import cv2
        import cv
        cascade_path = "/home/pc204/opencv-2.4.13/data/haarcascades/haarcascade_frontalface_alt.xml"
        cascade = cv2.CascadeClassifier(cascade_path)
        def crop(img):
            rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
            if len(rects) == 0:
                print("Warning: no face detected")
                return None
            x, y, h, w = rects[0]
            face = img[y:y+h, x:x+w]
            return face
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face = crop(image)
        if face is None:
            return None
        face = cv2.resize(face, self.size)
        face = np.asarray(image, dtype=np.uint8)
        return face

    def recognize(self, image):
        face = self.get_face(image)
        [p_label, p_confidence] = self.model.predict(face)
        for person in self.people:
            if person.num == p_label:
                return person.name
