import time, datetime
import db, group_rank, user_info, solvedac_api

epoch_time = datetime.datetime.fromtimestamp(0)

problems_tier = {}

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
            user_tier = solvedac_api.user_tier(name)

            data = user_info.recent_solved_problems(name, db_people[name][2])
            last_solution = 0
            for solution, problem_id, date_time in data:
                last_solution = max(last_solution, solution)

                if not problem_id in problems_tier:
                    problems_tier[problem_id] = solvedac_api.problem_tier(problem_id)

                level = problems_tier[problem_id] - user_tier
                db.add_problem(name, problem_id, date_time, level)

            db.update_user(name, corrects, submissions, last_solution)

        else:
            solution = user_info.last_solution(name, "init")
            db.update_user(name, corrects, submissions, solution)
            
            problems = user_info.solved_problems(name, "init")
            for problem_id in problems:
                db.add_problem(name, problem_id, epoch_time, 0)

        time.sleep(1)

db.close()