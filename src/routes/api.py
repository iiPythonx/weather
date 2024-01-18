# Copyright (c) 2023-2024 iiPython

# Modules
import re
import os
from natsort import natsorted
from typing import List, Dict

from src.app import app, scraper

# Initialization
date_whitelist = r"[^0-9\-]"

# Routes
@app.get("/api/today")
async def get_api_today() -> dict:
    date = scraper.current_key()[:-5]  # :-5 removes .json
    return {"status": 200, "date": date, "data": scraper.current_scrape}

@app.get("/api/past/{date}")
async def get_api_past(date: str) -> dict:
    data = scraper.get_weather_for(re.sub(date_whitelist, "", date))
    return {"status": data and 200 or 404, "data": data, "date": date}

@app.get("/api/dates")
async def get_dates() -> Dict[str, int | List[str]]:
    return {
        "status": 200,
        "data": natsorted(
            [
                f.split(".")[0]
                for f in os.listdir(os.path.dirname(scraper.last_path))
            ],
            reverse = True
        )
    }
