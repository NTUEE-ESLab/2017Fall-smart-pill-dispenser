import io
import numpy as np
import json
import cv2
from collections import Counter

class RecognizeHandler:
    def __init__(self, gallery_path, face_aligner, face_recognizer, camera, interval=3):
        self.gallery_path = gallery_path
        self.face_aligner = face_aligner
        self.face_recognizer = face_recognizer
        self.camera = camera
        self.interval = interval
    def recognize(self, post_data):
        start_time = time.time()
        info = json.loads(post_data)
        recognized_results = []
        while time.time() - start_time < self.interval:
            stream = io.BytesIO()
            self.camera.capture(stream, format='jpeg')
            # Construct a numpy array from the stream
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            # "Decode" the image from the array, preserving colour
            image = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
            # OpenCV returns an array with data in BGR order. If you want RGB instead
            # use the following...
            aligned = self.face_aligner.align(image)
            if aligned is not None:
                person = self.face_recognizer.recognize(aligned)
                recognized_results.append(person)
        results = Counter(recognized_results)
        person = results.most_common(1)[0][0]
        message = {"person": person}
        return message
