import requests
import json
import os
from datetime import datetime, timedelta


class WeatherForecast:
    def __init__(self, cache_file="weather_cache.json"):
        self.cache_file = cache_file
        self._data = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self._data, f, indent=4)

    def __setitem__(self, date, forecast):
        self._data[date] = forecast
        self._save_cache()

    def __getitem__(self, date):
        return self._data.get(date, None)

    def __iter__(self):
        return iter(self._data.keys())

    def items(self):
        for date, forecast in self._data.items():
            yield date, forecast

    def fetch_weather(self, latitude, longitude, date):
        if date in self._data:
            print(f"Fetching from cache for {date}")
            return self._data[date]

        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if "daily" in data and "precipitation_sum" in data["daily"]:
                precipitation = data["daily"]["precipitation_sum"][0]
                self[date] = precipitation  # Save to cache via __setitem__
                return precipitation
        except requests.RequestException as e:
            print(f"API request error: {e}")
            return None
        return None


def interpret_precipitation(value):
    if value is None or value < 0:
        return "I don't know"
    elif value == 0.0:
        return "It will not rain"
    else:
        return f"It will rain ({value} mm)"


def get_date_from_user():
    user_input = input("Enter a date: ").strip()
    if user_input == "":
        return (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    try:
        datetime.strptime(user_input, "%Y-%m-%d")
        return user_input
    except ValueError:
        print("Invalid format. Use YYYY-mm-dd.")
        return get_date_from_user()


def main():
    weather_forecast = WeatherForecast()

    date = get_date_from_user()
    try:
        latitude = float(input("Enter latitude:") or 51.5074)
        longitude = float(input("Enter longitude:") or -0.1278)
    except ValueError:
        print("Invalid input. Using London by default.")
        latitude, longitude = 51.5074, -0.1278

    precipitation = weather_forecast.fetch_weather(latitude, longitude, date)
    print(f"Weather on {date}: {interpret_precipitation(precipitation)}")

    # Example usage of custom methods
    print("\nDates with known forecasts:")
    for d in weather_forecast:  # __iter__
        print(d)

    print("\nAll forecasts:")
    for d, w in weather_forecast.items():  # items()
        print(d, "->", interpret_precipitation(w))


if __name__ == "__main__":
    main()
