import streamlit as st
from utils.data_loader import load_data
from components.cards import render_summary_cards
from components.graphs import render_moisture_graph
import pandas as pd
import plotly.express as px
from components.page_help import render_page_help
from components.login import login
from components.websocket_listener import start_websocket
from components.websocket_listener import get_latest_data

login()

# Start Ws on first load
if "ws_started" not in st.session_state:
    start_websocket("ws://localhost:8765")
    st.session_state["ws_started"] = True

st.set_page_config(
    page_title="SmartFarm Dashboard",
    page_icon="static/Totech_Logo.png",
    layout="wide"
)

# Sidebar logo & styling
user = st.secrets["credentials"]["name"]
with st.sidebar:
    st.image("static/Totech_Logo_W-Name.png", use_container_width=True)
    st.markdown("### SmartFarm App")
    st.markdown(f"Welcome {user}! Use the sidebar to navigate between pages and monitor your farm's health in real-time.")

# Load farm data
if st.session_state["ws_started"]:
    data = get_latest_data(fallback_loader=load_data)
else:
    data = load_data()

st.title("🌾 SmartFarm Dashboard")
render_page_help("home") 

# Summary cards
st.markdown("## Overview")
render_summary_cards(data)

# Zone comparison chart
st.markdown("## 📊 Compare Zones")

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

selected_param = st.selectbox("Select parameter to compare across zones", list(param_options.keys()))
category, key, label = param_options[selected_param]

# Create dataframe for plotting
df = pd.DataFrame([
    {
        "Zone": zone["zone_id"],
        "Value": zone[category][key]
    }
    for zone in data["zones"]
])

# Plot
fig = px.bar(df, x="Zone", y="Value", color="Zone", title=f"{label} by Zone")
fig.update_layout(yaxis_title=label)
st.plotly_chart(fig, use_container_width=True)