# WeatherDash

Check the weather at a glance!

Never be caught unprepared!

#Installation and Usage:

1. Clone Library
2. Install lib-jpeg using apt
4. Install ztlib using apt
3. Install Pillow using pip
5. Use config-pin utility to configure SPI pins and GPIOs on PocketBeagle using https://github.com/beagleboard/bb.org-overlays/blob/master/tools/beaglebone-universal-io/config-pin
4. Run WeatherTest.py - This will give you the current forecast, including temperature and weather conditions.
5. Use the above data and edit WeatherDash/ST7565 LCD/st7565/cmd/stdemo.py to output the temperature in text format and weather icon in image format'
6. This code will eventually be setup to run indefinitely to pull from the api multiple times a day and auto update the display with the weather


Enjoy!
