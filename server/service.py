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

def get_score_by_event():
    data = {}
    for event in db.get_event():
        res = db.get_score_by_problem_and_period(event[2], event[3], event[4])
        s = set(e[0] for e in res) # ignore level
        for e in s:
            if not e in data:
                data[e] = 0
            data[e] += 1
    return data
        
def get_event():
    return db.get_event()

def add_event(description, start_time, end_time, problem_id):
    return db.add_event(description, start_time, end_time, problem_id)

def truncate_event():
    return db.truncate_event()

def delete_event_by_id(id):
    return db.delete_event_by_id(id)

def delete_event_by_description(description):
    return db.delete_event_by_description(description)