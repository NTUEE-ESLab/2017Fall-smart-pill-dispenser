import face_recognition
import glob
import os

class Person:
    def __init__(self, name, images_folder):
        self.name = name
        self.images_folder = images_folder
        image_formats = ["jpg", "png"]
        image_files = []
        for image_format in image_formats:
            image_files += glob.glob(os.path.join(images_folder, "*.{}".format(image_format)))
        face_encodings = []
        for image_file in image_files:
            image = face_recognition.load_image_file(image_file)
            face_locations = face_recognition.face_locations(image)
            assert len(face_locations) > 0, "WARNING: no faces found in the whole folder {}".format(images_folder)
            _face_encodings = face_recognition.face_encodings(image, [face_locations[0]])
            face_encodings.append(_face_encodings[0])
        self.face_encoding = sum(face_encodings) / len(face_encodings)

            
