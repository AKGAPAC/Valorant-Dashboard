import streamlit as st
from supabase import create_client, Client
import os
import math

# --- Initialize Supabase ---
def init_supabase() -> Client:
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except Exception:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        st.error("Supabase credentials not found.")
        st.stop()
    return create_client(url, key)

# --- Helper functions ---
def safe_div(a, b):
    try:
        return round(float(a) / float(b), 2) if b else 0.0
    except:
        return 0.0

def calculate_derived(player):
    kills = float(player.get("kills", 0))
    deaths = float(player.get("deaths", 0))
    assists = float(player.get("assists", 0))
    headshots = float(player.get("headshots", 0))
    damage = float(player.get("damage", 0))
    games = float(player.get("games_played", 0))
    wins = float(player.get("wins", 0))

    return {
        "kd_ratio": safe_div(kills, deaths),
        "hs_percent": safe_div(headshots, kills) * 100 if kills > 0 else 0.0,
        "adr": safe_div(damage, games),
        "win_rate": safe_div(wins, games) * 100 if games > 0 else 0.0,
        "acs": safe_div((kills * 100 + assists * 50 + damage / 10 + safe_div(headshots, kills) * 10), games) if games > 0 else 0.0,
    }

# --- Theme ---
st.markdown(
    """
    <style>
    .reportview-container, .main, .block-container {
        background: linear-gradient(180deg, #0f1724, #0b0f1a);
        color: #e6e9ee;
    }
    .metric-card {
        background: linear-gradient(90deg, rgba(59,130,246,0.12), rgba(139,92,246,0.12));
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.6);
        margin-bottom: 10px;
    }
    .big-title {
        font-size:28px;
        font-weight:700;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Valorant — Competitive Dashboard")
st.sidebar.markdown("**Theme:** Blue • Black • Purple")
