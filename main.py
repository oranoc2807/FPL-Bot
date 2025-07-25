import streamlit as st
import pandas as pd
from fpl_data import fetch_fpl_data, fetch_fixtures
from answer import answer_question

# PAGE CONFIG
st.set_page_config(page_title="FPL Web Chatbot", layout="wide")

# === HEADER ===
st.markdown("<h1 style='text-align:center;'>⚽ FPL Assistant Bot</h1>", unsafe_allow_html=True)

# === FETCH DATA ===
players, teams = fetch_fpl_data()
fixtures = fetch_fixtures()

team_map = dict(zip(teams["id"], teams["name"]))
fixtures["team_h_name"] = fixtures["team_h"].map(team_map)
fixtures["team_a_name"] = fixtures["team_a"].map(team_map)
fixtures["kickoff_time"] = pd.to_datetime(fixtures["kickoff_time"]).dt.strftime("%b %d, %Y %H:%M")
upcoming = fixtures[fixtures["event"].notnull()].sort_values("event").head(10)
df = upcoming[["event", "team_h_name", "team_a_name", "kickoff_time"]]

# === CHATBOT ===
with st.container():
    question = st.text_input("Ask your FPL or general question:")
    if question:
        with st.spinner("Answering..."):
            answer = answer_question(question, players)
            st.markdown("### ✅ Answer")
            st.write(answer)

# === 2x2 GRID ===
# Row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Players PPM")
    players["PPM"] = players["total_points"] / players["minutes"].replace(0, 1)
    ppm_df = players.sort_values("PPM", ascending=False).head(10)
    st.dataframe(ppm_df[["first_name", "second_name", "team_name", "PPM"]])

with col2:
    st.markdown("### 💎 Best Value Picks")
    players["value"] = players["total_points"] / players["now_cost"]
    value_df = players.sort_values("value", ascending=False).head(10)
    st.dataframe(value_df[["first_name", "second_name", "team_name", "value"]])

# Row 2
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🕵️ Undervalued Players")
    undervalued = players[(players["minutes"] > 0) & (players["selected_by_percent"].astype(float) < 5)]
    undervalued = undervalued.sort_values("value", ascending=False).head(10)
    st.dataframe(undervalued[["first_name", "second_name", "team_name", "value", "selected_by_percent"]])

with col4:
    st.markdown("### 👑 Captain Suggestions")
    captain_choices = players.sort_values("form", ascending=False).head(10)
    st.dataframe(captain_choices[["first_name", "second_name", "team_name", "form"]])

# === FIXTURES — full width at the end ===
st.markdown("### 📅 Upcoming Fixtures")
grouped = df.groupby("event")
for gw, matches in grouped:
    st.markdown(f"<h4 style='color:#4CAF50;'>Gameweek {gw}</h4>", unsafe_allow_html=True)
    for _, row in matches.iterrows():
        home = row["team_h_name"]
        away = row["team_a_name"]
        date = row["kickoff_time"]
        st.markdown(f"""
        <div style="background-color: #1e1e1e; border-radius: 12px; padding: 14px; margin-bottom: 8px;">
            <div style="display:flex; justify-content: space-between; align-items:center;">
                <div style="font-weight:bold; font-size: 17px; color: #ffffff;">{home} 🆚 {away}</div>
                <div style="font-size: 14px; color: #aaaaaa;">{date}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
