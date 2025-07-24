import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("fpl.env")
openai_api_key = os.getenv("OPENAI_API_KEY")
serpapi_key = os.getenv("SERPAPI_KEY")

client = OpenAI(api_key=openai_api_key)
