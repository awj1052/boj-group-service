import requests, os
from dotenv import load_dotenv

load_dotenv()
PROBLEM_TIER_API = os.getenv("PROBLEM_TIER_API")
USER_TIER_API = os.getenv("USER_TIER_API")

def problem_tier(problem_id):
    response = requests.get(
        url= f"{PROBLEM_TIER_API}?problemId={problem_id}",
        headers= {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        },
    )
    return response.json()["level"]

def user_tier(username):
    response = requests.get(
        url= f"{USER_TIER_API}?handle={username}",
        headers= {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        },
    )
    return response.json()["tier"]