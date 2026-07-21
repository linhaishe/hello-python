import requests

def get_weather(city):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "current_weather": True,
        "timezone": "Asia/Shanghai"
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    return {
        "city": city["name"],
        "temperature": data["current_weather"]["temperature"],
        "wind_speed": data["current_weather"]["windspeed"],
        "time": data["current_weather"]["time"]
    }



def fetch_all_weather(cities):

    weather_reports = []

    for city in cities:
        weather = get_weather(city)
        weather_reports.append(weather)

    return weather_reports
    

