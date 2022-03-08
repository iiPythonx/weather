# Copyright 2022 iiPython

# Modules
import collections
from datetime import datetime

# Utility class
class WeatherUtilities(object):
    def __init__(self) -> None:
        pass

    def convert_time(self, time: str) -> str:
        return datetime.strptime(time, "%H:%M").strftime("%I:%M %p")

    def dayify(self, entries: list) -> dict:
        data = {}
        for entry in entries:
            if entry["date"] not in data:
                data[entry["date"]] = []

            data[entry["date"]].append(entry)

        return collections.OrderedDict(sorted(data.items(), reverse = True))

    def scale_bytes(self, num: int, suffix: str = "B") -> str:
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if abs(num) < 1024:
                return f"{num:3.1f}{unit}{suffix}"

            num /= 1024

        return f"{num:.1f}Y{suffix}"

    def swap_date_format(self, date: str) -> str | None:
        for frmt in ["%m/%d/%y", "%Y-%m-%d"]:
            try:
                return datetime.strptime(date, frmt).strftime("%D")

            except Exception:
                pass

        return None

    def suffix(self, d: int) -> str:
        return "th" if 11 <= d <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")

    def make_data_str(self, data: list, y_cb) -> str:
        return ", ".join([f"{{x: '{self.convert_time(item['time'])}', y: {round(y_cb(item))}}}" for item in data])

    def make_data_strings(self, data: list) -> dict:
        return {
            "temp": self.make_data_str(data, lambda i: i["json"]["main"]["temp"]),
            "humidity": self.make_data_str(data, lambda i: i["json"]["main"]["humidity"]),
            "pressure": self.make_data_str(data, lambda i: round(i["json"]["main"]["pressure"] / 33.86, 2)),
            "wind": self.make_data_str(data, lambda i: i["json"]["wind"]["speed"]),
            "visibility": self.make_data_str(data, lambda i: round(i["json"]["visibility"] / 1609))
        }
