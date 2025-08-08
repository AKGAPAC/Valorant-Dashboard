import streamlit as st

st.set_page_config(page_title="Valorant Match Tracker", layout="wide")

# Dummy admin auth
admin_pass = st.text_input("Enter Admin Password", type="password")
if admin_pass == "Admin123":
    st.success("Logged in!")

    tab = st.selectbox("Choose Action", ["Players", "Match Tracker"])

    if tab == "Players":
        st.header("Edit Players")
        st.text_input("Player Name")
        st.selectbox("Team", ["Kadiliman", "Other Team"])
        st.text_input("Rank")
        st.number_input("Kills", min_value=0)
        st.number_input("Deaths", min_value=0)
        st.number_input("Assists", min_value=0)

    elif tab == "Match Tracker":
        st.header("Add New Match Result")
        selected_team = st.selectbox("Select Team", ["Kadiliman"])
        player_list = ["NDG", "JettMains", "SovaGod"]  # Dummy values
        selected_player = st.selectbox("Select Player", player_list)

        if selected_player:
            st.success(f"Ready to enter stats for {selected_player}")
            st.selectbox("Map", ["Ascent", "Bind", "Corrode"])
            st.selectbox("Agent", ["Jett", "Sova", "Omen"])
            st.number_input("Kills", min_value=0)
            st.number_input("First Kills", min_value=0)
            st.number_input("First Deaths", min_value=0)
            st.button("Submit Result")
else:
    st.warning("Please enter admin password.")
