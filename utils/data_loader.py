import json

def load_data():
    with open("data/mock_data.json") as f:
        return json.load(f)

def load_calendar_data():
    return {
        "2025-03-21": ["Irrigation - Zone A", "Forecast: Rain"],
        "2025-03-22": ["No irrigation scheduled"]
    }