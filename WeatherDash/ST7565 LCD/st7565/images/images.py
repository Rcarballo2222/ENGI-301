"""
Indexes and lists images contained in this directory for use in bitmaps
"""
import os
from os import walk
from PIL import Image

images_path = "/var/lib/cloud9/Git/Engi 301/WeatherDash/ST7565 LCD/st7565/images/"

def create_images():
    """
    Creates a `PIL` image object for every image in this directory, callable in dictionary format. Images must end in `.pbm` or `.jpg`
    Using `images[filename]` will yield a `PIL` image object for that filename. 
    """
    images = {}
    for (dirpath, dirnames, filenames) in walk(images_path):
        break
    for file in filenames:
        if ((".pbm" in file) or (".jpg" in file)):
            images[file[:-4]] = Image.open(images_path + file)
    return images
            



