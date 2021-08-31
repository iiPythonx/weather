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

def key_get_dict(d: dict, key: str) -> any:
    val = d
    for i in key.split("."):
        val = val[i]

    return val

clear = lambda: subprocess.run(["cls" if os.name == "nt" else "clear"], shell = True)  # noqa

# Initialization
try:
    date = datetime.strptime(input("Enter date: "), "%m-%d-%y").strftime("%m-%d-%y")

except Exception:
    close_script(1, "[red]Invalid date. Format: `01-01-21`")

datakeys = {
    "Temperature (Celsius)": {"key": "main.temp", "func": lambda x: x, "short": "celsius"},
    "Temperature (Fahrenheit)": {"key": "main.temp", "func": lambda x: x * (9 / 5) + 32, "short": "fahrenheit"},
    "Humidity": {"key": "main.humidity", "func": lambda x: x, "short": "humidity"},
    "Air Pressure": {"key": "main.pressure", "func": lambda x: x, "short": "pressure"},
    "Temp Max (Celsius)": {"key": "main.temp_max", "func": lambda x: x, "short": "maxc"},
    "Temp Max (Fahrenheit)": {"key": "main.temp_max", "func": lambda x: x * (9 / 5) + 32, "short": "maxf"},
    "Temp Min (Celsius)": {"key": "main.temp_min", "func": lambda x: x, "short": "minc"},
    "Temp Min (Fahrenheit)": {"key": "main.temp_min", "func": lambda x: x * (9 / 5) + 32, "short": "minf"},
}
showInterval = 1  # Show every 10 minutes
showXLabel = False
showIndex = showInterval

# Load weather
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
    x, y, xlabel = [], [], []
    for minute in weather:
        if not minute["time"].startswith(date):
            continue

        # Handle interval
        if showIndex != showInterval:
            showIndex += 1
            continue

        showIndex = 0

        # Handle plotting
        time = minute["time"].split("@")[1]
        x.append(time_to_int(time))
        y.append(datakey_handler["func"](key_get_dict(minute, datakey_handler["key"])))

        if showXLabel:
            xlabel.append(time)

    # Begin plotting
    plt.xlabel("Time")
    plt.ylabel(datakey_label)
    if xlabel:
        plt.xticks(x, xlabel)

    plt.plot(x, y)

    plt.title(date)
    plt.show()
