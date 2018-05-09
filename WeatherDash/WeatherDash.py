import time
import random
import os
from PIL import Image
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.SPI as SPI

import ST7565_LCD.st7565.images.images as images
import ST7565_LCD.st7565.fonts.fonts as fonts
import ST7565_LCD.st7565.bitmap as bitmap
import ST7565_LCD.st7565.fonts.font5x7 as font5x7
import ST7565_LCD.st7565.lcd as lcd

import Forecast_IO_py.weather as weather
import Forecast_IO_py.forecastiopy.ForecastIO as ForecastIO
import Forecast_IO_py.forecastiopy.FIOAlerts as FIOAlerts
import Forecast_IO_py.forecastiopy.FIOCurrently as FIOCurrently
import Forecast_IO_py.forecastiopy.FIODaily as FIODaily
import Forecast_IO_py.forecastiopy.FIOFlags as FIOFlags
import Forecast_IO_py.forecastiopy.FIOHourly as FIOHourly
import Forecast_IO_py.forecastiopy.FIOMinutely as FIOMinutely
import Forecast_IO_py.forecastiopy.timeout as timeout

def reboot():
    os.system("sudo reboot")

"""
Init
"""
APIKEY = "ecec575b921533aa1148c52df084d94b"
font = fonts.create_font("segoe_ui")

lcd = lcd.LCD(adafruit=True)
lcd.clear()
screen = bitmap.Bitmap()
weather_icons = images.create_images()
cur_location = weather.get_location()
fio = ForecastIO.ForecastIO(APIKEY,units=ForecastIO.ForecastIO.UNITS_US,lang=ForecastIO.ForecastIO.LANG_ENGLISH)

"""
Main Code
"""
try:
    with timeout.timeout(seconds=10):
        fio.get_forecast(cur_location[0], cur_location[1])
except timeout.TimeoutError:
    print("Request Timed Out")
    print("Retrying in 10 seconds...")
    try:
        with timeout.timeout(seconds=10):
            fio.get_forecast(cur_location[0], cur_location[1])
    except timeout.TimeoutError:
        print("Failed. Rebooting device in 5 seconds")
        time.sleep(5)
        reboot()
        
fiocur = FIOCurrently.FIOCurrently(fio)
current = fiocur.get()
temp = weather.get_temperature(current)
weather = weather_icons[weather.get_icon(current)]
#weather = weather_icons["partly_cloudy_day"]
#temp = 83
images.display_img(weather, screen, lcd, 100, 58)
fonts.display_s(str(temp) + "d",font, screen, lcd, 5, 2, 15)
time.sleep(1)
images.shift_imgs(screen, lcd)
time.sleep(1)
images.shift_imgs(screen, lcd)


