"""
Contains functions that simplify weather data acquisition for the display
"""

import forecastiopy.ForecastIO as ForecastIO
import forecastiopy.FIOAlerts as FIOAlerts
import forecastiopy.FIOCurrently as FIOCurrently
import forecastiopy.FIODaily as FIODaily
import forecastiopy.FIOFlags as FIOFlags
import forecastiopy.FIOHourly as FIOHourly
import forecastiopy.FIOMinutely as FIOMinutely
from datetime import datetime


def get_location():
    """
    Returns current location of device in [latitude, longitude]
    """
    return [25.761681, -80.191788]

def get_icon(fio):
    """
    Returns a formatted icon name that should be displayed
    """
    icon = fio["icon"]
    if "-" in icon:
        icon = icon.replace('-', '_')
    if icon == "fog":
        icon = "cloudy"
    if icon == "sleet":
        icon = "snow"
    return icon
def get_temperature(fio):
    """
    Returns temperature in degrees
    """
    temp = int(round(fio["temperature"]))
    return temp
    
def get_rain_chance(fio, hours = 5):
    """
    Returns the highest percent chance of rain and the hour that it's the highest for the next `hours` hours
    """
    highest_chance = -1
    if fio.has_hourly() and (hours > 0) and (hours < 49):
        highest_chance = 0
        highest_chance_hour = 0
        fiohr = FIOHourly.FIOHourly(fio)
        fiocur = FIOCurrently.FIOCurrently(fio)
        highest_chance = float(fiocur.get()["precipProbability"])
        for hour in range(1,hours + 1):
            hour_chance = float(fiohr.get_hour(hour)["precipProbability"])
            if hour_chance > highest_chance:
                highest_chance = hour_chance
                highest_chance_hour = hour
        highest_chance = int(round(highest_chance * 100))
    return highest_chance, highest_chance_hour    
            

