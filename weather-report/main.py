from api.weather import fetch_all_weather
from services.parser import clean_weather
from services.report import save_csv
from constants import CITIES

data = fetch_all_weather(CITIES)
save_csv(data)