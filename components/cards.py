import streamlit as st

def render_summary_cards(data):
    # Calculate averages
    avg_moisture = sum([z["soil"]["moisture"] for z in data["zones"]]) / len(data["zones"])
    avg_temp = sum([z["soil"]["temperature"] for z in data["zones"]]) / len(data["zones"])
    avg_pH = sum([z["soil"]["pH"] for z in data["zones"]]) / len(data["zones"])
    avg_humidity = sum([z["environment"]["humidity"] for z in data["zones"]]) / len(data["zones"])
    avg_rainfall = sum([z["environment"]["rainfall"] for z in data["zones"]]) / len(data["zones"])
    avg_solar = sum([z["environment"]["solar_radiation"] for z in data["zones"]]) / len(data["zones"])
    avg_n = sum([z["soil"]["N"] for z in data["zones"]]) / len(data["zones"])
    avg_p = sum([z["soil"]["P"] for z in data["zones"]]) / len(data["zones"])
    avg_k = sum([z["soil"]["K"] for z in data["zones"]]) / len(data["zones"])
    avg_conductivity = sum([z["soil"]["conductivity"] for z in data["zones"]]) / len(data["zones"])
    avg_wind_speed = sum([z["environment"]["wind_speed"] for z in data["zones"]]) / len(data["zones"])
    avg_wind_direction = sum([z["environment"]["wind_direction"] for z in data["zones"]]) / len(data["zones"])
    avg_tank_level = sum([z["irrigation"]["tank_level"] for z in data["zones"]]) / len(data["zones"])
    total_sensors = 9

    # Helper color functions with alpha 25% (hex = 40)
    def rgba(hex_color): return hex_color + "40"  # adds 25% opacity

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

    def nutrient_color(): return f"background-color: {rgba('#9966cc')};"
    def conductivity_color(): return f"background-color: {rgba('#cc6699')};"
    def wind_color(): return f"background-color: {rgba('#3399ff')};"
    def tank_color(): return f"background-color: {rgba('#00cccc')};"
    def count_color(): return f"background-color: {rgba('#999999')};"

    # 5 columns per row
    cols = st.columns(5)

    metrics = [
        ("Soil Moisture", f"{avg_moisture:.1f}%", moisture_color(avg_moisture)),
        ("Soil Temp", f"{avg_temp:.1f} °C", temp_color(avg_temp)),
        ("Soil pH", f"{avg_pH:.1f}", pH_color(avg_pH)),
        ("Humidity", f"{avg_humidity:.1f}%", humidity_color(avg_humidity)),
        ("Rainfall", f"{avg_rainfall:.1f} mm", rainfall_color(avg_rainfall)),

        ("Solar Radiation", f"{avg_solar:.0f} W/m²", solar_color(avg_solar)),
        ("Nitrogen (N)", f"{avg_n:.0f} ppm", nutrient_color()),
        ("Phosphorus (P)", f"{avg_p:.0f} ppm", nutrient_color()),
        ("Potassium (K)", f"{avg_k:.0f} ppm", nutrient_color()),
        ("Conductivity", f"{avg_conductivity:.0f} µS/cm", conductivity_color()),

        ("Wind Speed", f"{avg_wind_speed:.1f} m/s", wind_color()),
        ("Wind Direction", f"{avg_wind_direction:.0f}°", wind_color()),
        ("Tank Level", f"{avg_tank_level:.0f}%", tank_color()),
        ("# of Sensors", f"{total_sensors}", count_color())
    ]

    for i, (label, value, style) in enumerate(metrics):
        with cols[i % 5]:
            st.markdown(f"<div style='{style} padding: 1rem; border-radius: 10px; text-align: center;'>"
                        f"<h4>{label}</h4><h2>{value}</h2></div>", unsafe_allow_html=True)