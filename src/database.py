# Copyright 2022 iiPython

# Modules
import os
import json
import sqlite3
from datetime import datetime

from .logging import print_log

# Database class
class WeatherDB(object):
    def __init__(self) -> None:
        self.db_path = os.path.abspath("db/weather.db")

        # Connect to db
        self.conn = sqlite3.connect(self.db_path, check_same_thread = False)
        self.conn.row_factory = self.dict_factory
        self.cursor = self.conn.cursor()

        # Initialization
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            date text,
            time text,
            json text
        )
        """)

    def dict_factory(self, cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    def save_db(self) -> None:
        self.conn.commit()

    def append(self, data: dict) -> None:
        data["weather"][0]["description"] = " ".join([d[0].upper() + d[1:] for d in data["weather"][0]["description"].split(" ")])
        dt, data = datetime.now(), json.dumps(data)
        self.cursor.execute("INSERT INTO weather VALUES (?,?,?)", (dt.strftime("%D"), dt.strftime("%H:%M"), data))
        self.save_db()

        print_log("info", f"Wrote {len(data)} bytes of data to weather.db")

    def grab_all(self) -> list:
        self.cursor.execute("SELECT * FROM weather")
        return self.cursor.fetchall()

    def get_date(self, date: str) -> list:
        self.cursor.execute("SELECT * FROM weather WHERE date=?", (date,))
        return self.cursor.fetchall()

    def grab_today(self) -> list:
        return self.get_date(datetime.now().strftime("%D"))
