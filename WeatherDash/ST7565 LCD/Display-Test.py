import time
from PIL import Image
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.SPI as SPI

import st7565.images.CreateImage as images
import st7565.bitmap
import st7565.fonts.font5x7 as font5x7
import st7565.lcd
import st7565.ops
import st7565.spidev


lcd = st7565.lcd.LCD(adafruit=True)
screen = st7565.bitmap.Bitmap()
image = images.create_image("r2d2.pbm")
screen.drawbitmap(image, True, True)
lcd.write_buffer(screen)

