import requests
import datetime

def fetch_openweather_forecast(api_key, lat, lon):
    url = (
        f"https://pro.openweathermap.org/data/2.5/forecast/climate?"
        f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching weather: {response.text}")
    data = response.json()
    
    forecast_data = []
    for day in data.get("list", []):
        date = datetime.datetime.fromtimestamp(day["dt"]).date()
        description = day["weather"][0]["description"].capitalize()
        forecast_data.append({
            "date": date,
            "description": description
        })
    return forecast_data