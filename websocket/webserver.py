import asyncio
import websockets
import json
import random
from datetime import datetime

zones = {
    "Zone 1": [1, 2, 4, 5],
    "Zone 2": [2, 3, 5, 6],
    "Zone 3": [4, 5, 7, 8],
    "Zone 4": [5, 6, 8, 9]
}

sensor_coords = {
    1: [43.586726, -116.774960],
    2: [43.587581, -116.774944],
    3: [43.588420, -116.774933],
    4: [43.586737, -116.773769],
    5: [43.587561, -116.773774],
    6: [43.588435, -116.773791],
    7: [43.586753, -116.772648],
    8: [43.587596, -116.772632],
    9: [43.588397, -116.772680]
}

def generate_data():
    all_zones = []
    for zone_id, sensor_ids in zones.items():
        soil = {
            "moisture": round(random.uniform(15, 40), 2),
            "pH": round(random.uniform(5.8, 7.8), 2),
            "temperature": round(random.uniform(15, 28), 2),
            "N": round(random.uniform(20, 80), 2),
            "P": round(random.uniform(10, 50), 2),
            "K": round(random.uniform(30, 90), 2),
            "conductivity": round(random.uniform(100, 600), 2),
        }
        env = {
            "air_temperature": round(random.uniform(16, 32), 2),
            "humidity": round(random.uniform(35, 90), 2),
            "rainfall": round(random.uniform(0, 12), 2),
            "solar_radiation": round(random.uniform(200, 900), 2),
            "wind_speed": round(random.uniform(0, 10), 2),
            "wind_direction": round(random.uniform(0, 360), 2),
        }
        irrigation = {
            "tank_level": round(random.uniform(30, 100), 2)
        }
        sensors = [{"lat": sensor_coords[sid][0], "lon": sensor_coords[sid][1]} for sid in sensor_ids]
        all_zones.append({
            "zone_id": zone_id,
            "crop_type": "Tomato",
            "soil": soil,
            "environment": env,
            "irrigation": irrigation,
            "sensors": sensors
        })

    return json.dumps({
        "timestamp": datetime.now().isoformat(),
        "farm_location": {
            "latitude": 43.587641,
            "longitude": -116.775265
        },
        "zones": all_zones
    })

# ✅ Proper handler with both websocket and path
async def sensor_server(websocket):
    print("Client connected")
    try:
        while True:
            data = generate_data()
            await websocket.send(data)
            await asyncio.sleep(5)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

# ✅ Modern asyncio server runner
async def main():
    print("Starting SmartFarm WebSocket server on ws://localhost:8765")
    async with websockets.serve(sensor_server, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())