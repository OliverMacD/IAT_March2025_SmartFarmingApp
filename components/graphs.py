import streamlit as st
import pandas as pd
import plotly.express as px

def render_moisture_graph(data):
    df = pd.DataFrame([
        {"Zone": z["zone_id"], "Moisture": z["soil"]["moisture"]}
        for z in data["zones"]
    ])
    fig = px.bar(df, x="Zone", y="Moisture", color="Zone", title="Current Soil Moisture by Zone")
    st.plotly_chart(fig, use_container_width=True)

def render_analytics_graphs(data):
    for zone in data["zones"]:
        st.subheader(f"{zone['zone_id']} - Moisture Trend (Mock Data)")
        df = pd.DataFrame({
            "Day": list(range(1, 8)),
            "Moisture": [zone["soil"]["moisture"] - i*0.5 for i in range(7)]
        })
        fig = px.line(df, x="Day", y="Moisture", title=f"{zone['zone_id']} Moisture Over Time")
        st.plotly_chart(fig, use_container_width=True)

def render_zone_detail(zone):
    st.metric("Moisture", f"{zone['soil']['moisture']}%")
    st.metric("Temperature", f"{zone['soil']['temperature']} °C")
    st.metric("pH", f"{zone['soil']['pH']}")
    st.metric("N", f"{zone['soil']['N']} ppm")
    st.metric("P", f"{zone['soil']['P']} ppm")
    st.metric("K", f"{zone['soil']['K']} ppm")

def render_comparison(data):
    import pandas as pd
    import plotly.express as px
    st.subheader("Farm Comparison (Mock Data)")
    df = pd.DataFrame([
        {
            "Zone": z["zone_id"],
            "Moisture": z["soil"]["moisture"],
            "pH": z["soil"]["pH"],
            "Temperature": z["soil"]["temperature"],
            "N": z["soil"]["N"],
            "P": z["soil"]["P"],
            "K": z["soil"]["K"]
        }
        for z in data["zones"]
    ])
    st.write("### Moisture Comparison")
    fig = px.bar(df, x="Zone", y="Moisture", color="Zone")
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Nutrient Comparison (NPK)")
    fig = px.bar(df, x="Zone", y=["N", "P", "K"], barmode="group", title="NPK Levels by Zone")
    st.plotly_chart(fig, use_container_width=True)