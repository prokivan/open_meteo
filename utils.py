import requests
import json
from datetime import datetime, timedelta
import os
from permanents import API_URL, LATITUDE, LONGITUDE, CACHE_FILE


def get_weather_data(date):
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "rain",
        "daily": "rain_sum",
        "timezone": "Europe/London",
        "start_date": date,
        "end_date": date
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if "daily" in data and "rain_sum" in data["daily"] and len(data["daily"]["rain_sum"]) > 0:
            rain_sum = data["daily"]["rain_sum"][0]
            return rain_sum
        else:
            return None
    else:
        return None


def check_rain(date):
    rain_sum = get_weather_data(date)

    if rain_sum is None:
        return "I don't know"
    elif rain_sum > 0.0:
        return "It's gonna rain"
    elif rain_sum == 0.0:
        return "It's not gonna rain"
    else:
        return "I don't know"


def read_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    else:
        return {}


def write_cache(cache):
    with open(CACHE_FILE, "w") as file:
        json.dump(cache, file, indent=4)


def main():
    user_input = input("Input date (YYYY-mm-dd), Enter- for choice tomorrow: ")

    if user_input.strip() == "":
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        date = user_input.strip()

    cache = read_cache()

    if date in cache:
        print(f"Info from file: {cache[date]}")
    else:
        result = check_rain(date)
        print(f"Result: {result}")

        cache[date] = result
        write_cache(cache)
