import time
from datetime import datetime
import random
import os
import os.path
import pickle
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

#Declaring global values
global TIMEZONE
global APIKEY
global TIMEOUT
global TIMEZONES
global TEMP_FILE
global lcd
global screen
global font
global icons
global cur_location
global fio

"""
User-Settings
"""
TIMEZONE = "ET" #Current timezone
APIKEY = "ecec575b921533aa1148c52df084d94b" #Darksky API Key
TIMEOUT = 30 #Timeout for pulling data from Darksky
FONT = "segoe_ui" #Font to use for displaying numbers

""""""
font = fonts.create_font(FONT)
lcd = lcd.LCD(adafruit=True)  
screen = bitmap.Bitmap()
icons = images.create_images()
cur_location = weather.get_location()
fio = ForecastIO.ForecastIO(APIKEY,units=ForecastIO.ForecastIO.UNITS_US,lang=ForecastIO.ForecastIO.LANG_ENGLISH)

TIMEZONES = {}
TIMEZONES["ET"] = 4 #UTC -4
TIMEZONES["CT"] = 5 #UTC -5
TEMP_FILE = "temp.tmp"
if not(os.path.isfile(TEMP_FILE)): 
    tmp = open(TEMP_FILE, "w+")

"""
Functions
"""

def reboot():
    os.system("sudo reboot")

def sleep():
    global lcd
    
    lcd.sleep()
    
def wake():
    global lcd
    
    lcd.wake()

def maintenance():
    global screen
    global lcd 
    
    temp = open(TEMP_FILE, "r")
    screen = pickle.load(temp)
    images.shift_imgs(screen, lcd)
    
def first_start():
    
    global TIMEOUT
    global icons
    global screen
    global lcd
    global cur_location
    
    wake()
    not_connected = True
    
    try:
        with timeout.timeout(seconds=300):
            images.display_img(icons["weatherdash_logo"], screen, lcd, 60, 20, 10)
            lcd.pos(6, 40)
            lcd.puts("Loading...")
            while not_connected:
                try:
                    with timeout.timeout(seconds=2):
                        lcd.clear()
                        lcd.puts("In loop")
                        fio.get_forecast(cur_location[0], cur_location[1])
                        lcd.pos(2)
                        lcd.puts("Connected")
                        not_connected = False
                except timeout.TimeoutError:
                    continue
    except timeout.TimeoutError:
        lcd.clear()
        lcd.puts("Request timed out")
        lcd.page_set(2)
        lcd.puts("Retrying with longer timeout")
        lcd.page_set(3)
        lcd.puts("Retrying in 10 seconds...")
        i = 10
        while(i > 0):
            time.sleep(1)
            i -= 1
        try:
            with timeout.timeout(seconds=2*TIMEOUT):
                fio.get_forecast(cur_location[0], cur_location[1])
        except timeout.TimeoutError:
            lcd.page_set(4)
            lcd.puts("Failed. Rebooting device in 5 seconds")
            time.sleep(5)
            reboot()
    screen.clear()
    lcd.clear()
    update()

def update():
    """
    Init
    """
    global APIKEY
    global TIMEOUT
    global FONT
    global TEMP_FILE
    global screen
    global lcd
    global icons
    global cur_location
    global fio
    
    lcd.clear()
    
    """
    Main Code
    """
    try:
        with timeout.timeout(seconds=TIMEOUT):
            fio.get_forecast(cur_location[0], cur_location[1])
    except timeout.TimeoutError:
        lcd.clear()
        lcd.puts("Request timed out")
        lcd.page_set(2)
        lcd.puts("Retrying with longer timeout")
        lcd.page_set(3)
        lcd.puts("Retrying in 10 seconds...")
        i = 10
        while(i > 0):
            time.sleep(1)
            i -= 1
        try:
            with timeout.timeout(seconds=2*TIMEOUT):
                fio.get_forecast(cur_location[0], cur_location[1])
        except timeout.TimeoutError:
            lcd.page_set(4)
            lcd.puts("Failed. Rebooting device in 5 seconds")
            time.sleep(5)
            reboot()
    
    fiocur = FIOCurrently.FIOCurrently(fio)
    current = fiocur.get()
    temp = weather.get_temperature(current)
    icon = icons[weather.get_icon(current)]
    lcd.clear()

    screen = images.display_img(icon, screen, lcd, 100, 58)
    screen = fonts.display_s(str(temp) + "d",font, screen, lcd, 5, 2, 15)
    temp = open(TEMP_FILE, "w")
    pickle.dump(screen, temp, -1)
          
def main():
    
    lcd.clear()
    cur_time = str(datetime.now().time())
    cur_time = int(cur_time[0:2])
    cur_time -= TIMEZONES[TIMEZONE]
    
    print("testing")
    
    if cur_time < 0:
        cur_time += 24
    if cur_time == 7:
        wake()
        update()
    elif cur_time == 23:
        sleep()
    elif cur_time > 7 and cur_time < 23 and not(cur_time % 2 == 0):
        update()
    elif cur_time > 7 and cur_time < 23 and (cur_time % 2 == 0):
        maintenance()
    else:
        sleep()
  
if __name__ == '__main__':
    main()