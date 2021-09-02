# Copyright 2021 iiPython

# Modules
import os
import sys
import json
import subprocess
from rich import print
from datetime import datetime
import matplotlib.pyplot as plt

# Function definitions
def close_script(code: int, message: str) -> None:
    print("\n", message, sep = "")
    sys.exit(code)

def time_to_int(time: str) -> int:
    data = time.split(":")
    return (int(data[0]) * 60) + int(data[1])

def time_to_date(time: str) -> str:
    return time.split("@")[0].replace("-", "/")

def key_get_dict(d: dict, key: str) -> any:
    val = d
    for i in key.split("."):
        val = val[i]

    return val

clear = lambda: subprocess.run(["cls" if os.name == "nt" else "clear"], shell = True)  # noqa

# Initialization
class Configuration(object):
    def __init__(self, data: dict) -> None:
        self.data = data

    def get(self, key: str) -> any:
        if key in self.data:
            return self.data[key]

        return None

if os.path.isfile("config.json"):
    with open("config.json", "r") as cfile:
        config = json.loads(cfile.read())

    if "graph" in config:
        config = config["graph"]

    config = Configuration(config)

else:
    config = Configuration({})

datakeys = {
    "Temperature (Celsius)": {"key": "main.temp", "func": lambda x: x, "short": "celsius"},
    "Temperature (Fahrenheit)": {"key": "main.temp", "func": lambda x: x * (9 / 5) + 32, "short": "fahrenheit"},
    "Humidity": {"key": "main.humidity", "func": lambda x: x, "short": "humidity"},
    "Air Pressure": {"key": "main.pressure", "func": lambda x: x, "short": "pressure"},
    "Sea Level": {"key": "main.sea_level", "func": lambda x: x, "short": "slvl"},
    "Wind Speed (mph)": {"key": "wind.speed", "func": lambda x: round(x / 1.467, 2), "short": "wspeed"},
    "Temp Max (Celsius)": {"key": "main.temp_max", "func": lambda x: x, "short": "maxc"},
    "Temp Max (Fahrenheit)": {"key": "main.temp_max", "func": lambda x: x * (9 / 5) + 32, "short": "maxf"},
    "Temp Min (Celsius)": {"key": "main.temp_min", "func": lambda x: x, "short": "minc"},
    "Temp Min (Fahrenheit)": {"key": "main.temp_min", "func": lambda x: x * (9 / 5) + 32, "short": "minf"},
}
showInterval = config.get("showInterval") or 10
showXLabel = config.get("showXLabel")
showIndex = showInterval
showAllData = config.get("showAllData") or False

# Load weather
if not showAllData:
    try:
        date = datetime.strptime(input("Enter date: "), "%m-%d-%y").strftime("%m-%d-%y")

    except Exception:
        close_script(1, "[red]Invalid date. Format: `01-01-21`")

try:
    with open("weather.json", "r") as file:
        weather = json.loads(file.read())

except (json.JSONDecodeError, FileNotFoundError):
    close_script(1, "[red]Failed to load weather data.")

# Handle datakey
while True:
    datakey_handler, datakey_label = None, None
    while True:
        clear()
        print(f"[green]Successfully loaded {len(weather)} minute(s) of weather data.")
        print("Available data:\n", "".join("  " + _ + f" \\[{datakeys[_]['short']}]\n" for _ in datakeys), sep = "")
        try:
            key = input("> ")

        except KeyboardInterrupt:
            close_script(1, "\n[red]Retrieval canceled.")

        for datakey in datakeys:
            if key == datakeys[datakey]["short"]:
                datakey_handler = datakeys[datakey]
                datakey_label = datakey

        if datakey_handler:
            break

    # Handle weather
    x, y, xlabel, xx = [], [], [], 1
    for minute in weather:
        if not showAllData and not minute["time"].startswith(date):
            continue

        # Handle interval
        if showIndex != showInterval:
            showIndex += 1
            continue

        showIndex = 0

        # Handle plotting
        time = minute["time"].split("@")[1]
        if showAllData:
            x.append(xx)
            xx += 1

        else:
            x.append(time_to_int(time))
        y.append(datakey_handler["func"](key_get_dict(minute, datakey_handler["key"])))

        if showXLabel is None or showXLabel:
            xlabel.append(time)

        else:
            xlabel.append(time_to_int(time))

    # Begin plotting
    plt.xlabel("Time")
    plt.ylabel(datakey_label)
    if xlabel and not showAllData:
        plt.xticks(x, xlabel)

    plt.plot(x, y, color = config.get("lineColor") or "blue")
    if config.get("showMarker") or config.get("showMarker") is None:
        plt.hlines(range(round(min(y)), round(max(y))), min(x), max(x), colors = [config.get("markerColor") or "#C0C0C0"])

    plt.title(date if not showAllData else f"{time_to_date(weather[0]['time'])}-{time_to_date(weather[-1]['time'])}")
    plt.show()
