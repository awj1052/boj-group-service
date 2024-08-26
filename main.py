import time, datetime
import db, group_rank, user_info, solvedac_api

epoch_time = datetime.datetime.fromtimestamp(0)

for i in range(1): # iter
    
    db_people = {}
    for id, name, corrects, submissions, solution in db.get_user():
        db_people[name] = (corrects, submissions, solution)

    people = group_rank.get_group_member()
    for name, corrects, submissions in people:
        print(name)
        if corrects == 0: continue # 맞힌 문제가 0이면 탐색 안함
        if name in db_people:
            if db_people[name][1] == submissions: continue  # 제출 수 변화가 없으면 탐색 안함

            problems_dict = {}
            data = user_info.recent_solved_problems(name, db_people[name][2])
            for solution, problem_id, date_time in data:
                if problem_id in problems_dict:
                    problems_dict[problem_id] = max(problems_dict[problem_id], date_time)
                else:
                    problems_dict[problem_id] = date_time

            for key, item in problems_dict.items():
                db.add_problem(name, key, item)

        else:
            solution = user_info.last_solution(name, "init")
            db.update_user(name, corrects, submissions, solution)
            
            problems = user_info.solved_problems(name, "init")
            for problem_id in problems:
                db.add_problem(name, problem_id, epoch_time)

        time.sleep(1)