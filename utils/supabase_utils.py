def get_teams(supabase):
    response = supabase.table("teams").select("*").execute()
    return response.data if response.data else []

def create_player(supabase, name, team_id, rank):
    supabase.table("players").insert({
        "name": name,
        "team_id": team_id,
        "rank": rank
    }).execute()

def get_players(supabase):
    response = supabase.table("players").select("*").execute()
    return response.data if response.data else []
