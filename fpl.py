import requests
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="fpl.env")
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def fetch_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        players = pd.DataFrame(data["elements"])
        return players
    else:
        print("Failed to fetch FPL data")
        return pd.DataFrame()

def ask_fpl_llm(question, players):
    # Format a summary of the FPL data (e.g., top 10 players by form)
    top_players = players.sort_values(by="form", ascending=False).head(10)
    player_list = "\n".join([
        f"- {row['first_name']} {row['second_name']}: {row['form']} form"
        for _, row in top_players.iterrows()
    ])
    prompt = (
        f"You are an expert on Fantasy Premier League. Here is some player data:\n"
        f"{player_list}\n\n"
        f"User question: {question}\n"
        f"Answer in detail."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    players = fetch_fpl_data()
    if not players.empty:
        question = input("Ask any FPL question: ")
        answer = ask_fpl_llm(question, players)
        print("\nLLM Answer:\n", answer)

if __name__ == "__main__":
    main()
