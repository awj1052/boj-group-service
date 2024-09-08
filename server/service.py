import db, datetime, random, os
from dotenv import load_dotenv
load_dotenv()

RANDOM_SEED = os.getenv("RANDOM_SEED")

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
    bias = get_bias()
    for e in bias:
        if bias[e] == 0: continue
        if not e in json:
            json[e] = 0
        json[e] += bias[e]
    return json

def get_score_and_rank(json):
    data = [(name, score) for name, score in json.items()]
    data.sort(key=lambda x : (-x[1], x[0]))
    return data

def get_shuffle(ranks):
    random.seed(RANDOM_SEED)
    weighted_user = []
    for name, score in ranks:
        for i in range(score):
            weighted_user.append((name, score))
    random.shuffle(weighted_user)
    shuffled = list(dict.fromkeys(weighted_user))
    res = [(name, score) for name, score in shuffled]
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
    for event in db.get_event_by_month(year, month):
        res = db.get_score_by_problem_and_period(year, month, event[2], event[3], event[4])
        s = set(e[0] for e in res)
        for e in s:
            if not e in data:
                data[e] = 0
            data[e] += 1
    return data


def get_events():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    events = db.get_event_by_month(year, month)
    distinct_events = []
    names = set()
    for event in events:
        if event[1] in names:
            continue
        names.add(event[1])
        distinct_events.append(event)
    return distinct_events

def get_bias():
    data = {}
    for e in db.get_bias():
        data[e[0]] = e[1]
    return data