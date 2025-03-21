import streamlit as st

def render_irrigation_controls(zone):
    st.subheader("Irrigation Controls")
    st.write(f"Status: {zone['irrigation']['status']}")
    st.write(f"Tank Level: {zone['irrigation']['tank_level']}%")
    if st.button(f"Toggle Irrigation for {zone['zone_id']}"):
        st.success(f"Irrigation toggled for {zone['zone_id']} (mock action)")