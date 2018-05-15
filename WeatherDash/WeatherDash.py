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
global FONT
global TIMEZONES
global temp
global PROTOCOL


"""
User-Settings
"""
TIMEZONE = "ET" #Current timezone
APIKEY = "ecec575b921533aa1148c52df084d94b" #Darksky API Key
TIMEOUT = 30 #Timeout for pulling data from Darksky
FONT = "segoe_ui" #Font to use for displaying numbers

""""""
if not(os.path.isfile("temp.txt")): 
    temp = open("temp.txt","w+")

font = fonts.create_font(FONT)
lcd = lcd.LCD(adafruit=True)  
screen = bitmap.Bitmap()
PROTOCOL = pickle.HIGHEST_PROTOCOL
TIMEZONES = {}
TIMEZONES["ET"] = 4 #UTC -4
TIMEZONES["CT"] = 5 #UTC -5

"""
Functions
"""

def reboot():
    os.system("sudo reboot")

def sleep():
    pass

def wake():
    pass

def maintenance():
    pass

def update():
    """
    Init
    """
    global APIKEY
    global TIMEOUT
    global FONT
    global PROTOCOL
    global temp
    
    
    lcd.clear()
    weather_icons = images.create_images()
    cur_location = weather.get_location()
    fio = ForecastIO.ForecastIO(APIKEY,units=ForecastIO.ForecastIO.UNITS_US,lang=ForecastIO.ForecastIO.LANG_ENGLISH)
    pickle.dump(fio, temp, -1)
    
    test = pickle.load(temp)
    test.get_forecast(cur_location[0], cur_location[1])
    fiocur = FIOCurrently.FIOCurrently(fio)
    current = fiocur.get()
    print current
    
    """
    Main Code
    
    try:
        with timeout.timeout(seconds=TIMEOUT):
            fio.get_forecast(cur_location[0], cur_location[1])
    except timeout.TimeoutError:
        print("Request timed out")
        print("Retrying with longer timeout")
        i = 10
        while(i > 0):
            print("Retrying in %d seconds..." % i)
            time.sleep(1)
            i -= 1
        try:
            with timeout.timeout(seconds=2*TIMEOUT):
                fio.get_forecast(cur_location[0], cur_location[1])
        except timeout.TimeoutError:
            print("Failed. Rebooting device in 5 seconds")
            time.sleep(5)
            reboot()
    
    for i in range(1,5):
        time.sleep(2)
        fiocur = FIOCurrently.FIOCurrently(fio)
        current = fiocur.get()
        temp = weather.get_temperature(current)
        icon = weather_icons[weather.get_icon(current)]
        #weather = weather_icons["partly_cloudy_day"]
        #temp = 83
        lcd.clear()
        if i % 2 == 0:
            images.shift_imgs(screen, lcd)
            print("shift")
        else:
            lcd.clear()
            images.display_img(icon, screen, lcd, 100, 58)
            fonts.display_s(str(temp) + "d",font, screen, lcd, 5, 2, 15)
            print("New")
    """        
def main():
    
    time = str(datetime.now().time())
    time = int(time[0:2])
    time -= TIMEZONES[TIMEZONE]
    update()
    """
    if time < 0:
        time = 24 + time
    if time == 7:
        wake()
        update()
    elif time == 23:
        sleep()
    elif not(time % 2 == 0):
        update()
    else:
        maintenance()
    """    
if __name__ == '__main__':
    main()