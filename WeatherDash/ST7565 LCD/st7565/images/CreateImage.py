"""
Creates PIL Image objects for images in this directory
"""

from PIL import Image

def create_image(img_file):
    """
    Takes image file (ex: "r2d2.pbm") and returns an Image object for it. File must be placed in images folder
    """
    return Image.open(img_file)



