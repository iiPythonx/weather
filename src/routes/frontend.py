# Copyright (c) 2023-2024 iiPython

# Modules
from src.app import app, app_root
from starlette.responses import FileResponse

# Routes
@app.get("/")
async def get_index() -> FileResponse:
    return FileResponse(app_root / "src/templates/index.html")
