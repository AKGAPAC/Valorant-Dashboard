def get_teams(supabase):
    return supabase.table("teams").select("*").execute().data

def get_players(supabase):
    return supabase.table("players").select("*").execute().data

def get_matches(supabase):
    return supabase.table("matches").select("*").execute().data

def create_player(supabase, name, team_id, rank):
    return supabase.table("players").insert({
        "name": name,
        "team_id": team_id,
        "rank": rank
    }).execute()

def insert_player_match_stats(data: dict):
    return supabase.table("player_match_stats").insert(data).execute()
