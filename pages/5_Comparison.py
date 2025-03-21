import streamlit as st
from utils.data_loader import load_data
from components.page_help import render_page_help
import pandas as pd
import plotly.express as px
import copy
from components.login import login
from components.websocket_listener import get_latest_data

login()

st.set_page_config(page_title="Farm Comparison", layout="wide", page_icon="static/Totech_Logo.png")

st.title("🔄 Farm Comparison")
render_page_help("comparison")

# Sidebar logo & styling
user = st.secrets["credentials"]["name"]
with st.sidebar:
    st.image("static/Totech_Logo_W-Name.png", use_container_width=True)
    st.markdown("### SmartFarm App")
    st.markdown(f"Welcome {user}! Use the sidebar to navigate between pages and monitor your farm's health in real-time.")

# Load current data
if st.session_state["ws_started"]:
    current_data = get_latest_data(fallback_loader=load_data)
else:
    current_data = load_data()

# Load past season mock data (for example, last year)
# Here we simulate by modifying current values slightly
past_data = {"zones": []}
for zone in current_data["zones"]:
    old_zone = copy.deepcopy(zone)
    for k in old_zone["soil"]:
        if isinstance(old_zone["soil"][k], (int, float)):
            old_zone["soil"][k] *= 0.95  # simulate slightly less performance last season
    for k in old_zone["environment"]:
        if isinstance(old_zone["environment"][k], (int, float)):
            old_zone["environment"][k] *= 0.9
    for k in old_zone["irrigation"]:
        if isinstance(old_zone["irrigation"][k], (int, float)):
            old_zone["irrigation"][k] *= 0.85
    past_data["zones"].append(old_zone)

# Parameter options
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
    "Solar Radiation": ("environment", "solar_radiation", "Solar Radiation (W/m²)"),
    "Tank Level": ("irrigation", "tank_level", "Tank Level (%)")
}
selected_param = st.selectbox("Select parameter to compare between seasons", list(param_options.keys()))
category, key, label = param_options[selected_param]

# Build dataframe
rows = []
for zone in current_data["zones"]:
    rows.append({
        "Zone": zone["zone_id"],
        "Season": "Current Season",
        "Value": zone[category][key]
    })
for zone in past_data["zones"]:
    rows.append({
        "Zone": zone["zone_id"],
        "Season": "Last Season",
        "Value": zone[category][key]
    })
df = pd.DataFrame(rows)

# Plot
st.markdown(f"### {label} by Zone – Current vs. Last Season")
fig = px.bar(df, x="Zone", y="Value", color="Season", barmode="group", height=500)
fig.update_layout(yaxis_title=label)
st.plotly_chart(fig, use_container_width=True)