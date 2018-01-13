from io import BytesIO
from time import sleep
from picamera import PiCamera
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import requests
import json
from arduino import callForDrug

# Create an in-memory stream
camera = PiCamera()
camera.resolution = (320, 240)
camera.start_preview()
url = 'http://140.112.18.204:8000'
class S(BaseHTTPRequestHandler):
    def _set_response(self, message=None):
        self.send_response(200)
        #self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        if self.path == "/recognize":
            camera.capture('foo.jpg')
            with open('foo.jpg', 'rb') as f:
                byte_im = f.read()
                encoded = base64.b64encode(byte_im)
            payload = {"img": encoded}
            print("sending images...")
            try:
                res = requests.post(url + "/recognize", json=payload)
                print("end sending images...")
                body = res.json()
            except:
                body = {"status": "fail"}
            print("recognize response body: {}".format(body))
        self._set_response()
        self.wfile.write(json.dumps(body).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_data = json.loads(post_data.decode('utf-8'))
        print(post_data)
        if self.path == "/register":
            camera.capture('foo.jpg')
            with open('foo.jpg', 'rb') as f:
                byte_im = f.read()
                encoded = base64.b64encode(byte_im)
            payload = {'username': post_data["username"], "img": encoded}
            print("sending images...")
            try:
                res = requests.post(url + "/register", json=payload)
                print("end sending images...")
                body = res.json()
            except:
                body = {"status": "fail"}
        elif self.path == "/delivery":
            try:
                callForDrug(post_data['drugA'], post_data['drugB'])
                body = {"status": "success"}
            except:
                body = {"status": "fail"}
        self._set_response()
        self.wfile.write(json.dumps(body).encode('utf-8'))


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
    run(port=8000)
