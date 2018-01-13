import cv2
import dlib
import os
from utils import extract_left_eye_center, extract_right_eye_center, get_rotation_matrix, crop_image

class FaceAligner:
    def __init__(self, predictor_path, scale=1):
        self.detector = dlib.get_frontal_face_detector()
        path = os.path.join(predictor_path, "shape_predictor_68_face_landmarks.dat")
        self.predictor = dlib.shape_predictor(path)
        self.scale = scale
    def align(self, img):
        print("image shape: {}".format(img.shape))
        height, width = img.shape[:2]
        s_height, s_width = height // self.scale, width // self.scale
        img = cv2.resize(img, (s_width, s_height))

        dets = self.detector(img, 1)
        print("number of dets: {}".format(len(dets)))
        def crop_from_detected(det):
            shape = self.predictor(img, det)
            left_eye = extract_left_eye_center(shape)
            right_eye = extract_right_eye_center(shape)

            M = get_rotation_matrix(left_eye, right_eye)
            rotated = cv2.warpAffine(img, M, (s_width, s_height), flags=cv2.INTER_CUBIC)

            cropped = crop_image(rotated, det)
            return cropped
        try:
            cropped_face = crop_from_detected(dets[0])
            return cropped_face
        except:
            return None

