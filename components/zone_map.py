import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_field_map(data):
    parameter = st.selectbox(
        "Select parameter to visualize:",
        ["Soil Moisture", "Soil pH", "Soil Temperature", "Humidity", "Rainfall", "Solar Radiation"]
    )

    color_label = ""
    color_scale = []
    rows = []

    for zone in data["zones"]:
        for i, sensor in enumerate(zone["sensors"]):
            record = {
                "Zone": zone["zone_id"],
                "Sensor": f"{zone['zone_id']}-S{i+1}",
                "Latitude": sensor["lat"],
                "Longitude": sensor["lon"]
            }

            if parameter == "Soil Moisture":
                record["Value"] = zone["soil"]["moisture"]
                color_label = "Moisture (%)"
                color_scale = ["red", "yellow", "green"]  # Fixed: red = dry, green = wet
            elif parameter == "Soil pH":
                record["Value"] = zone["soil"]["pH"]
                color_label = "Soil pH"
                color_scale = ["red", "green", "blue"]  # acidic to neutral to alkaline
            elif parameter == "Soil Temperature":
                record["Value"] = zone["soil"]["temperature"]
                color_label = "Soil Temp (°C)"
                color_scale = ["blue", "white", "red"]
            elif parameter == "Humidity":
                record["Value"] = zone["environment"]["humidity"]
                color_label = "Humidity (%)"
                color_scale = ["gray", "blue"]
            elif parameter == "Rainfall":
                record["Value"] = zone["environment"]["rainfall"]
                color_label = "Rainfall (mm)"
                color_scale = ["gray", "blue"]
            elif parameter == "Solar Radiation":
                record["Value"] = zone["environment"]["solar_radiation"]
                color_label = "Solar Radiation (W/m²)"
                color_scale = ["yellow", "orange", "red"]

            rows.append(record)

    df = pd.DataFrame(rows)

    fig = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Value",
        color_continuous_scale=color_scale,
        hover_name="Sensor",
        size=[75] * len(df),  # Fixed size for all points
        size_max=75,
        zoom=16,
        mapbox_style="open-street-map",
        height=600,
    )
    fig.update_layout(coloraxis_colorbar={"title": color_label})

    # Add farmhouse as black dot
    farm_lat = data["farm_location"]["latitude"]
    farm_lon = data["farm_location"]["longitude"]
    fig.add_trace(go.Scattermapbox(
        lat=[farm_lat],
        lon=[farm_lon],
        mode="markers",
        marker=go.scattermapbox.Marker(size=10, color="black"),
        name="Farmhouse"
    ))

    st.plotly_chart(fig, use_container_width=True)