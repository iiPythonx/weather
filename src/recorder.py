# Copyright 2022 iiPython

# Modules
import json
import requests
from time import sleep
from urllib.parse import urlencode
from multiprocessing import Process

from .web import app
from .config import config
from .logging import print_log
from .database import WeatherDB

# Recorder class
class WeatherRecorder(object):
    def __init__(self) -> None:
        self.db = WeatherDB()
        self.config = config

        # Configuration
        self.api_key = config.get("main.owm.api_key")
        self.city_id = config.get("main.owm.city_id")

        # Load city name, coords, etc
        self.city_dt = self.get_city_data()

        # Server website
        self.ws = None
        addr = config.get("web.addr")
        if addr:
            app.db = self.db
            self.ws = Process(target = app.run, kwargs = {"host": addr[0], "port": addr[1]})
            self.ws.start()

    def make_request(self, endpoint: str, data: dict = {}) -> dict:
        try:
            req = requests.get(f"https://api.openweathermap.org/{endpoint}?{urlencode(data | {'appid': self.api_key})}", timeout = 5)
            if req.status_code == 429:
                print_log("warn", "Hit an OWM ratelimit, retrying request in 10 minutes ...")
                sleep(600)
                return self.make_request(endpoint, data)

            return req.json()

        except Exception:
            print_log("warn", "Request failed for unknown reason, retrying request in 5 minutes ...")
            sleep(300)
            return self.make_request(endpoint, data)

    def get_city_data(self) -> dict:
        with open("db/cities.json", "r") as f:
            cities = json.loads(f.read())

        city = [c for c in cities if c["id"] == self.city_id][0]
        del cities
        return city

    def start(self) -> None:
        print_log("info", f"Recording {self.city_dt['name']}, {self.city_dt['state']} ({self.city_id})")
        print_log("info", f"Coordinates: {self.city_dt['coord']['lat']}, {self.city_dt['coord']['lon']}")
        try:
            while True:
                self.db.append(self.make_request("data/2.5/weather", {
                    "lat": self.city_dt["coord"]["lat"],
                    "lon": self.city_dt["coord"]["lon"],
                    "units": "imperial"
                }))
                sleep(self.config.get("main.save_interval") * 60)

        except KeyboardInterrupt:
            if self.ws is not None:
                print_log("info", "Waiting for webserver to terminate ...")
                self.ws.terminate()
                self.ws.join()

            self.db.save_db()
