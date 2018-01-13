#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import argparse
import time
import json
from face_recognizer import FaceRecognizer
from face_aligner import FaceAligner
from register_handler import RegisterHandler
from recognize_handler import RecognizeHandler
from algorithm import OpenCVAlgorithm
import base64
import numpy as np
import cv2

parser = argparse.ArgumentParser(description='Server for registering')
# Path Arguments
parser.add_argument('--predictor_path', type=str, required=True,
                            help='location of the dlib facial landmark predictor where shape_predictor_68_face_landmarks.dat is located')
parser.add_argument('--gallery_path', type=str, required=True,
                            help='location of the gallery')
parser.add_argument('--port', type=int, default=8000,
                            help='which port to use')
args = parser.parse_args()


face_aligner = FaceAligner(args.predictor_path)
face_recognizer = FaceRecognizer(args.gallery_path, OpenCVAlgorithm, face_aligner)
register_handler = RegisterHandler(args.gallery_path, face_aligner)
recognize_handler = RecognizeHandler(args.gallery_path, face_aligner, face_recognizer)

class S(BaseHTTPRequestHandler):
    def _set_response(self, message=None):
        self.send_response(200)
        if message is not None:
        #self.send_header('Content-type', 'text/html')
            self.send_header('Content-type', 'application/json')

        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        message = recognize_handler.recognize()
        self._set_response()
        self.wfile.write(json.dumps(message).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_data = json.loads(post_data.decode('utf-8'))
        img = post_data["img"]
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #        str(self.path), str(self.headers))

        def decode_base64(data):
            """Decode base64, padding being optional.
        
            :param data: Base64 data as an ASCII byte string
            :returns: The decoded byte string.
        
            """
            missing_padding = len(data) % 4
            if missing_padding != 0:
                data += b'='* (4 - missing_padding)
            return base64.decodestring(data)

        img_str = decode_base64(img.encode("utf-8"))
        nparr = np.fromstring(img_str, np.uint8)
        #img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite('ou.jpg', img)

        message = ''
        print("path: {}".format(self.path))
        if self.path == "/register":
            username = post_data["username"]
            message = register_handler.register(username, img)
            if message['status'] == "success":
                face_recognizer.train()
        elif self.path == "/recognize":
            message = recognize_handler.recognize(img)
            
        print("result: {}".format(message))
        self._set_response()
        self.wfile.write(json.dumps(message).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    run(port=args.port)
