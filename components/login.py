import streamlit as st

def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.set_page_config(page_title="Login", layout="wide", page_icon="static/Totech_Logo.png", initial_sidebar_state="collapsed")
        st.title("🔐 Login to SmartFarm")
        st.markdown("Please enter your credentials to access the dashboard.")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == st.secrets["credentials"]["username"] and password == st.secrets["credentials"]["password"]:
                st.session_state.logged_in = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
        st.stop()