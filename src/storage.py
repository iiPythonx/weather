# Copyright 2023 iiPython

# Modules
import os
import json
import gzip
from typing import List
from requests import get
from datetime import datetime

from .config import config, app_root

# Initialization
database_path = os.path.join(app_root, "db")
if config.get("database_location"):
    database_path = os.path.abspath(config["database_location"])
    if not os.path.isdir(database_path):
        os.makedirs(database_path)
        raise RuntimeError("created database folder, please copy cities.json to it.")

entries_location = os.path.join(database_path, "entries")
if not os.path.isdir(entries_location):
    os.mkdir(entries_location)

# Load openweathermap data
def get_city_info(city_id: int) -> dict:
    try:
        with open(os.path.join(database_path, "cities.json"), "r") as fh:
            return [
                c for c in json.loads(fh.read())
                if c["id"] == owm_cityid
            ][0]

    except (FileNotFoundError, json.JSONDecodeError):
        raise RuntimeError("cities.json file is either missing or corrupted!")

    except IndexError:
        raise RuntimeError(f"Configured city ID ({city_id}) is invalid!")

owm_apikey = config.get("openweather_api_key")
owm_cityid = config.get("openweather_city_id")
if not (owm_apikey and owm_cityid):
    raise RuntimeError("Configuration is missing either openweather_api_key OR openweather_city_id!")

# Request handlers
def make_api_request(endpoint: str, data: dict) -> dict:
    try:
        req = get(
            f"https://api.openweathermap.org/{endpoint}",
            params = data | {"appid": owm_apikey},
            timeout = 5
        )
        if req.status_code == 429:
            return exit("Hit an OpenWeatherMap ratelimit, please adjust scrape interval and restart.")

        return req.json()

    except Exception as e:
        print(f"[-] Caught a '{type(e)}'!")
        return make_api_request(endpoint, data)

# Scraping handlers
class Scraper(object):
    def __init__(self) -> None:
        self.last_path = None
        self.current_scrape, self.data_cache = [], {}

        # Fetch coordinates
        city_data = get_city_info(owm_cityid)["coord"]
        self.lat, self.lon = city_data["lat"], city_data["lon"]

    def current_key(self) -> str:
        return datetime.utcnow().strftime("%m-%d-%y") + ".json"  # 0M-0D-0Y

    def get_weather_for(self, date: str) -> List[dict] | None:
        fp = os.path.join(entries_location, date + ".json")
        for p in [fp, fp + ".gz"]:
            gz = p[-3:] == ".gz"
            if gz and date in self.data_cache:
                return self.data_cache[date]

            elif not os.path.isfile(p):
                continue

            with open(p, "rb") as fh:
                raw = fh.read()
                data = json.loads(raw.decode() if not gz else gzip.decompress(raw).decode())
                if gz:
                    self.data_cache[date] = data

                return data

        return None

    def scrape_weather(self) -> None:
        path = os.path.join(entries_location, self.current_key())
        if (path != self.last_path) and (self.last_path is not None):
            os.remove(self.last_path)
            with open(self.last_path + ".gz", "wb") as fh:  # Convert to a .json.gz
                fh.write(gzip.compress(json.dumps(self.current_scrape).encode("utf8")))

            self.current_scrape = []  # Reset in-memory buffer

        # Read file from disk if we don't have it
        elif (not self.current_scrape) and os.path.isfile(path):
            with open(path, "r") as fh:
                self.current_scrape = json.loads(fh.read())

        # Update on-disk weather
        self.current_scrape.append(make_api_request(
            "data/2.5/weather",
            {"lat": self.lat, "lon": self.lon, "units": "imperial"}
        ))
        with open(path, "w+") as fh:
            fh.write(json.dumps(self.current_scrape))

        self.last_path = path
