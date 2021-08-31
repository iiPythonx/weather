# Copyright 2021 iiPython

# Modules
import os
import sys
import json
import requests
from time import sleep
from datetime import datetime

# Initialization
class Configuration(object):
    def __init__(self, data: dict) -> None:
        self.data = data

    def get(self, key: str) -> any:
        if key in self.data:
            return self.data[key]

        return None

if not os.path.isfile("weather.json"):
    with open("weather.json", "w+") as file:
        file.write("")

    weather = []

else:
    with open("weather.json", "r") as file:
        weather = json.loads(file.read())

    with open("config.json", "r") as cfile:
        config = Configuration(json.loads(cfile.read()))

cityID  = config.get("cityID")
apiKey  = config.get("apiKey")
saveIdx = config.get("saveTime") or 10  # In minutes
saveTmp = 0

# Main loop
while True:

    # Make request to API
    try:
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?id={cityID}&appid={apiKey}&units=metric"
        ).json()

        time = datetime.now()
        req["time"] = time.strftime("%D").replace("/", "-") + "@" + time.strftime("%H:%M")

        if weather[-1]["time"] == req["time"]:
            print("Seems like the script was restarted, skipping current minute.")

        else:
            weather.append(req)

        # Save weather if needed
        if saveTmp == saveIdx:
            with open("weather.json", "w+") as file:
                file.write(json.dumps(weather))

            print("Saved weather.json @", req["time"])
            saveTmp = -1

        print("Fetched weather information for", req["time"])

        sleep(60)  # Once per minute
        saveTmp += 1

    except KeyboardInterrupt:
        with open("weather.json", "w+") as file:
            file.write(json.dumps(weather))

        sys.exit(0)
