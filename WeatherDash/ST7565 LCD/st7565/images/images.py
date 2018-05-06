"""
Allows for creation, manipulation, and displaying of images contained in this directory for use in bitmaps.
"""
import os
from os import walk
from PIL import Image

import st7565.bitmap
import st7565.lcd

images_path = "/var/lib/cloud9/Git/Engi 301/WeatherDash/ST7565 LCD/st7565/images/"

def create_img(file_name):
    """Returns a `PIL` image object of `file_name`. """
    try:
        return Image.open(images_path + file_name)
    except IOError:
        print("Specified image file: %s cannot be found" % file_name)

def create_images():
    """
    Returns a dictionary containing a `PIL` image object for every image in this directory. Images must end in `.pbm` or `.jpg`.
    Using `images['filename']` will yield a `PIL` image object for that filename. 
    """
    images = {}
    for (dirpath, dirnames, filenames) in walk(images_path):
        break
    for file in filenames:
        if ((".pbm" in file) or (".jpg" in file)):
            images[file[:-4]] = create_img(images_path + file)
    return images

def resize_image(img, size):
    """
    Returns a proportionally resized image to `size` percent of the original image.
    
    `img`: A `PIL` image object.
    """
    size /= 100
    width, height = img.size
    width = round(width*size)
    height = round(height*size)
    img.resize((width,height))
    return img
            
def display_img(img, screen, lcd, size = 100, x=0, y=0):
    """
    Displays PIL image objects on the ST7565 display at a specified x and y coordinates.
    
    `img`: A `PIL` image object.
    `screen`: A bitmap object. What will be written to the display.
    `lcd`: An lcd object.
    """
    if not(size == 100):
        img = resize_image(img)
    screen.drawbitmap(img, x, y)
    lcd.write_buffer(screen) 


