import glob
import os

class Person:
    def __init__(self, name, images_folder, num):
        self.name = name
        self.num = num
        self.images_folder = images_folder
        image_formats = ["jpg", "png"]
        self.image_files = []
        for image_format in image_formats:
            self.image_files += glob.glob(os.path.join(images_folder, "*.{}".format(image_format)))

            
