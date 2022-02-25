# Copyright 2022 iiPython

# Modules
import os
import json
from . import app, rpath
from ..config import config
from datetime import datetime
from flask import abort, request, render_template, send_from_directory

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
    date = request.args.get("date")
    data = [d | {"json": json.loads(d["json"])} for d in app.db.get_date(date)]
    if not data:
        return abort(404)

    def suffix(d: int) -> str:
        return "th" if 11 <= d <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")

    def make_data_str(data: list, y_cb) -> str:
        return ", ".join([f"{{x: '{app.utils.convert_time(item['time'])}', y: {round(y_cb(item))}}}" for item in data])

    date = datetime.now().strptime(date, "%m/%d/%y")
    return render_template(
        "widgets/weather.html",
        data = data,
        last = ([e for e in data if e["time"] == request.args.get("time")] or [data[-1]])[0],
        date = date.strftime("%A, %B %-d{} %Y").format(suffix(date.day)),
        strings = {
            "temp": make_data_str(data, lambda i: i["json"]["main"]["temp"]),
            "humidity": make_data_str(data, lambda i: i["json"]["main"]["humidity"]),
            "pressure": make_data_str(data, lambda i: round(i["json"]["main"]["pressure"] / 33.86, 2)),
            "wind": make_data_str(data, lambda i: i["json"]["wind"]["speed"]),
            "visibility": make_data_str(data, lambda i: round(i["json"]["visibility"] / 1609))
        },
        widget = True
    ), 200

@app.route("/s/<path:path>")
def send_static_file(path: str) -> None:
    return send_from_directory(rpath("static"), path, conditional = True)
