def check_alerts(zone):
    alerts = []
    if zone["soil"]["moisture"] < 20:
        alerts.append("⚠️ Moisture below 20%")
    if zone["irrigation"]["tank_level"] < 15:
        alerts.append("🚨 Tank level critically low")
    return alerts