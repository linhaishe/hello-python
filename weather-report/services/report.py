import csv
import os
from datetime import datetime


today = datetime.now().strftime("%Y-%m-%d")

folder = f"./reports/{today}"

if not os.path.exists(folder):
    os.makedirs(folder)

filename = f"{folder}/weather_report.csv"

def save_csv(weather_list):

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=weather_list[0].keys()
        )

        writer.writeheader()

        writer.writerows(weather_list)