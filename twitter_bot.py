import tweepy
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Load Twitter credentials
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_secret = os.getenv("TWITTER_ACCESS_SECRET")

# Load OpenAI key (if using GPT to generate replies)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Twitter authentication
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)

# Get mentions
mentions = api.mentions_timeline(count=1)

for mention in mentions:
    user = mention.user.screen_name
    text = mention.text
    tweet_id = mention.id

    # Remove @yourusername from the text
    prompt = text.replace(f"@{api.me().screen_name}", "").strip()

    # Generate a response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    reply_text = f"@{user} {response.choices[0].message['content'].strip()}"

    # Post the reply
    api.update_status(status=reply_text, in_reply_to_status_id=tweet_id)

    print("Twitter bot loaded.")

