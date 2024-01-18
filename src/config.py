# Copyright (c) 2023-2024 iiPython

# Modules
import sys
from pathlib import Path

if (
    sys.version_info[0] == 3 and
    sys.version_info[1] >= 11
):  # Python 3.11+
    import tomllib as toml

else:
    import toml

# Initialization
app_root = Path(__file__).parents[1]
config_file = app_root / "config.toml"

# Load config
if config_file.is_file():
    with config_file.open("r") as fh:
        config = toml.loads(fh.read())

else:
    raise RuntimeError("missing configuration file!")
