# Copyright 2023 iiPython

# Modules
import re
from src.app import app, scraper

# Initialization
date_whitelist = r"[^0-9\-]"

# Routes
@app.route("/api/now", methods = ["GET"])
async def get_api_now() -> dict:
    return {
        "status": 200,
        "data": scraper.get_weather_for(scraper.current_key()[:-5])[-1]  # :-5 removes .json
    }

@app.route("/api/past/{date}", methods = ["GET"])
async def get_api_past(date: str) -> dict:
    data = scraper.get_weather_for(re.sub(date_whitelist, "", date))
    return {"status": 200 if data is not None else 404, "data": data}
