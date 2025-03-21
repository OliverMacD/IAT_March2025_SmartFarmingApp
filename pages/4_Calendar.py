import streamlit as st
from components.farm_calendar import render_farm_calendar
from components.page_help import render_page_help
from components.login import login

login()

st.set_page_config(page_title="Calendar View", layout="wide", page_icon="static/Totech_Logo.png")
st.title("📅 Farm Calendar")

# Sidebar logo & styling
user = st.secrets["credentials"]["name"]
with st.sidebar:
    st.image("static/Totech_Logo_W-Name.png", use_container_width=True)
    st.markdown("### SmartFarm App")
    st.markdown(f"Welcome {user}! Use the sidebar to navigate between pages and monitor your farm's health in real-time.")

render_page_help("calendar")
render_farm_calendar()