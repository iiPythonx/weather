# Copyright 2022 iiPython

# Modules
import os
import json
from . import app, rpath
from ..config import config
from datetime import datetime
from flask import abort, request, redirect, render_template, send_from_directory

# Routes
@app.route("/")
def index() -> None:
    return render_template("public/index.html", date = datetime.now().strftime("%D")), 200

@app.route("/historical")
def historical() -> None:
    return render_template("public/historical.html", data = app.utils.dayify(app.db.grab_all())), 200

@app.route("/config")
def config_page() -> None:
    return render_template(
        "public/config.html",
        length = len(app.db.grab_all()),
        size = app.utils.scale_bytes(os.path.getsize("db/weather.db")),
        config = config
    ), 200

@app.route("/widgets/weather")
def weather_widget() -> None:
    date = app.utils.swap_date_format(request.args.get("date"))
    data = [d | {"json": json.loads(d["json"])} for d in app.db.get_date(date)]
    if not data:
        return render_template("errors/404.html", error = "No data exists for the provided date.", widget = True), 200

    date = datetime.strptime(date, "%m/%d/%y")
    data = {
        "data": ([e for e in data if e["time"] == request.args.get("time")] or [data[-1]])[0],
        "date": date.strftime("%A, %B %-d{} %Y").format(app.utils.suffix(date.day)),
        "json": app.utils.make_data_strings(data)
    }

    # Send template
    return render_template("widgets/weather.html", data = data, widget = True)

@app.route("/s/<path:path>")
def send_static_file(path: str) -> None:
    return send_from_directory(rpath("static"), path, conditional = True)

# Error handlers
@app.errorhandler(404)
def handle404(e: Exception) -> None:
    return render_template("errors/404.html"), 404
