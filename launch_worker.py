# Copyright 2023 iiPython

# Modules
import os
from src.app import app

# Launch debug server
import uvicorn
uvicorn.run(
    app,
    host = os.getenv("HOST", "0.0.0.0"),
    port = int(os.getenv("PORT", 8080)),
    log_level = "info"
)
