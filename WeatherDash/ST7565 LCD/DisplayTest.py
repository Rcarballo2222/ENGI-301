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
"""
for key, value in weather_icons.items():
    lcd.clear()
    lcd.pos(0)
    screen.clear()
    if (key == "partly_cloudy" or key == "p_cloudy_night"):
        screen.drawbitmap(value.resize((50,50)))
    else:
        screen.drawbitmap(value.resize((64,64)))
    screen.hscroll(60)
    lcd.write_buffer(screen)
    lcd.pos(4)
    lcd.puts(key)
    time.sleep(1.5)
""" 
"""
sunny = weather_icons["sunny"].resize((64,64))
snowy = weather_icons["snowy"].resize((64,64))
screen.drawbitmap(snowy)
screen.hscroll(60)
#screen.drawbitmap(rainy)
lcd.write_buffer(screen)
"""