import db, datetime, random

def get_score():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    json = get_score_by_month(year, month)
    res = get_score_by_event(year, month)
    for e in res:
        if not e in json:
            json[e] = 0
        json[e] += res[e]
    return json

def get_score_and_rank(json):
    data = [(name, score) for name, score in json.items()]
    data.sort(key=lambda x : -x[1])
    return data

def get_shuffle(json):
    random.seed("ANA")
    weighted_user = []
    for name, score in json.items():
        for i in range(score):
            weighted_user.append(name)
    random.shuffle(weighted_user)
    shuffled = list(dict.fromkeys(weighted_user))
    res = [(name, json[name]) for name in shuffled]
    return res

def get_log():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    return db.get_log_by_month(year, month)

def get_score_by_month(year, month):
    data = {}
    for day in range(1, 31+1):
        res = db.get_score_by_day(year, month, day)
        s = set(e[0] for e in res)
        for e in s:
            if not e in data:
                data[e] = 0
            data[e] += 1
    return data

def get_score_by_event(year, month):
    data = {}
    for event in db.get_event():
        res = db.get_score_by_problem_and_period(year, month, event[2], event[3], event[4])
        s = set(e[0] for e in res)
        for e in s:
            if not e in data:
                data[e] = 0
            data[e] += 1
    return data

def get_event_by_month(year, month):
    data = {}
    for event in db.get_event_by_month(year, month):
        name, problem_id = event[1], event[4]
        if not name in data:
            data[name] = []
        data[name].append(problem_id)
    return data