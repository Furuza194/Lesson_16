import json
import os
from json import JSONDecodeError


class WeatherForecast:
    def __init__(self, filename="weather_data.json"):
        self.filename = filename
        self._forecasts = self._load_forecasts()

    def _load_forecasts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}


    def _save_forecasts(self):
        with open(self.filename, "w") as f:
            json.dump(self._forecasts, f)

    def __setitem__(self, date, weather):
        self._forecasts[date] = weather
        self._save_forecasts()

    def __getitem__(self, date):
        return self._forecasts.get(date, "No forecast available")

    def __iter__(self):
        return iter(self._forecasts)

    def items(self):
        return ((date, weather) for date, weather in self._forecasts.items())

forecast = WeatherForecast()

forecast["2025-07-22"] = "Rainy"
forecast["2025-07-23"] = "Sunny"

for date in forecast:
    print(f"The {date} is {forecast[date]}")

