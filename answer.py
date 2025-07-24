import pandas as pd
from env_setup import client
from utils import web_search

def answer_question(query, players):
    query_lower = query.lower()
    matched_player = None

    if "build" in query_lower and "team" in query_lower:
        top_by_position = {
            1: players[players["element_type"] == 1].sort_values("form", ascending=False).head(1),
            2: players[players["element_type"] == 2].sort_values("form", ascending=False).head(4),
            3: players[players["element_type"] == 3].sort_values("form", ascending=False).head(4),
            4: players[players["element_type"] == 4].sort_values("form", ascending=False).head(2),
        }
        team = pd.concat(top_by_position.values())
        response = "Here’s a suggested FPL squad:\n"
        for _, row in team.iterrows():
            response += f"- {row['first_name']} {row['second_name']} ({row['team_name']}) | Form: {row['form']}\n"
        return response

    if "captain" in query_lower:
        best = players.sort_values("form", ascending=False).iloc[0]
        return f"Suggested captain: **{best['first_name']} {best['second_name']}** from {best['team_name']} (Form: {best['form']})"

    if "cheap" in query_lower and "defender" in query_lower:
        cheap_defs = players[(players["element_type"] == 2) & (players["now_cost"] <= 45)]
        if not cheap_defs.empty:
            best_cheap = cheap_defs.sort_values("form", ascending=False).head(3)
            return "Top cheap defenders under 4.5m:\n" + "\n".join(
                f"- {row['first_name']} {row['second_name']} ({row['team_name']}) | Form: {row['form']}" for _, row in best_cheap.iterrows()
            )
        return "No cheap defenders found."

    if "top" in query_lower:
        if "mid" in query_lower:
            mids = players[players["element_type"] == 3].sort_values("form", ascending=False).head(5)
            return "Top midfielders:\n" + "\n".join(
                f"- {row['first_name']} {row['second_name']} | Form: {row['form']} | Team: {row['team_name']}" for _, row in mids.iterrows()
            )
        elif "forward" in query_lower:
            fwds = players[players["element_type"] == 4].sort_values("form", ascending=False).head(5)
            return "Top forwards:\n" + "\n".join(
                f"- {row['first_name']} {row['second_name']} | Form: {row['form']} | Team: {row['team_name']}" for _, row in fwds.iterrows()
            )

    if "value" in query_lower or ("cheap" in query_lower and "good" in query_lower):
        players["value"] = players["form"] / (players["now_cost"] / 10)
        bargains = players.sort_values("value", ascending=False).head(5)
        return "Best value picks (Form per £1m):\n" + "\n".join(
            f"- {row['first_name']} {row['second_name']} | Form: {row['form']} | Price: £{row['now_cost'] / 10:.1f}" for _, row in bargains.iterrows()
        )

    if "differential" in query_lower or "low ownership" in query_lower:
        diff = players[(players["selected_by_percent"] < 20.0) & (players["form"].astype(float) > 2)]
        top_diff = diff.sort_values("form", ascending=False).head(5)
        return "Top differentials (<20% ownership):\n" + "\n".join(
            f"- {row['first_name']} {row['second_name']} | Team: {row['team_name']} | Form: {row['form']} | Owned by: {row['selected_by_percent']}%" for _, row in top_diff.iterrows()
        )

    for _, row in players.iterrows():
        full_name = f"{row['first_name']} {row['second_name']}".lower()
        if full_name in query_lower or row['second_name'].lower() in query_lower:
            matched_player = row
            break

    if matched_player is not None:
        player_info = (
            f"{matched_player['first_name']} {matched_player['second_name']} | "
            f"Team: {matched_player['team_name']} | Form: {matched_player['form']} | "
            f"Price: £{matched_player['now_cost'] / 10}"
        )
        prompt = (
            f"You are a Fantasy Premier League expert.\n\n"
            f"Player info:\n{player_info}\n\n"
            f"User question: {query}\n\n"
            f"Respond like an FPL advisor."
        )
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    return web_search(query)
