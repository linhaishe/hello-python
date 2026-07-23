from api.weather import fetch_all_weather
from services.report import save_csv, save_sqlite
from constants import CITIES

data = fetch_all_weather(CITIES)
# save_csv(data)
save_sqlite(data)
