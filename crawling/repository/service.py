from repository import database
from repository.orm import *
import datetime, random, os, calendar
from typing import Type
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

def get_score_by_month(year, month):
    data = {}
    for day in range(*calendar.monthrange(year, month)):
        res = database.get_score_by_day(year, month, day)
        s = set(e[0] for e in res)
        for e in s:
            if not e in data:
                data[e] = 0
            data[e] += 1
    return data

def get_score_by_event(year, month):
    data = {}
    for event in database.get_event_by_month(year, month):
        res = database.get_score_by_problem_and_period(event.start_time, event.end_time, event.problem_id)
        s = set(e[0] for e in res)
        for e in s:
            if not e in data:
                data[e] = 0
            data[e] += 1
    return data

def open_db():
    database.open_db()

def close_db():
    database.close_db()

def update_user(username: str, corrects: int, submissions: int, solution: int) -> Type[User]:
    return database.update_user(User(name=username, corrects=corrects, submissions=submissions, solution=solution))

def add_problem(username: str, problem_id: int, level: int, time = datetime.datetime.fromtimestamp(0)):
    database.add_problem(Problem(name=username, time=time, level=level, problem=problem_id))

def get_user():
    return database.get_user()

def get_bias():
    data = {}
    for e in database.get_bias():
        data[e[0]] = e[1]
    return data


if __name__ == '__main__':
    open_db()

    print(get_score_by_event(2024, 9))

    close_db()