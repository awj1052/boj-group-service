# import requests

# baseURL = 'https://www.acmicpc.net/user/awj1052'
# response = requests.get(
#     url=baseURL,
#     headers= {
#         "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
#     },
# )

# html = response.text

# temp
# with open('test.html', 'w', encoding='utf-8') as f:
#     f.write(html)
html = ''
with open('test.html', 'r', encoding='utf-8') as f:
    html = f.read()
# temp

problem_list = html.find('<div class="problem-list">') + 26 # 26 letters
problem_list_end = html.find("</div>", problem_list)
html = html[problem_list:problem_list_end].replace('<a href="/problem/', '').replace('" class="">', ' ').replace('</a>', ' ')
problems = set(list(map(int,html.split())))
print(*problems)
print(len(problems))