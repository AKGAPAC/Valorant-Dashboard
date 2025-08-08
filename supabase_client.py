from supabase import create_client

def get_supabase():
    import streamlit as st
    import os

    url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL"))
    key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY"))

    if not url or not key:
        st.error("Supabase credentials are missing.")
        st.stop()

    return create_client(url, key)
