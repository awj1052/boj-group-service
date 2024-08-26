import requests, os
from dotenv import load_dotenv
load_dotenv()

USER_INFO = os.getenv("USER_INFO")
USER_SUBMITTION = os.getenv("USER_SUBMITTION")

def solved_problems(username):
    response = requests.get(
        url = f'{USER_INFO}/{username}',
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        },
    )

    html = response.text

    problem_list = html.find('<div class="problem-list">') + 26 # 26 letters
    problem_list_end = html.find("</div>", problem_list)
    html = html[problem_list:problem_list_end].replace('<a href="/problem/', '').replace('" class="">', ' ').replace('</a>', ' ')
    problems = list(map(int,html.split()))
    return problems

def recent_solved_problems(username, last_submit, query=''):
    response = requests.get(
        url = f'{USER_SUBMITTION}user_id={username}&{query}',
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        },
    )

    html = response.text

    