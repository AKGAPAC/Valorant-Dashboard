import streamlit as st
from supabase_client import get_teams, get_players, add_match, add_player_match_stats
import datetime

st.set_page_config(page_title="Valorant Dashboard", layout="wide")

st.title("🎯 Valorant Match Tracker")

admin_password = st.secrets.get("ADMIN_PASSWORD", "Admin123")
if "admin" not in st.session_state:
    st.session_state.admin = False

if not st.session_state.admin:
    pwd = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if pwd == admin_password:
            st.session_state.admin = True
        else:
            st.error("Incorrect password")

if st.session_state.admin:
    st.subheader("📋 Add New Match Result")
    teams = get_teams()
    team_options = {t["name"]: t["id"] for t in teams}
    selected_team = st.selectbox("Select Team", list(team_options.keys()))
    selected_team_id = team_options[selected_team]

    players = get_players(selected_team_id)
    player_options = {p["name"]: p["id"] for p in players}
    selected_player = st.selectbox("Select Player", list(player_options.keys()))
    selected_player_id = player_options[selected_player]

    opponent = st.text_input("Opponent Team")
    map_played = st.selectbox("Map", [
        "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox",
        "Lotus", "Pearl", "Split", "Sunset", "Corrode"
    ])
    agent = st.text_input("Agent Used")
    result = st.selectbox("Result", ["win", "loss", "draw"])
    date = st.date_input("Match Date", value=datetime.date.today())

    with st.form("match_stats"):
        kills = st.number_input("Kills", 0)
        deaths = st.number_input("Deaths", 0)
        assists = st.number_input("Assists", 0)
        headshots = st.number_input("Headshots", 0)
        damage = st.number_input("Total Damage", 0)
        score = st.number_input("Combat Score", 0)
        rounds_played = st.number_input("Rounds Played", 0)
        first_kills = st.number_input("First Kills", 0)
        first_deaths = st.number_input("First Deaths", 0)
        submitted = st.form_submit_button("Submit Match Result")

        if submitted:
            match = {
                "date": date.isoformat(),
                "opponent": opponent,
                "map": map_played,
                "result": result
            }
            match_resp = add_match(match)
            if match_resp.data:
                match_id = match_resp.data[0]["id"]
                stats = {
                    "match_id": match_id,
                    "player_id": selected_player_id,
                    "agent_used": agent,
                    "kills": kills,
                    "deaths": deaths,
                    "assists": assists,
                    "headshots": headshots,
                    "damage": damage,
                    "score": score,
                    "rounds_played": rounds_played,
                    "first_kills": first_kills,
                    "first_deaths": first_deaths
                }
                stat_resp = add_player_match_stats(stats)
                if stat_resp.data:
                    st.success("Match and player stats added successfully!")
                else:
                    st.error("Failed to insert player stats.")
            else:
                st.error("Failed to insert match.")
