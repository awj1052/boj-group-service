import db

def get_score_by_month(year, month):
    data = {}
    for day in range(1, 31+1):
        res = db.get_score_by_day(year, month, day)
        s = set(e[0] for e in res if e[1] >= -5)
        for e in s:
            if not e in data:
                data[e] = 0
            data[e] += 1
    return data

def get_score_by_evnet():
    data = {}
    for event in db.get_event():
        res = db.get_score_by_problem_and_period(event[2], event[3], event[4])
        s = set(e[0] for e in res) # ignore level
        for e in s:
            if not e in data:
                data[e] = 0
            data[e] += 1
    return data
        
# TODO event : add, truncate, delete
def add_event():
    pass