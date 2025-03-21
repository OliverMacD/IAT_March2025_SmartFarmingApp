import streamlit as st
from utils.data_loader import load_data
from components.page_help import render_page_help
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta
from components.login import login
from components.websocket_listener import get_latest_data

login()

st.set_page_config(page_title="Analytics & Trends", layout="wide", page_icon="static/Totech_Logo.png")

st.title("📈 Analytics & Trends")
render_page_help("analytics")

# Sidebar logo & styling
user = st.secrets["credentials"]["name"]
with st.sidebar:
    st.image("static/Totech_Logo_W-Name.png", use_container_width=True)
    st.markdown("### SmartFarm App")
    st.markdown(f"Welcome {user}! Use the sidebar to navigate between pages and monitor your farm's health in real-time.")

# Load current data
if st.session_state["ws_started"]:
    data = get_latest_data(fallback_loader=load_data)
else:
    data = load_data()

# Sidebar filters
st.markdown("### Select Data for Trend Analysis")

# Select zones
zone_ids = [z["zone_id"] for z in data["zones"]]
selected_zones = st.multiselect("Select zones to compare", zone_ids, default=zone_ids)

# Select parameter
param_options = {
    "Soil Moisture": ("soil", "moisture", "Moisture (%)"),
    "Soil Temperature": ("soil", "temperature", "Temperature (°C)"),
    "Soil pH": ("soil", "pH", "pH"),
    "Nitrogen (N)": ("soil", "N", "N (ppm)"),
    "Phosphorus (P)": ("soil", "P", "P (ppm)"),
    "Potassium (K)": ("soil", "K", "K (ppm)"),
    "Conductivity": ("soil", "conductivity", "Conductivity (µS/cm)"),
    "Humidity": ("environment", "humidity", "Humidity (%)"),
    "Rainfall": ("environment", "rainfall", "Rainfall (mm)"),
    "Air Temperature": ("environment", "air_temperature", "Air Temp (°C)"),
    "Wind Speed": ("environment", "wind_speed", "Wind Speed (m/s)"),
    "Wind Direction": ("environment", "wind_direction", "Wind Direction (°)"),
    "Solar Radiation": ("environment", "solar_radiation", "Solar Radiation (W/m²)"),
    "Tank Level": ("irrigation", "tank_level", "Tank Level (%)")
}
selected_param = st.selectbox("Select data type", list(param_options.keys()))
category, key, label = param_options[selected_param]

# Time range (mocked for now)
days = st.slider("Number of past days to visualize", 3, 30, 7)
end_date = datetime.now().date()
start_date = end_date - timedelta(days=days)

# Generate mock historical data
history = []
for zone in data["zones"]:
    if zone["zone_id"] not in selected_zones:
        continue
    for d in range(days):
        date = start_date + timedelta(days=d)
        base_val = zone[category][key]
        variation = random.uniform(-5, 5) if isinstance(base_val, (int, float)) else 0
        value = round(base_val + variation, 2)
        history.append({
            "Zone": zone["zone_id"],
            "Date": date,
            "Value": value
        })

df = pd.DataFrame(history)

# Plot trend
st.markdown(f"### {label} Trends Over Time")
fig = px.line(df, x="Date", y="Value", color="Zone", markers=True)
fig.update_layout(yaxis_title=label, xaxis_title="Date", height=500)
st.plotly_chart(fig, use_container_width=True)