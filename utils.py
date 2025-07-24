from serpapi import GoogleSearch
from env_setup import serpapi_key

def web_search(query):
    search = GoogleSearch({
        "q": query,
        "api_key": serpapi_key,
        "num": 1
    })
    results = search.get_dict()
    if "organic_results" in results and results["organic_results"]:
        top = results["organic_results"][0]
        return f"**{top.get('title')}**\n\n{top.get('snippet')}\n\n{top.get('link')}"
    else:
        return "No relevant web results found."
