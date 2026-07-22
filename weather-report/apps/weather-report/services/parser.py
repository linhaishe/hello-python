def get_weather_status(code):
    mapping = {
        0: "Sunny",
        1: "Mostly Sunny",
        2: "Partly Cloudy",
        3: "Cloudy",
        61: "Rain"
    }

    return mapping.get(
        code,
        "Unknown"
    )

def clean_weather(data):
    """
    清洗天气数据
    """
    print(data)
    # current = data.get("current_weather", {})
    
    # code = current.get("weathercode")
    # weather = {
    #     # "city": current.get("city", "").strip(),
    #     "city": 'HZ',
    #     "time": current.get("time"),
    #     "temperature": int(
    #         current.get("temperature", 0)
    #     ),
    #     "weather": get_weather_status(code),
    #     "windspeed": current.get(
    #         "windspeed",
    #         0
    #     )
    # }


    return weather