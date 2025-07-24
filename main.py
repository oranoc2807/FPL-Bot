import streamlit as st
import pandas as pd
from fpl_data import fetch_fpl_data, fetch_fixtures
from answer import answer_question

st.set_page_config(page_title="FPL Web Chatbot", layout="wide")
st.title("⚽ FPL Web Chatbot")

players, teams = fetch_fpl_data()
fixtures = fetch_fixtures()

team_map = dict(zip(teams["id"], teams["name"]))
fixtures["team_h_name"] = fixtures["team_h"].map(team_map)
fixtures["team_a_name"] = fixtures["team_a"].map(team_map)
fixtures["kickoff_time"] = pd.to_datetime(fixtures["kickoff_time"]).dt.strftime("%b %d, %Y %H:%M")
upcoming = fixtures[fixtures["event"].notnull()].sort_values("event").head(10)
df = upcoming[["event", "team_h_name", "team_a_name", "kickoff_time"]]

left_col, right_col = st.columns([2, 1])

with left_col:
    question = st.text_input("Ask your FPL or general question:")
    if question:
        with st.spinner("Answering..."):
            answer = answer_question(question, players)
            st.markdown("### ✅ Answer")
            st.write(answer)

    st.subheader("🔥 Most In-Form Players")
    top_form = players[players["selected_by_percent"].astype(float) > 0].copy()
    top_form = top_form.sort_values("selected_by_percent", ascending=False).head(10)
    st.dataframe(top_form[["first_name", "second_name", "team_name", "form", "selected_by_percent"]])

with right_col:
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
