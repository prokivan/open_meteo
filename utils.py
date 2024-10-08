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
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading cache file: {e}")
        return {}

    def save_cache(self):
        try:
            with open(self.cache_file, 'w') as file:
                json.dump(self.cache, file, indent=4)
        except IOError as e:
            print(f"Error saving cache: {e}")

    def get_weather(self, date):
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude="
               f"{self.longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'daily' in data and 'rain_sum' in data['daily']:
                return data['daily']['rain_sum'][0]
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
        except (KeyError, IndexError) as e:
            print(f"Error parsing weather data: {e}")
        return None

    def __getitem__(self, item):
        if item not in self.cache:
            rain_sum = self.get_weather(item)
            if rain_sum is None:
                self.cache[item] = "I don't know"
            elif rain_sum > 0:
                self.cache[item] = "It's gonna rain"
            else:
                self.cache[item] = "It's not gonna rain"
            self.save_cache()
        return self.cache[item]

    def __setitem__(self, date, weather):
        try:
            self.cache[date] = weather
            self.save_cache()
        except Exception as e:
            print(f"Error setting cache item: {e}")

    def __iter__(self):
        return iter(self.cache)

    def items(self):
        return self.cache.items()


def main():
    try:
        forecast = WeatherForecast()

        date_input = input("Enter date (YYYY-mm-dd), or press Enter for tomorrow: ")
        if not date_input:
            date_input = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        weather = forecast[date_input]
        print(f"Weather on {date_input}: {weather}")

        print("\nStored forecasts:")
        for date, weather in forecast.items():
            print(f"{date}: {weather}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()