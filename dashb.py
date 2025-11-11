import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 1 second
st_autorefresh(interval=1000, key="refresh")

st.set_page_config(page_title="Energy Dashboard", layout="wide")

# CSS Styling
st.markdown("""
<style>
header {visibility: hidden !important; height: 0px !important;}
.stDeployButton, .stButton button {visibility: hidden !important; height: 0px !important;}
.stApp {overflow: hidden !important;}
.main {padding: 0; margin: 0; overflow: hidden !important;}
.block-container {padding: 10px !important; margin: 0 !important;}
</style>
""", unsafe_allow_html=True)

# Flask API URL
api_url = "https://esp-dashboard-m5jz.onrender.com"  # Update this IP based on where Flask is running

# Default values
steps, energy, power, status = 0, 0, 0, "Inactive"

# Fetch the latest data from API
try:
    response = requests.get(api_url, timeout=2)
    if response.status_code == 200:
        data = response.json()
        steps = data.get("steps", 0)
        energy = data.get("energy", 0)
        power = data.get("power", 0)
        status = data.get("status", "Inactive")
    else:
        st.warning(f"API returned status code {response.status_code}")
except Exception as e:
    st.warning(f"API fetch error: {e}")

# Manual refresh button
if st.button("Refresh Now"):
    st.rerun()

# Display time and date
now = datetime.now()
st.markdown(f"""
<div style='text-align:center; padding:10px; font-size:60px; color:#0d47a1; font-weight:700'>
{now.strftime('%I:%M:%S %p')}
</div>
<div style='text-align:center; font-size:25px; color:#424242; margin-bottom:40px'>
{now.strftime('%A, %B %d, %Y')}
</div>
""", unsafe_allow_html=True)

# Layout
top1, top2 = st.columns(2, gap="large")

with top1:
    st.markdown(f"""
    <div style='background:white; border-radius:20px; padding:30px; text-align:center;
    box-shadow:0 6px 20px rgba(0,0,0,0.1); height:220px; margin:15px;'>
    <h3>👣 Steps</h3>
    <div style='font-size:38px; font-weight:bold; color:#0056b3'>{steps}</div>
    </div>
    """, unsafe_allow_html=True)

with top2:
    st.markdown(f"""
    <div style='background:white; border-radius:20px; padding:30px; text-align:center;
    box-shadow:0 6px 20px rgba(0,0,0,0.1); height:220px; margin:15px;'>
    <h3>🔋 Energy</h3>
    <div style='font-size:38px; font-weight:bold; color:#6a0dad'>{energy} J</div>
    </div>
    """, unsafe_allow_html=True)

bottom1, bottom2 = st.columns(2, gap="large")

with bottom1:
    st.markdown(f"""
    <div style='background:white; border-radius:20px; padding:30px; text-align:center;
    box-shadow:0 6px 20px rgba(0,0,0,0.1); height:220px; margin:15px;'>
    <h3>⚡ Power</h3>
    <div style='font-size:38px; font-weight:bold; color:#f57c00'>{power:.2f} W</div>
    </div>
    """, unsafe_allow_html=True)

with bottom2:
    color = "#00796b" if str(status).lower() == "active" else "#9e9e9e"
    st.markdown(f"""
    <div style='background:white; border-radius:20px; padding:30px; text-align:center;
    box-shadow:0 6px 20px rgba(0,0,0,0.1); height:220px; margin:15px;'>
    <h3>💡 Status</h3>
    <div style='font-size:38px; font-weight:bold; color:{color}'>
        {status}
    </div>
    </div>
    """, unsafe_allow_html=True)

