baseURL = 'https://www.acmicpc.net/group/ranklist/13872'
people = []

def get_user(html):
    arr = html.replace('<td>', '').split('</td>')
    name_first = arr[1].find('/user/') + 6
    name_end = arr[1].find('">', name_first)
    name = arr[1][name_first:name_end]

    correct = arr[3]
    correct_first = arr[3].find('>') + 1
    correct = arr[3].replace('</a>', '')[correct_first:]

    submission = arr[4]
    submission_first = arr[4].find('>') + 1
    submission = arr[4].replace('</a>', '')[submission_first:]
    return (name, int(correct), int(submission))

for i in range(1, 2+1):

    # temp
    # with open('test.html', 'w', encoding='utf-8') as f:
    #     f.write(html)
    html = ''
    with open(f'group{i}.html', 'r', encoding='utf-8') as f:
        html = f.read()
    # temp

    problem_first = html.find('id="ranklist"') + 13 # 13 letters
    problem_first = html.find('<tbody>', problem_first) + 7 # 7 letters
    problem_end = html.find('</tbody>', problem_first)
    html = html[problem_first:problem_end].replace('<tr>', '')
    arr = html.split('</tr>')
    arr.pop()

    for e in arr:
        people.append(get_user(e))

print(*people,sep='\n')