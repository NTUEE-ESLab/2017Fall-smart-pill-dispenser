#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from button import Button
import picamera
import argparse
import time
import json
from arduino import callForDrug

parser = argparse.ArgumentParser(description='Server for registering')
# Path Arguments
parser.add_argument('--predictor_path', type=str, required=True,
                            help='location of the dlib facial landmark predictor')
parser.add_argument('--gallery_path', type=str, required=True,
                            help='location of the dlib facial landmark predictor')
parser.add_argument('--port', type=int, default=8080,
                            help='which port to use')
args = parser.parse_args()

class S(BaseHTTPRequestHandler):
    def _set_response(self, message=None):
        self.send_response(200, message)
        if message is not None:
        #self.send_header('Content-type', 'text/html')
            self.send_header('Content-type', 'applicaion/json')

        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        callForDrug(3, 4)
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_data = post_data.decode('utf-8')
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data)

        self._set_response()


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
