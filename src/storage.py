# Copyright 2023 iiPython

# Modules
import os
# import gzip
# from requests import get

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

print(config, app_root)
