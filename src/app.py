# Copyright 2023 iiPython

# Modules
import os
import asyncio
from jinja2 import FileSystemLoader
from blacksheep import Application
from blacksheep.server.templating import use_templates

from .storage import Scraper
from .config import config, app_root

# Initialization
app = Application()
app.serve_files(os.path.join(app_root, "src/static"), root_path = "static")
render = use_templates(
    app,
    loader = FileSystemLoader(os.path.join(app_root, "src/templates"))
)

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
