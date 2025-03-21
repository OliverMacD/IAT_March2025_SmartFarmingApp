import streamlit as st

def render_page_help(page):
    help_texts = {
        "home": {
            "what": "Gives you a real-time overview of farm conditions using color-coded metrics and comparison tools.",
            "how": (
                "• Glance at the colored stat cards to quickly assess soil, weather, and tank levels.<br>"
                "• Use the dropdown to select any measurement (e.g., pH, rainfall, solar radiation) and compare values across zones using a color-coded table and bar chart.<br>"
                "• Look for red/yellow cards or table highlights to spot issues."
            )
        },
        "map": {
            "what": "Plots all your IoT sensors on a live map with color indicators for the selected parameter.",
            "how": (
                "• Use the dropdown to select what to visualize (e.g., Soil Moisture, pH, Humidity).<br>"
                "• Each dot represents a sensor — colors show how good or bad the value is (green = good, red = warning).<br>"
                "• The small black dot shows your farmhouse location for reference."
            )
        },
        "zone": {
            "what": "Displays all sensor data for a single zone in a clean, color-tagged grid.",
            "how": (
                "• Choose a zone from the dropdown.<br>"
                "• Review values like moisture, temperature, nutrients, and wind in an organized grid.<br>"
                "• Use this page before field work to know what’s happening in specific areas."
            )
        },
        "analytics": {
            "what": "Visualize how any metric changes over time across multiple zones.",
            "how": (
                "• Choose which zones you'd like to compare using the multiselect tool.<br>"
                "• Select a data type such as temperature, pH, or rainfall.<br>"
                "• Adjust the slider to pick how many past days of data to view (mock data is used for now).<br>"
                "• Use the line graph to spot trends and patterns between zones over time."
            )
        },
        "calendar": {
            "what": "Displays your scheduled events and forecasts for the month in a visual calendar.",
            "how": (
                "• Review pre-filled events for irrigation, refills, market days, planting, and harvest.<br>"
                "• Use the dropdown and date picker to add new pre-defined events like 🧪 restocks or 🌾 harvests.<br>"
                "• View daily weather icons added automatically using OpenWeather forecasts.<br>"
                "• Everything is color-coded and easy to scan across the month."
            )
        },
        "comparison": {
            "what": "Lets you visually compare performance between zones or seasons side by side.",
            "how": (
                "• Select seasons or zones to compare.<br>"
                "• Analyze which parts of your farm are improving, struggling, or changing over time.<br>"
                "• Useful for post-harvest review and decision-making."
            )
        },
        "settings": {
            "what": "Manages your IoT devices and controls what data you see and how.",
            "how": (
                "• Rename sensors or zones for clarity.<br>"
                "• Adjust preferences like units (Celsius vs Fahrenheit) or default display parameter.<br>"
                "• Check which devices are active or offline."
            )
        }
    }

    content = help_texts.get(page)
    if content:
        with st.expander("ℹ️ How to use this page"):
            st.markdown(f"**What it does:**<br>{content['what']}", unsafe_allow_html=True)
            st.markdown(f"**How to use it:**<br>{content['how']}", unsafe_allow_html=True)