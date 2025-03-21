# components/websocket_listener.py
import websocket
import threading
import json
import queue

# Thread-safe queue to hold messages
data_queue = queue.Queue()

def on_message(ws, message):
    try:
        data = json.loads(message)
        data_queue.put(data)
    except Exception as e:
        print("WebSocket message parse error:", e)

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket connected")

def start_websocket(url):
    ws = websocket.WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

# Call this from your Streamlit app to safely get new data
def get_latest_data(fallback_loader=None):
    import streamlit as st
    if not "live_sensor_data" in st.session_state:
        st.session_state["live_sensor_data"] = fallback_loader() if fallback_loader else None

    try:
        while not data_queue.empty():
            st.session_state["live_sensor_data"] = data_queue.get_nowait()
    except queue.Empty:
        pass

    return st.session_state["live_sensor_data"]
