import requests, os
from dotenv import load_dotenv
load_dotenv()

BOT_BROADCAST_URL = os.getenv("BOT_BROADCAST_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SITE_URL = os.getenv("SITE_URL")

def broadcast(lotto):
    message = [
        "추첨 결과가 바뀌었습니다.",
        f"{SITE_URL} 에서 확인하세요!",
        ""
    ]
    for i in range(len(lotto)):
        message.append(f"{i+1}. `{lotto[i][0]}`: {lotto[i][1]} 문제")
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bot {BOT_TOKEN}",
    }
    content = {
        "content": "\n".join(message)
    }
    requests.post(BOT_BROADCAST_URL, headers=header, json=content)

def notify():
    requests.post("http://localhost:8080/notify/score")