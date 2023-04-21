# Copyright 2023 iiPython

# Modules
import asyncio
from blacksheep import Application

from .config import config
from .storage import Scraper

# Initialization
app = Application()

# Handle periodic scraping
scraper = Scraper()  # noqa
async def scrape_task(app: Application) -> None:
    interval = config.get("scrape_interval", 10) * 60
    while True:
        scraper.scrape_weather()
        await asyncio.sleep(interval)

async def configure_scraper(app: Application) -> None:
    asyncio.get_event_loop().create_task(scrape_task(app))

app.on_start += configure_scraper

# Routes
from .routes import (api, frontend)  # noqa
