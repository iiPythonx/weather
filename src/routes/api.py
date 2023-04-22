# Copyright 2023 iiPython

# Modules
import re
import os
from typing import List
from src.app import app, scraper

# Initialization
date_whitelist = r"[^0-9\-]"

# Routes
@app.route("/api/today", methods = ["GET"])
async def get_api_today() -> dict:
    date = scraper.current_key()[:-5]  # :-5 removes .json
    return {"status": 200, "date": date, "data": scraper.get_weather_for(date)}

@app.route("/api/past/{date}", methods = ["GET"])
async def get_api_past(date: str) -> dict:
    data = scraper.get_weather_for(re.sub(date_whitelist, "", date))
    return {"status": 200 if data is not None else 404, "data": data, "date": date}

@app.route("/api/dates", methods = ["GET"])
async def get_dates() -> List[str]:
    return {
        "status": 200,
        "data": sorted(
            [f.split(".")[0] for f in os.listdir(os.path.dirname(scraper.last_path))],
            reverse = True
        )
    }
