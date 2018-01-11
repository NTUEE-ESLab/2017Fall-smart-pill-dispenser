import io
import numpy as np
import json
import cv2

class RegisterHandler:
    def __init__(self, gallery_path, face_aligner, camera):
        self.gallery_path = gallery_path
        self.face_aligner = face_aligner
        self.camera = camera
    def register(self, post_data):
        info = json.loads(post_data)
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
            file_name = hash(time.time()) + ".jpg"
            directory = os.path.join(self.gallery_path, info.username)
            if not os.path.exists(directory):
                os.makedirs(directory)
            cv2.imwrite(os.path.join(directory, file_name), aligned)
            message = {"status": "sucess"}
        else:
            message = {"status": "fail"}
        return message
