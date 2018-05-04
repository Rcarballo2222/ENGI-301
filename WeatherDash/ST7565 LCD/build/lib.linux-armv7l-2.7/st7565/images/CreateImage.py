"""
Creates PIL Image objects for images in this directory
"""
import os
from PIL import Image

os.chdir("/var/lib/cloud9/Git/Engi 301/WeatherDash/ST7565 LCD/st7565")

def create_image(img_file):
    """
    Takes image file (ex: "r2d2.pbm") and returns an Image object for it. File must be placed in images folder
    """
    return Image.open("/var/lib/cloud9/Git/Engi 301/WeatherDash/ST7565 LCD/st7565/images/" + img_file)



