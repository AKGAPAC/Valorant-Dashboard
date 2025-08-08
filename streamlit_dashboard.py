import streamlit as st
from supabase import create_client
from utils.supabase_utils import (
    get_teams, get_players, get_matches,
    create_player, insert_player_match_stats
)

st.set_page_config(page_title="Valorant Dashboard", layout="wide")

# Initialize Supabase
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)

st.title("🧪 Valorant Team Dashboard")
password = st.text_input("Enter Admin Password", type="password")

if password != "Admin123":
    st.warning("Enter password to access admin features.")
    st.stop()

# Main sections
section = st.sidebar.selectbox("Select Panel", ["Players", "Add Match Result"])

if section == "Players":
    st.header("🧍 Create or Edit Players")
    with st.form("player_form"):
        name = st.text_input("Player Name")
        teams = get_teams(supabase)
        team_names = [team["name"] for team in teams]
        team_name = st.selectbox("Team", team_names)
        rank = st.text_input("Rank")
        if st.form_submit_button("Save Player"):
            team_id = next((t["id"] for t in teams if t["name"] == team_name), None)
            if team_id:
                create_player(supabase, name, team_id, rank)
                st.success(f"Player '{name}' saved!")

    st.subheader("Current Players")
    players = get_players(supabase)
    for p in players:
        st.write(f"👤 {p['name']} | Rank: {p['rank']}")

elif section == "Add Match Result":
    st.header("📊 Log Match Stats")

    players = get_players(supabase)
    player_names = [p["name"] for p in players]
    player = st.selectbox("Player", player_names)

    selected = next((p for p in players if p["name"] == player), None)
    player_id = selected["id"] if selected else None

    match_id = st.text_input("Match ID (or code)")
    map_played = st.selectbox("Map", ["Ascent", "Bind", "Haven", "Split", "Lotus", "Sunset", "Breeze", "Icebox", "Corrode"])
    agent = st.text_input("Agent Used")
    kills = st.number_input("Kills", 0)
    deaths = st.number_input("Deaths", 0)
    assists = st.number_input("Assists", 0)
    headshots = st.number_input("Headshots", 0)
    damage = st.number_input("Damage", 0)
    score = st.number_input("Score", 0)
    rounds_played = st.number_input("Rounds Played", 1)
    first_kill = st.checkbox("Got First Kill")
    first_death = st.checkbox("Got First Death")

    if st.button("Submit Stats"):
        match_record = {
            "match_id": match_id,
            "player_id": player_id,
            "agent_used": agent,
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "headshots": headshots,
            "damage": damage,
            "score": score,
            "rounds_played": rounds_played,
            "first_kill": first_kill,
            "first_death": first_death,
            "map_played": map_played
        }
        insert_player_match_stats(match_record)
        st.success("✅ Match stats submitted!")
