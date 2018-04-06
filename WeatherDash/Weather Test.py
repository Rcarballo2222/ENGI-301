from forecastiopy import ForecastIO, FIOAlerts, FIOCurrently, FIODaily, FIOFlags, FIOHourly, FIOMinutely
import datetime

apikey = "ecec575b921533aa1148c52df084d94b"

Houston = [29.761993, -95.366302]

fio = ForecastIO.ForecastIO(apikey,units=ForecastIO.ForecastIO.UNITS_US,lang=ForecastIO.ForecastIO.LANG_ENGLISH,latitude=Houston[0], longitude=Houston[1])
fio.get_forecast(fio.latitude, fio.longitude)
#print(fio.get_currently)

fiocur = FIOCurrently.FIOCurrently(fio)
testcurrently =  fiocur.get()
testcurrently['time'] = datetime.datetime.fromtimestamp(int((testcurrently['time'])))
testcurrently['time'] = testcurrently['time'].strftime('%Y-%m-%d %H:%M:%S')
print(testcurrently)

