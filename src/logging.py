# Copyright 2022 iiPython

# Modules
from datetime import datetime
try:
    from rich import print
    _is_rich = True

except ImportError:
    _is_rich = False

# Logging handler
def print_log(level: str, message: str, crash: bool = False) -> None:
    time, color = datetime.now().strftime("%I:%M %p"), "[" + {
        "info": "white",
        "warn": "yellow",
        "error": "red"
    }[level] + "]" if _is_rich else ""
    message = f"{color}[{time}] [{level.upper()}]: {message}"
    if _is_rich:
        message += "[/]"

    print(message)
    if crash:
        return exit(1)
