import io
import numpy as np
import json
import cv2
from collections import Counter

class RecognizeHandler:
    def __init__(self, gallery_path, face_aligner, face_recognizer, interval=3):
        self.gallery_path = gallery_path
        self.face_aligner = face_aligner
        self.face_recognizer = face_recognizer
        self.interval = interval
    def recognize(self, image):
        aligned = self.face_aligner.align(image)
        if aligned is not None:
            print("face detected! start recognizing")
            person = self.face_recognizer.recognize(aligned)
            message = {"person": person}
        else:
            print("face not detected! failure occurred")
            message = {"person": ''}
        return message
