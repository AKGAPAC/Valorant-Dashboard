import streamlit as st
from supabase import create_client
from utils.supabase_utils import get_teams, create_player, get_players

st.title("Edit Players")

supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)

# Form to create or edit player
with st.form("player_form"):
    player_name = st.text_input("Player Name")
    teams = get_teams(supabase)
    team_names = [team["name"] for team in teams]
    team_name = st.selectbox("Team", team_names)
    rank = st.text_input("Rank")
    submitted = st.form_submit_button("Save Player")

    if submitted:
        team_id = next((team["id"] for team in teams if team["name"] == team_name), None)
        if team_id:
            create_player(supabase, player_name, team_id, rank)
            st.success("Player saved!")

# Display current players
players = get_players(supabase)
st.subheader("Current Players")
for player in players:
    st.write(f"{player['name']} — {player['rank']}")
# force reload
