"""
Indexes and lists fonts contained in this directory for use in bitmaps. 
Fonts must be in the form of an image containing 0-9 in ascending order with their regular letter spacing included.
"""
from PIL import Image
import st7565.images.images as images 


fonts_path = "/var/lib/cloud9/Git/Engi 301/WeatherDash/ST7565 LCD/st7565/fonts/"

def create_font(font_name):
    """
    returns a dictionary containing a `PIL` image object for every number in the specified font image `font_name`.jpg, callable in dictionary format.
    """
    font = {}
    try:
        numbers = Image.open(fonts_path + font_name + ".jpg")
        width, height = numbers.size
        width = width/10
        for i in range(9):
            box = (i*(width), 0, (i + 1)*(width), height)
            font[i] = numbers.crop() 
    except IOError:
        print("Specified font file: %s.jpg cannot be found" % font_name)
    return font
def display_c(c, font, screen, lcd, size, x=0, y=0):
    """
    Displays a character in the given `font` at the specified `x` and `y` coordinates
    
    `c`: A char
    `font`: A font dictionary
    `size`: An integer from 1-10, 10 being max size that can fit the display
    """
    char = font[c]
    
    images.display_img(c,screen,lcd,size,x,y)
        
    