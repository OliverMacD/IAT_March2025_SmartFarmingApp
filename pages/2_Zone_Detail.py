import streamlit as st
from utils.data_loader import load_data
import plotly.express as px
import pandas as pd
from components.page_help import render_page_help
from components.login import login
from components.websocket_listener import get_latest_data

login()

st.set_page_config(page_title="Zone Detail", layout="wide", page_icon="static/Totech_Logo.png")
st.title("📍 Zone Detail View")
render_page_help("zone")

# Sidebar logo & styling
user = st.secrets["credentials"]["name"]
with st.sidebar:
    st.image("static/Totech_Logo_W-Name.png", use_container_width=True)
    st.markdown("### SmartFarm App")
    st.markdown(f"Welcome {user}! Use the sidebar to navigate between pages and monitor your farm's health in real-time.")

if st.session_state["ws_started"]:
    data = get_latest_data(fallback_loader=load_data)
else:
    data = load_data()
    
zone = st.selectbox("Select Zone", [z["zone_id"] for z in data["zones"]])
selected_zone = next(z for z in data["zones"] if z["zone_id"] == zone)

st.subheader(f"Zone: {selected_zone['zone_id']} ({selected_zone['crop_type']})")

# --- Color Functions ---
def rgba(hex_color): return hex_color + "40"

def moisture_color(val):
    return f"background-color: {rgba('#ff0000')};" if val < 20 else f"background-color: {rgba('#ffff00')};" if val < 30 else f"background-color: {rgba('#00cc44')};"

def pH_color(val):
    return f"background-color: {rgba('#ff0000')};" if val < 6.0 else f"background-color: {rgba('#00cc44')};" if val < 7.5 else f"background-color: {rgba('#0066ff')};"

def temp_color(val):
    return f"background-color: {rgba('#0066ff')};" if val < 15 else f"background-color: {rgba('#ffffff')};" if val < 22 else f"background-color: {rgba('#ff0000')};"

def humidity_color(val):
    return f"background-color: {rgba('#cccccc')};" if val < 50 else f"background-color: {rgba('#0066ff')};"

def rainfall_color(val):
    return f"background-color: {rgba('#cccccc')};" if val < 1 else f"background-color: {rgba('#0066ff')};"

def solar_color(val):
    return f"background-color: {rgba('#ffff00')};" if val < 650 else f"background-color: {rgba('#ff9900')};" if val < 700 else f"background-color: {rgba('#ff0000')};"

def static_color(c): return f"background-color: {rgba(c)};"

# --- Grid Display with Colored Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div style='{moisture_color(selected_zone['soil']['moisture'])} padding: 1rem; border-radius: 10px; text-align: center;'>"
                f"<h4>Soil Moisture</h4><h2>{selected_zone['soil']['moisture']}%</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='{pH_color(selected_zone['soil']['pH'])} padding: 1rem; border-radius: 10px; text-align: center;'>"
                f"<h4>Soil pH</h4><h2>{selected_zone['soil']['pH']}</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='{static_color('#f2f0f7')} padding: 1rem; border-radius: 10px; text-align: center;'>"
                f"<h4>N</h4><h2>{selected_zone['soil']['N']} ppm</h2></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div style='{temp_color(selected_zone['soil']['temperature'])} padding: 1rem; border-radius: 10px; text-align: center;'>"
                f"<h4>Soil Temp</h4><h2>{selected_zone['soil']['temperature']} °C</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='{static_color('#fff5eb')} padding: 1rem; border-radius: 10px; text-align: center;'>"
                f"<h4>P</h4><h2>{selected_zone['soil']['P']} ppm</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='{static_color('#cc6699')} padding: 1rem; border-radius: 10px; text-align: center;'>"
                f"<h4>Conductivity</h4><h2>{selected_zone['soil']['conductivity']} µS/cm</h2></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div style='{temp_color(selected_zone['environment']['air_temperature'])} padding: 1rem; border-radius: 10px; text-align: center;'>"
                f"<h4>Air Temp</h4><h2>{selected_zone['environment']['air_temperature']} °C</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='{humidity_color(selected_zone['environment']['humidity'])} padding: 1rem; border-radius: 10px; text-align: center;'>"
                f"<h4>Humidity</h4><h2>{selected_zone['environment']['humidity']}%</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='{static_color('#f7fbff')} padding: 1rem; border-radius: 10px; text-align: center;'>"
                f"<h4>K</h4><h2>{selected_zone['soil']['K']} ppm</h2></div>", unsafe_allow_html=True)

st.markdown("### Rainfall and Wind")
st.write(f"Rainfall (last 24h): {selected_zone['environment']['rainfall']} mm")
st.write(f"Wind Speed: {selected_zone['environment']['wind_speed']} m/s")
st.write(f"Wind Direction: {selected_zone['environment']['wind_direction']}°")

# Map with parameter selector
st.markdown("### Sensor Map for This Zone")

param_options = {
    "Soil Moisture": ("soil", "moisture", "Moisture (%)", ["red", "yellow", "green"]),
    "Soil pH": ("soil", "pH", "pH", ["red", "green", "blue"]),
    "Soil Temperature": ("soil", "temperature", "Soil Temp (°C)", ["blue", "white", "red"]),
    "Humidity": ("environment", "humidity", "Humidity (%)", ["gray", "blue"]),
    "Rainfall": ("environment", "rainfall", "Rainfall (mm)", ["gray", "blue"]),
    "Solar Radiation": ("environment", "solar_radiation", "Solar Radiation (W/m²)", ["yellow", "orange", "red"]),
    "Conductivity": ("soil", "conductivity", "Conductivity (µS/cm)", ["purple", "orange"]),
    "Nitrogen (N)": ("soil", "N", "N (ppm)", ["#f7fbff", "#08306b"]),
    "Phosphorus (P)": ("soil", "P", "P (ppm)", ["#fff5eb", "#7f2704"]),
    "Potassium (K)": ("soil", "K", "K (ppm)", ["#f2f0f7", "#4a1486"]),
}

selected_param = st.selectbox("Select parameter to visualize on map", list(param_options.keys()))
category, key, label, color_scale = param_options[selected_param]

sensor_df = pd.DataFrame(selected_zone["sensors"])
sensor_df["Sensor"] = [f"{zone}-S{i+1}" for i in range(len(sensor_df))]
sensor_df["Value"] = selected_zone[category][key]

fig = px.scatter_mapbox(
    sensor_df,
    lat="lat",
    lon="lon",
    color="Value",
    color_continuous_scale=color_scale,
    size=[75] * len(sensor_df),
    size_max=75,
    hover_name="Sensor",
    zoom=17,
    mapbox_style="open-street-map",
    height=500
)
fig.update_layout(coloraxis_colorbar={"title": label})
st.plotly_chart(fig, use_container_width=True)