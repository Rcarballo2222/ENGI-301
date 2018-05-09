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
import datetime


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

