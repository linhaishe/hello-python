import csv
import sqlite3
from datetime import datetime
from pathlib import Path

# 基于脚本目录而不是当前工作目录。
today = datetime.now().strftime("%Y-%m-%d")
base_dir = Path(__file__).resolve().parent.parent
folder = base_dir / "reports" / today
folder.mkdir(parents=True, exist_ok=True)

csv_filename = folder / "weather_report.csv"
sqlite_filename = folder / "weather_report.db"

def save_csv(weather_list):
    if not weather_list:
        return

    with csv_filename.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=weather_list[0].keys()
        )
        writer.writeheader()
        writer.writerows(weather_list)


def save_sqlite(weather_list):
    if not weather_list:
        return

    with sqlite3.connect(sqlite_filename) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_reports (
                city TEXT,
                temperature REAL,
                wind_speed REAL,
                time TEXT
            )
            """
        )
        conn.execute("DELETE FROM weather_reports")
        conn.executemany(
            "INSERT INTO weather_reports (city, temperature, wind_speed, time) VALUES (?, ?, ?, ?)",
            [
                (
                    report.get("city"),
                    report.get("temperature"),
                    report.get("wind_speed"),
                    report.get("time"),
                )
                for report in weather_list
            ],
        )
