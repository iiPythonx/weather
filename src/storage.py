# Copyright (c) 2023-2024 iiPython

# Modules
import os
import time
import json
import gzip
from typing import List
from pathlib import Path
from datetime import datetime

from requests import get

from .config import config, app_root

# Initialization
database_path = Path(config.get("database_location") or os.path.join(app_root, "db"))
if not database_path.is_dir():
    os.makedirs(database_path)
    raise RuntimeError("created database folder, please copy cities.json to it.")

entries_location = database_path / "entries"
if not entries_location.is_dir():
    os.mkdir(entries_location)

# Load openweathermap data
def get_city_info(city_id: int) -> dict:
    try:
        with open(database_path / "cities.json", "r") as fh:
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
        print(f"[-] Caught a '{type(e)}'! Trying again in 5 seconds ...")
        time.sleep(5)
        return make_api_request(endpoint, data)

# Scraping handlers
class Scraper(object):
    def __init__(self) -> None:
        self.last_path = entries_location / self.current_key()
        self.current_scrape, self.data_cache = [], {}

        # Fetch coordinates
        city_data = get_city_info(owm_cityid)["coord"]
        self.lat, self.lon = city_data["lat"], city_data["lon"]

    def current_key(self) -> str:
        return datetime.utcnow().strftime("%m-%d-%y") + ".json"  # 0M-0D-0Y

    def get_weather_for(self, date: str) -> List[dict] | None:
        fp = entries_location / (date + ".json.gz")
        cache_data = self.data_cache.get(date)
        if cache_data is not None:
            return cache_data

        elif not fp.is_file():

            # Check if theres an active .json file
            fp_json = entries_location / (date + ".json")
            if fp_json.is_file():
                with fp_json.open("rb") as fh:
                    json_string = fh.read()
                    json_data = json.loads(json_string)

                if fp_json.name != self.current_key():
                    self.data_cache[date] = json_data
                    with fp.open("wb") as fh:
                        fh.write(gzip.compress(json_string))

                    os.remove(fp_json)
                    print(f"[-] File '{fp_json.name}' was not previously closed. File has been fixed.")
                    return self.data_cache[date]

                return json_data

            return None  # Otherwise this date doesn't exist

        with open(fp, "rb") as fh:
            data = json.loads(gzip.decompress(fh.read()).decode())
            self.data_cache[date] = data
            return data

    def minify(self, data: dict) -> dict:
        return {
            "desc": data["weather"][0]["description"],
            "wspeed": data["wind"]["speed"]
        } | {k: data["main"][k] for k in ["temp", "pressure", "humidity"]}

    def scrape_weather(self) -> None:
        path = entries_location / self.current_key()
        if (path != self.last_path) and (self.last_path is not None):
            os.remove(self.last_path)
            with open(self.last_path.with_suffix(".json.gz"), "wb") as fh:  # Convert to a .json.gz
                fh.write(gzip.compress(json.dumps(self.current_scrape).encode("utf8")))

            self.current_scrape = []  # Reset in-memory buffer

        # Read file from disk if we don't have it
        elif (not self.current_scrape) and path.is_file():
            with open(path, "r") as fh:
                self.current_scrape = json.loads(fh.read())

        # Update on-disk weather
        self.current_scrape.append(self.minify(make_api_request(
            "data/2.5/weather",
            {"lat": self.lat, "lon": self.lon, "units": "imperial"}
        )))
        self.current_scrape[-1]["time"] = datetime.utcnow().strftime("%H:%M")
        with open(path, "w+") as fh:
            fh.write(json.dumps(self.current_scrape))

        self.last_path = path
