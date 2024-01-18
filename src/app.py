# Copyright (c) 2023-2024 iiPython

# Modules
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every

from .storage import Scraper
from .config import config, app_root

# Initialization
app = FastAPI()
app.mount("/static", StaticFiles(directory = app_root / "src/static"), name = "static")

# Handle periodic scraping
scraper = Scraper()
interval = config.get("scrape_interval", 10) * 60

@app.on_event("startup")
@repeat_every(seconds = interval)
def handle_weather_scrape() -> None:
    scraper.scrape_weather()

# Routes
from .routes import (api, frontend)  # noqa
