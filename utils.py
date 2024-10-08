import requests
import json
import os
from datetime import datetime, timedelta


class WeatherForecast:
    def __init__(self, cache_file='weather_cache.json', latitude="51.7592", longitude="19.4560"):
        self.cache_file = cache_file
        self.latitude = latitude
        self.longitude = longitude
        self.cache = self.load_cache()

    def load_cache(self):
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as file:
                    return json.load(file)
        except Exception as e:
            print(f"Couldn't read cache: {e}")
        return {}

    def save_cache(self):
        try:
            with open(self.cache_file, 'w') as file:
                json.dump(self.cache, file, indent=4)
        except Exception as e:
            print(f"Couldn't save cache: {e}")

    def get_weather(self, date):
        url = (f"https://api.open-meteo.com/v1/forecast?"
               f"latitude={self.latitude}&longitude={self.longitude}&"
               f"hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&"
               f"start_date={date}&end_date={date}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data.get('daily', {}).get('rain_sum', [None])[0]
        except Exception as e:
            print(f"Error fetching weather data: {e}")
        return None

    def __getitem__(self, item):
        if item not in self.cache:
            rain_sum = self.get_weather(item)
            self.cache[
                item] = "It's gonna rain" if rain_sum and rain_sum > 0 else "It's not gonna rain" if rain_sum == 0 else "I don't know"
            self.save_cache()
        return self.cache[item]

    def __setitem__(self, date, weather):
        self.cache[date] = weather
        self.save_cache()

    def __iter__(self):
        return iter(self.cache)

    def items(self):
        return self.cache.items()


def main():
    forecast = WeatherForecast()

    date_input = input("Enter date (YYYY-mm-dd), or press Enter for tomorrow: ")
    if not date_input:
        date_input = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    try:
        weather = forecast[date_input]
        print(f"Weather on {date_input}: {weather}")

        print("\nStored forecasts:")
        for date, weather in forecast.items():
            print(f"{date}: {weather}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
