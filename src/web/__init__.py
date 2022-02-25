# Copyright 2022 iiPython

# Modules
import os
import sys
import logging
from flask import Flask

from .utils import WeatherUtilities

# Initialization
def rpath(path: str) -> None:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

logging.getLogger("werkzeug").setLevel(logging.CRITICAL)
sys.modules["flask.cli"].show_server_banner = lambda *x: None

app = Flask(
    "Weather Recorder",
    template_folder = rpath("templates")
)
app.utils = WeatherUtilities()

# Jinja env
@app.context_processor
def add_globals() -> dict:
    return {k: getattr(app.utils, k) for k in dir(app.utils) if k[0] != "_"}

# Routes
from .routes import *
