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
# --- Initialize Supabase ---
supabase = init_supabase()

# --- Fetch data ---
@st.cache_data(ttl=30)
def fetch_teams():
    res = supabase.table("teams").select("*").execute()
    return res.data or []

@st.cache_data(ttl=30)
def fetch_players():
    res = supabase.table("players").select("*").execute()
    return res.data or []

teams = fetch_teams()
players = fetch_players()
team_names = {t["id"]: t.get("name", "Unknown") for t in teams}

# --- Dashboard Header ---
st.markdown('<div class="big-title">Valorant Competitive Dashboard</div>', unsafe_allow_html=True)

# --- Team Selector ---
team_options = ["All Teams"] + [f'{t["name"]} ({t["id"]})' for t in teams]
selected = st.selectbox("Select team", options=team_options)

# --- Filter players ---
if selected != "All Teams":
    try:
        selected_id = int(selected.split("(")[-1].replace(")", ""))
        players = [p for p in players if p.get("team_id") == selected_id]
    except:
        pass

# --- Display team info ---
def render_team_card(team):
    st.markdown(f'<div class="metric-card"><h3>{team.get("name")}</h3>', unsafe_allow_html=True)
    logo = team.get("logo_url")
    if logo:
        st.image(logo, width=160)
    st.markdown("</div>", unsafe_allow_html=True)

if selected != "All Teams":
    t = next((x for x in teams if x["id"] == selected_id), None)
    if t:
        render_team_card(t)
else:
    for t in teams:
        render_team_card(t)
# --- Player Cards ---
cols = st.columns(3)
for i, p in enumerate(players):
    derived = calculate_derived(p)
    with cols[i % 3]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader(p.get("name", "Player"))
        st.write(f'**Rank:** {p.get("rank", "-")}  •  **Team:** {team_names.get(p.get("team_id"), "-")}')
        st.markdown(f'**K/D:** {derived["kd_ratio"]}  •  **ADR:** {derived["adr"]}  •  **ACS:** {derived["acs"]}')
        st.markdown(f'Kills: {p.get("kills", 0)}  •  Deaths: {p.get("deaths", 0)}  •  Assists: {p.get("assists", 0)}')
        st.markdown(f'HS%: {derived["hs_percent"]}%  •  Win%: {derived["win_rate"]}%  •  Games: {p.get("games_played", 0)}')
        st.markdown('</div>', unsafe_allow_html=True)

# --- Admin Access ---
st.sidebar.markdown("---")
st.sidebar.subheader("Admin Panel (Password Protected)")
admin_input = st.sidebar.text_input("Enter admin password", type="password")

# Use password stored in secrets or fallback
admin_password = st.secrets.get("ADMIN_PASSWORD", "Admin123")

if admin_input == admin_password:
    st.sidebar.success("Access granted")

    action = st.sidebar.radio("What would you like to edit?", ["Teams", "Players", "Upload Logo"])

    if action == "Teams":
        st.header("Edit Teams")
        team_names = [t["name"] for t in teams]
        team_to_edit = st.selectbox("Select team", options=["Create New"] + team_names)

        if team_to_edit == "Create New":
            name = st.text_input("Team Name")
            if st.button("Create Team"):
                supabase.table("teams").insert({"name": name, "logo_url": ""}).execute()
                st.success("Team created. Refresh to see changes.")
        else:
            team = next(t for t in teams if t["name"] == team_to_edit)
            name = st.text_input("Edit Team Name", value=team["name"])
            if st.button("Update Team"):
                supabase.table("teams").update({"name": name}).eq("id", team["id"]).execute()
                st.success("Team updated.")

    elif action == "Players":
        st.header("Edit Players")
        player_names = [p["name"] for p in players]
        player_to_edit = st.selectbox("Select player", options=["Create New"] + player_names)

        if player_to_edit == "Create New":
            new_player = {}
        else:
            new_player = next(p for p in players if p["name"] == player_to_edit)

        name = st.text_input("Player Name", value=new_player.get("name", ""))
        rank = st.text_input("Rank", value=new_player.get("rank", ""))
        team_id = st.selectbox("Team", options=[t["id"] for t in teams], index=0)
        kills = st.number_input("Kills", value=int(new_player.get("kills", 0)))
        deaths = st.number_input("Deaths", value=int(new_player.get("deaths", 0)))
        assists = st.number_input("Assists", value=int(new_player.get("assists", 0)))
        headshots = st.number_input("Headshots", value=int(new_player.get("headshots", 0)))
        damage = st.number_input("Damage", value=int(new_player.get("damage", 0)))
        games = st.number_input("Games Played", value=int(new_player.get("games_played", 0)))
        wins = st.number_input("Wins", value=int(new_player.get("wins", 0)))

        payload = {
            "name": name,
            "rank": rank,
            "team_id": team_id,
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "headshots": headshots,
            "damage": damage,
            "games_played": games,
            "wins": wins
        }

        derived = calculate_derived(payload)
        payload.update(derived)

        if player_to_edit == "Create New":
            if st.button("Create Player"):
                supabase.table("players").insert(payload).execute()
                st.success("Player added.")
        else:
            if st.button("Update Player"):
                supabase.table("players").update(payload).eq("id", new_player["id"]).execute()
                st.success("Player updated.")

    elif action == "Upload Logo":
        st.header("Upload Team Logo")
        team_id = st.selectbox("Select team ID", options=[t["id"] for t in teams])
        file = st.file_uploader("Upload logo image (JPG/PNG)")

        if file:
            path = f"logos/{team_id}_{file.name}"
            try:
                supabase.storage.create_bucket("team-logos", public=True)
            except:
                pass  # bucket probably exists

            res = supabase.storage.from_("team-logos").upload(path, file.getvalue())
            if res:
                public_url = supabase.storage.from_("team-logos").get_public_url(path).get("publicURL")
                supabase.table("teams").update({"logo_url": public_url}).eq("id", team_id).execute()
                st.success("Logo uploaded and linked.")
else:
    if admin_input:
        st.sidebar.error("Access denied.")
