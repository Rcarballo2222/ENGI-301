"""
Indexes and lists fonts contained in this directory for use in bitmaps. 
Currently only works with numbers
Fonts must be in the form of an image containing 0-9 in ascending order on the same line with their regular letter spacing included.
"""
from PIL import Image
import ST7565_LCD.st7565.images.images as images
import os 

fonts_path = os.path.dirname(os.path.realpath(__file__)) + "/"

def create_font(font_name, fit = True):
    """
    Returns a dictionary containing a `PIL` image object for every number in the specified font image `font_name`.jpg, callable in dictionary format.
    """
    font = {}
    try:
        numbers = Image.open(fonts_path + font_name + ".jpg")
        if fit:
            numbers = images.fit_to_display(numbers, True)
        width, height = numbers.size
        font["d"] = Image.open(fonts_path + "degree.jpg")
        font["d"] = images.fit_to_display(font["d"])
        font["p"] = Image.open(fonts_path + "percent.jpg")
        font["p"] = images.fit_to_display(font["p"])
        font["m"] = Image.open(fonts_path + "am.jpg")
        font["m"] = images.fit_to_display(font["m"], True)
        font["a"] = Image.open(fonts_path + "pm.jpg")
        font["a"] = images.fit_to_display(font["a"], True)
        d_w, d_h = font["d"].size
        font["d"] = font["d"].crop((10,0,d_w-10,d_w))
        box_width = float(width)/10   
        #Crop out each character in the provided image and save that to a dictionary
        for i in range(0, 10):
            box = [int(round(i*(box_width))), 0, int(round((i + 1)*(box_width))), height]
            #Checks if a subrectangle passes the width of the image, and shortens it if necessary
            if box[3] > width:
                box[3] = width
            
            box = tuple(box)
            font[str(i)] = numbers.crop(box) 
        return font
    except IOError:
        print("Specified font file: %s.jpg cannot be found at: %s" % (font_name,fonts_path))
def display_c(c, font, screen, lcd, size=5, x=0, y=0):
    """
    Displays a character in the given `font` with top-left corner at the specified `x` and `y` coordinates
    
    `c`: A character
    `font`: A font dictionary
    `size`: An integer from 1-10, 10 being max size that can fit the display
    """
    char = font[str(c)]
    width, height = char.size
    """
    if not(size == 10):
        size /= 10.0
        width = int(round(size*width))
        height = int(round(size*height))
        char.resize((width,height))
    """
    size = int(round(size * 10))
    images.display_img(char,screen,lcd,size,x,y)
        
def display_s(s, font, screen, lcd, size=5, x=0, y=0):
    """
    Displays a string of characters in the given `font` with top-left corner at the specified `x` and `y` coordinates
    
    Returns an updated screen object if wanted
    """
    i = 0
    spacing = size * .11
    s = str(s)
    char = s[0]
    char_w, char_h = font[char].size
    for c in s:
        display_c(c,font,screen,lcd,size,(int(i*spacing*char_w)+x),y)
        i += 1
    return screen    
        
        
        