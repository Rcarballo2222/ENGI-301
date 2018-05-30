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
    Returns an average percent chance of rain for the next `hours` hours
    """
    total_chance = -1
    if fio.has_hourly() and (hours > 0) and (hours < 49):
        total_chance = 0
        fiohr = FIOHourly.FIOHourly(fio)
        for hour in range(1,hours + 1):
            total_chance += float(fiohr.get_hour(hour)["precipProbability"])
        total_chance /= float(hours)
        total_chance = int(round(total_chance * 100))
    return total_chance    
            

