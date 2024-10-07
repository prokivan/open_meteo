import requests
import json
import os
from datetime import datetime, timedelta


class WeatherForecast:
    def __init__(self, cache_file='weather_cache.json', latitude="51.7592", longitude="19.4560"):
        self.cache_file = cache_file
        self.latitude = latitude
        self.longitude = longitude
        self.cache = self._read_cache()

    def _read_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as file:
                return json.load(file)
        return {}

    def _write_cache(self):
        with open(self.cache_file, 'w') as file:
            json.dump(self.cache, file, indent=4)

    def _fetch_weather(self, date):
        url = (f"https://api.open-meteo.com/v1/forecast?"
               f"latitude={self.latitude}&longitude={self.longitude}&"
               f"hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&"
               f"start_date={date}&end_date={date}")

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rain_sum = data['daily']['rain_sum']
            if rain_sum:
                return rain_sum[0]
        return None

    def __getitem__(self, item):
        if item not in self.cache:
            rain_sum = self._fetch_weather(item)
            if rain_sum is None:
                self.cache[item] = "I don't know"
            elif rain_sum > 0:
                self.cache[item] = "It's gonna rain"
            else:
                self.cache[item] = "It's not gonna rain"
            self._write_cache()
        return self.cache[item]

    def __setitem__(self, date, weather):
        self.cache[date] = weather
        self._write_cache()

    def __iter__(self):
        return iter(self.cache)

    def items(self):
        return self.cache.items()


def main():
    weather_forecast = WeatherForecast()

    date_input = input("Input date (YYYY-mm-dd), Enter- for choice tomorrow: ")
    if not date_input:
        date_input = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    weather = weather_forecast[date_input]
    print(f"Weather on day {date_input}: {weather}")

    print("\nInfo from file:")
    for date, weather in weather_forecast.items():
        print(f"{date}: {weather}")


if __name__ == '__main__':
    main()
