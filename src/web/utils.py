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
