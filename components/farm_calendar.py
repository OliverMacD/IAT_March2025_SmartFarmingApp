import streamlit as st
from streamlit_calendar import calendar
import uuid
import datetime
import requests

def render_farm_calendar():
    if "calendar_events" not in st.session_state:
        st.session_state.calendar_events = []
    if "calendar_prefilled" not in st.session_state:
        st.session_state.calendar_prefilled = False
    if "weather_loaded" not in st.session_state:
        st.session_state.weather_loaded = False

    event_meta = {
        "Irrigation": {"title": "💧 Irrigation", "color": "#4FC3F7"},
        "Tank Refill": {"title": "🛢️ Tank Refill", "color": "#9E9E9E"},
        "Restock - Fertilizer": {"title": "🧪 Fertilizer Restock", "color": "#BA68C8"},
        "Restock - Seeds": {"title": "🌱 Seed Restock", "color": "#81C784"},
        "Market Day": {"title": "🛍️ Market Day", "color": "#FFB74D"},
        "Harvest Date": {"title": "🌾 Harvest Date", "color": "#FDD835"},
        "Planting Date": {"title": "🪴 Planting Date", "color": "#AED581"},
        "Weather": {"color": "#90CAF9"}
    }

    if not st.session_state.calendar_prefilled:
        base_date = datetime.date(2025, 4, 1)
        for i in range(0, 30, 3):
            st.session_state.calendar_events.append({
                "id": str(uuid.uuid4()),
                "title": event_meta["Irrigation"]["title"],
                "start": (base_date + datetime.timedelta(days=i)).isoformat(),
                "end": (base_date + datetime.timedelta(days=i)).isoformat(),
                "color": event_meta["Irrigation"]["color"]
            })

        for i in range(0, 30, 7):
            st.session_state.calendar_events.append({
                "id": str(uuid.uuid4()),
                "title": event_meta["Tank Refill"]["title"],
                "start": (base_date + datetime.timedelta(days=i)).isoformat(),
                "end": (base_date + datetime.timedelta(days=i)).isoformat(),
                "color": event_meta["Tank Refill"]["color"]
            })

        st.session_state.calendar_events.extend([
            {"id": str(uuid.uuid4()), "title": event_meta["Restock - Fertilizer"]["title"], "start": "2025-04-08", "end": "2025-04-08", "color": event_meta["Restock - Fertilizer"]["color"]},
            {"id": str(uuid.uuid4()), "title": event_meta["Market Day"]["title"], "start": "2025-04-06", "end": "2025-04-06", "color": event_meta["Market Day"]["color"]},
            {"id": str(uuid.uuid4()), "title": event_meta["Planting Date"]["title"], "start": "2025-04-02", "end": "2025-04-02", "color": event_meta["Planting Date"]["color"]},
            {"id": str(uuid.uuid4()), "title": event_meta["Harvest Date"]["title"], "start": "2025-04-28", "end": "2025-04-28", "color": event_meta["Harvest Date"]["color"]}
        ])
        st.session_state.calendar_prefilled = True

    with st.expander("➕ Add New Event"):
        event_type = st.selectbox("Event Type", list(event_meta.keys())[:-1])  # exclude Weather
        event_date = st.date_input("Event Date", datetime.date(2025, 4, 1))
        if st.button("Add Event"):
            st.session_state.calendar_events.append({
                "id": str(uuid.uuid4()),
                "title": event_meta[event_type]["title"],
                "start": event_date.isoformat(),
                "end": event_date.isoformat(),
                "color": event_meta[event_type]["color"]
            })
            st.success(f"✅ Event '{event_meta[event_type]['title']}' added for {event_date}")

    if not st.session_state.weather_loaded:
        try:
            api_key = st.secrets["api"]["OPENWEATHER_API_KEY"]
            lat, lon = 43.587641, -116.775265
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}"
            response = requests.get(url)
            forecast_data = response.json()

            seen_dates = set()
            for item in forecast_data["list"]:
                dt_txt = item["dt_txt"]
                date = dt_txt.split(" ")[0]
                if date in seen_dates:
                    continue
                seen_dates.add(date)

                weather = item["weather"][0]
                description = weather["main"]
                emoji_map = {
                    "Clear": "☀️", "Clouds": "🌥️", "Rain": "🌧️", "Snow": "❄️",
                    "Thunderstorm": "⛈️", "Drizzle": "🌦️", "Mist": "🌫️", "Fog": "🌫️"
                }
                emoji = emoji_map.get(description, "🌦️")
                title = f"{emoji} {description}"

                st.session_state.calendar_events.append({
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "start": date,
                    "end": date,
                    "color": event_meta["Weather"]["color"]
                })
            st.session_state.weather_loaded = True

        except Exception as e:
            st.error(f"Error loading weather forecast: {e}")

    calendar_options = {
        "initialView": "dayGridMonth",
        "editable": False,
        "height": 600,
        "locale": "en"
    }

    calendar(events=st.session_state.calendar_events, options=calendar_options)