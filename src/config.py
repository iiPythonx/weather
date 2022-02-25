# Copyright 2022 iiPython

# Modules
import os
import json
from typing import Any
from .logging import print_log

# Load config
if not os.path.isfile("config.json"):
    with open("config.json", "w+") as configf:
        configf.write("{}")

    config = {}

else:
    try:
        with open("config.json", "r") as configf:
            config = json.loads(configf.read())

    except Exception:
        print_log("error", "Failed to read from config.json", True)

# Config handlers
def process_key(key: str) -> list:
    return key.split(".")

def get_value(config: dict, key: str) -> Any:
    val = config
    for layer in process_key(key):
        val = val.get(layer)

    return val

def set_value(config: dict, key: str, val: Any) -> None:
    key, parent = process_key(key), config
    for layer in key[:-1]:
        parent = parent[layer]

    parent[key[-1]] = val

# Check required keys
key_data = {
    "main.owm.city_id": {"required": True},
    "main.owm.api_key": {"required": True},
    "main.save_interval": {"default": 10}
}
for key, data in key_data.items():
    value = get_value(config, key)
    if value is None:
        if data.get("required"):
            print_log("error", f"Missing required field '{key}' in config.json!", True)

        elif data.get("default"):
            set_value(config, key, data["default"])

# Custom config class
class Configuration(object):
    def __init__(self, config: dict) -> None:
        self.config = config

    def get(self, key: str) -> Any:
        return get_value(self.config, key)

config = Configuration(config)
