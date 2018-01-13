import io
import numpy as np
import json
import cv2
import time
import os

class RegisterHandler:
    def __init__(self, gallery_path, face_aligner):
        self.gallery_path = gallery_path
        self.face_aligner = face_aligner
    def register(self, username, image):
        # OpenCV returns an array with data in BGR order. If you want RGB instead
        # use the following...
        aligned = self.face_aligner.align(image)
        if aligned is not None:
            file_name = str(hash(time.time())) + ".jpg"
            directory = os.path.join(self.gallery_path, username)
            print("directory: {}".format(directory))
            print("filename: {}".format(file_name))
            if not os.path.exists(directory):
                os.makedirs(directory)
            cv2.imwrite(os.path.join(directory, file_name), aligned)
            message = {"status": "sucess"}
        else:
            message = {"status": "fail"}

        print(message)
        return message
