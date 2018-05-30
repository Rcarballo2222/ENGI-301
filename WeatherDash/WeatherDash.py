import time
from datetime import datetime
import random
import os
import os.path
import pickle
import urllib3
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
cur_location = [25.6781743,-80.326881] #Current location [Lattitude, Longitude]

""""""
font = fonts.create_font(FONT)
lcd = lcd.LCD(adafruit=True)  
screen = bitmap.Bitmap()
icons = images.create_images()
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

def retry_attempt():
    global TIMEOUT
    global lcd
    global cur_location
    global fio
    
    time_start = time.time()
    retry_timeout = TIMEOUT * 2
    not_connected = True
    
    lcd.clear()
    lcd.puts("Error") 
    lcd.pos(1)
    lcd.puts("Unable to update data")
    lcd.pos(2)
    lcd.puts("Check your Internet Connection")
    time.sleep(1)
    i = 10
    while(i > 0):
        text = "Retrying in " + "  " + " seconds..."
        lcd.pos(3)
        lcd.puts(text)
        text = "Retrying in " + str(i) + " seconds..."
        lcd.pos(3)
        lcd.puts(text)
        time.sleep(1)
        i -= 1
    try:
        
        while not_connected:
            try:
                with timeout.timeout(seconds=retry_timeout):
                    fio.get_forecast(cur_location[0], cur_location[1])
                    not_connected = False
            except:
                time_elapsed = time.time() - time_start
                if time_elapsed > retry_timeout:
                    raise timeout.TimeoutError("Max Timeout")
                else:
                    time.sleep(2)
                    continue
    except timeout.TimeoutError:
        lcd.pos(4)
        lcd.puts("Failed.")
        lcd.pos(5)
        lcd.puts("Rebooting device in 5s")
        time.sleep(5)
        reboot()
    
def first_start():
    
    global TIMEOUT
    global icons
    global screen
    global lcd
    global cur_location
    global fio
    
    wake()
    not_connected = True
    
    try:
        time_start = time.time()
        images.display_img(icons["weatherdash_logo"], screen, lcd, 60, 20, 10)
        lcd.pos(6, 40)
        lcd.puts("Loading...")
        while not_connected:
            try:
                with timeout.timeout(seconds=2):
                    fio.get_forecast(cur_location[0], cur_location[1])
                    not_connected = False
            except:
                time_elapsed = time.time() - time_start
                if time_elapsed > 300:
                    raise timeout.TimeoutError("Max Timeout")
                else:
                    time.sleep(2)
                    continue
    except timeout.TimeoutError:
        retry_attempt()
    screen.clear()
    lcd.clear()
    update()

def update():
    """
    Init
    """
    global APIKEY
    global TIMEOUT
    global font
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
    except:
        retry_attempt()
        
    fiocur = FIOCurrently.FIOCurrently(fio)
    current = fiocur.get()
    temp = weather.get_temperature(current)
    icon = icons[weather.get_icon(current)]
    chance_of_rain = weather.get_rain_chance(fio)
    lcd.clear()

    screen = images.display_img(icon, screen, lcd, 70, 77)
    screen = fonts.display_s(str(temp) + "d",font, screen, lcd, 5, 5, 7)
    screen = images.display_img(icons["umbrella"], screen, lcd, 20, 40, 48)
    test_font = fonts.create_font("pixel", False)
    if chance_of_rain > 0:
        screen = fonts.display_s(str(chance_of_rain) + "p",font, screen, lcd, 2, 57, 48)
    temp = open(TEMP_FILE, "w")
    pickle.dump(screen, temp, -1)
          
def main():
    lcd.clear()
    cur_time = str(datetime.now().time())
    cur_time = int(cur_time[0:2])
    cur_time -= TIMEZONES[TIMEZONE]

    if cur_time < 0:
        cur_time += 24
    if cur_time == 7:
        reboot()
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