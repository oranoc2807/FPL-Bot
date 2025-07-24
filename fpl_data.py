import requests
import pandas as pd
import streamlit as st

@st.cache_data
def fetch_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        players = pd.DataFrame(data["elements"])
        teams = pd.DataFrame(data["teams"])
        team_map = dict(zip(teams["id"], teams["name"]))
        players["team_name"] = players["team"].map(team_map)
        players["full_name"] = (players["first_name"] + " " + players["second_name"]).str.lower()
        players["selected_by_percent"] = players["selected_by_percent"].astype(float)
        return players, teams
    return pd.DataFrame(), pd.DataFrame()

@st.cache_data
def fetch_fixtures():
    url = "https://fantasy.premierleague.com/api/fixtures/"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()
