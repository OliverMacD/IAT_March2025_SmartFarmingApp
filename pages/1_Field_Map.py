import streamlit as st
from components.zone_map import render_field_map
from utils.data_loader import load_data
from components.page_help import render_page_help
from components.login import login
from components.websocket_listener import get_latest_data

login()

st.set_page_config(page_title="Field Map", layout="wide", page_icon="static/Totech_Logo.png")

# Sidebar logo & styling
user = st.secrets["credentials"]["name"]
with st.sidebar:
    st.image("static/Totech_Logo_W-Name.png", use_container_width=True)
    st.markdown("### SmartFarm App")
    st.markdown(f"Welcome {user}! Use the sidebar to navigate between pages and monitor your farm's health in real-time.")

st.title("🗺️ Field Map View")
render_page_help("map")

if st.session_state["ws_started"]:
    data = get_latest_data(fallback_loader=load_data)
else:
    data = load_data()


render_field_map(data)