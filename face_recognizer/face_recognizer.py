import numpy as np
import glob
from person import Person
import os
import pdb
from algorithm import *

class FaceRecognizer:
    def __init__(self, gallery, algo, face_aligner):
        self.people = {}
        self.set_gallery(gallery)
        self.algo = algo(self.people, face_aligner)
    def set_gallery(self, gallery_folder):
        if gallery_folder[-1] == "/":
            gallery_folder = gallery_folder[:-1]
        for num, folder in enumerate(glob.glob(gallery_folder + "/*/")):
            print(folder)
            self.set_person(folder, num)
    def set_person(self, folder, num):
        name = folder.split("/")[-2]
        try:
            person = Person(name, folder, num)
        except AssertionError:
            print("WARNING: {}'s face not found in gallery".format(name))
        print(name)
        self.people[name] = person
    def recognize(self, photo):
        print("Start Recognizing...")
        faces_detected = self.algo.recognize(photo)
        return faces_detected


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="gallery location")
    parser.add_argument("-a", default="opencv", help="use which package")
    parser.add_argument("-i", default="~/gallery/zhongyi/1.jpg", help="photo to be recognized")
    args = parser.parse_args()
    print("initializing face recognizer...")
    if args.a == "dlib":
        import face_recognition
        algo = DlibAlgorithm
        photo = face_recognition.load_image_file(args.i)
    elif args.a == "opencv":
        import cv2
        algo = OpenCVAlgorithm
        photo = cv2.imread(args.i, cv2.IMREAD_GRAYSCALE)
    recognizer = face_recognizer(args.g, algo)
    a = recognizer.recognize(photo)
    print(a)
