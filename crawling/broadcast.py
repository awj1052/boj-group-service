import requests, os
from dotenv import load_dotenv
load_dotenv()

BOT_BROADCAST_URL = os.getenv("BOT_BROADCAST_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

def broadcast(msg):
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bot {BOT_TOKEN}",
    }
    content = {
        "content": msg
    }
    requests.post(BOT_BROADCAST_URL, headers=header, json=content)