# Copyright 2023 iiPython

# Modules
import sys
import os.path
from os.path import abspath, dirname
if (
    sys.version_info[0] == 3 and
    sys.version_info[1] >= 11
):  # Python 3.11+
    import tomllib as toml

else:
    import toml

# Initialization
app_root = abspath(dirname(dirname(__file__)))
config_file = os.path.join(app_root, "config.toml")

# Load config
if os.path.isfile(config_file):
    with open(config_file, "r") as fh:
        config = toml.loads(fh.read())

else:
    raise RuntimeError("missing configuration file!")
