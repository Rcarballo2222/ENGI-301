import time
from PIL import Image
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.SPI as SPI

import st7565.images.images as images
import st7565.bitmap
import st7565.fonts.font5x7 as font5x7
import st7565.lcd
import st7565.ops
import st7565.spidev

lcd = st7565.lcd.LCD(adafruit=True)
lcd.clear()
screen = st7565.bitmap.Bitmap()


weather_icons = images.create_images()
sunny = weather_icons["sunny"].resize((64,64))
screen.drawbitmap(sunny)
screen.hscroll(60)
lcd.write_buffer(screen)
lcd.pos(4, 20)
lcd.puts("79")

