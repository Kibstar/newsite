import json
import requests
import datetime

lat = '52.213'
long = '0.753'


class General:

    # This is my unique API key I use to call data. Maximum 60 calls per minute.
    api_key = '5fab7e900289e050f6ad161e8cee3dde'

    # Takes in Lat and Long and then finds the data on the internet with an API call.
    def __init__(self, city_name):
        self.max_wind = 17
        self.min_temp = 10
        self.city_name = city_name
        self.lat = lat
        self.long = long
        # Weather data for each instance are stored in a parent class where a few other variables are stored.
        self.get_weather_data_city()
        self.unique_dates()
        self.times()
        self.data()

    def times(self):  # Creates a list of all the times eg.1582275600.
        time_list = []
        for i in self.weather_data['list']:
            time = i['dt']
            time_list.append(time)
            self.time_list = time_list
    # Gathers the data from the internet using, Lat, Long and API key.

    def get_weather_data_city(self):
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={self.city_name}&appid={self.api_key}'
        print(url)
        res = requests.get(url)
        try:
            res.raise_for_status()
            self.weather_data = res.json()
            # with open('weather_data.json', 'w') as f:
            #     json.dump(self.weather_data, f, indent=4)
            self.fail = False

        except:
            self.fail = True
            print(self.fail)
            # with open('weather_data.json', 'r') as f:
            #     self.weather_data = json.load(f)

    # Creates a list of all the unique dates. Used for printing out the data eg. Monday 23rd Feburary.
    def unique_dates(self):
        list = []
        for i in self.weather_data['list']:
            x = datetime.datetime.utcfromtimestamp(
                i['dt']).strftime('%A %d %B')
            if x not in list:
                list.append(x)
                self.dates = list

    # Automatically creates a list of all the objects created using the time eg.1582275600.
    def data(self):
        list_of_obj = []
        for i in self.time_list:
            o = Weather(i, self)
            list_of_obj.append(o)
            self.weather_data_list = list_of_obj


class Weather:
    def __init__(self, time, parent):
        self.parent = parent
        self.time = time
        self.extract_data()
        self.cardinal = self.convert_degrees(self.wind_dir)
        self.tf_time = self.convert_time(self.time)
        self.dark_func()
        self.good_to_fly()
        self.date = datetime.datetime.utcfromtimestamp(
            self.time).strftime('%A %d %B')
        self.date = self.date.lstrip('0')

    def extract_data(self):  # Extracts a lot of info about each 3 hour interval
        for i in self.parent.weather_data['list']:
            if i['dt'] == self.time:
                for k1, v1 in i['wind'].items():
                    if k1 == 'speed':
                        self.wind_speed = self.convert_wind(v1)
                    if k1 == 'deg':
                        self.wind_dir = v1
                for k2, v2 in i['main'].items():
                    if k2 == 'temp':
                        self.temp = self.convert_temp(v2)
                for j in i['weather']:
                    self.main = j['main']
                    self.description = j['description']
                    self.iconname = j['icon']

        loc = self.parent.weather_data['city']
        for k, v in loc.items():
            if k == 'name':
                self.city = v
            if k == 'country':
                self.country = v
            if k == 'timezone':
                self.timezone = v

    def convert_time(self, secs):
        return (datetime.datetime.utcfromtimestamp(secs).strftime('%H:%M').lstrip('0'))

    def convert_degrees(self, degs):

        dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        return dirs[(int(degs // 22.5))]

    def convert_temp(self, k):
        return round(k - 273.15, 1)

    def convert_wind(self, mps):
        return round(mps * 2.23694, 1)

    def dark_func(self):
        for k1, v1 in self.parent.weather_data['city'].items():
            if k1 == 'sunset':
                t = (v1 + self.timezone)
                self.sunset = self.convert_time(t)
            if k1 == 'sunrise':
                t = (v1 + self.timezone)
                self.sunrise = self.convert_time(t)
        if (float(self.tf_time.replace(':', '.')) + 1.3) > float(self.sunrise.replace(':', '.')) and float(self.tf_time.replace(':', '.')) < float(self.sunset.replace(':', '.')):
            self.dark = False
        else:
            self.dark = True

    def good_to_fly(self):
        why = []
        if self.temp > self.parent.min_temp and (self.wind_speed < self.parent.max_wind) and self.dark == False and self.main != 'Rain':
            self.why = why
            return True

        else:
            if self.temp < self.parent.min_temp:
                why.append('Too cold,')

            if self.wind_speed > self.parent.max_wind:
                why.append('Too Windy,')

            if self.dark == True:
                why.append('Too Dark,')

            if self.main == 'Rain':
                why.append("It's raining")

            self.why = ' '.join(why).strip(',')
            return False

    @classmethod
    def change_max_wind(cls, new_amount):
        cls.max_wind = new_amount

    @classmethod
    def change_min_temp(cls, new_amount):
        cls.min_temp = new_amount


example = General('Manchester')
