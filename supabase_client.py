import os
from supabase import create_client
import streamlit as st

SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_teams():
    return supabase.table("teams").select("*").execute().data

def get_players(team_id=None):
    query = supabase.table("players").select("*")
    if team_id:
        query = query.eq("team_id", team_id)
    return query.execute().data

def get_matches():
    return supabase.table("matches").select("*").execute().data

def add_match(match_data):
    return supabase.table("matches").insert(match_data).execute()

def add_player_match_stats(stats_data):
    return supabase.table("player_match_stats").insert(stats_data).execute()

def get_player_match_stats(player_id):
    return supabase.table("player_match_stats").select("*").eq("player_id", player_id).execute().data
