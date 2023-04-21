# Copyright 2023 iiPython

# Modules
from src.app import app, render

# Routes
@app.route("/", methods = ["GET"])
async def get_index() -> None:
    return render("index.html", {})
