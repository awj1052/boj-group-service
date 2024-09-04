import time, schedule, os, sys
import group_rank, user_info, solvedac_api, service, broadcast
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logger
from logger import msg, warning, error, debug, LogLevel

logger.set_level(LogLevel.DEBUG)

problems_tier = {}

@schedule.repeat(schedule.every().hour.at(":00")) # 매시 정각마다
def do_crawling():
    msg("크롤링 시작...")
    service.open_db()

    scores = service.get_score()
    lotto = service.get_shuffle(scores)

    db_people = {}
    for id, name, corrects, submissions, solution in service.get_user():
        db_people[name] = (corrects, submissions, solution)

    people = group_rank.get_group_member()
    for name, corrects, submissions in people:
        print(f'현재 {name}님의 정보를 가져오는 중입니다.')
        if corrects == 0: continue  # 맞힌 문제가 0이면 탐색 안함

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
                service.add_problem(name, problem_id, level, date_time)

            service.update_user(name, corrects, submissions, last_solution)

        else:
            solution = user_info.last_solution(name, "init")
            service.update_user(name, corrects, submissions, solution)

            problems = user_info.solved_problems(name, "init")
            for problem_id in problems:
                service.add_problem(name, problem_id, 0)

        time.sleep(1)
    service.close_db()
    msg("크롤링 완료!")

    scores = service.get_score()
    lotto_after = service.get_shuffle(scores)
    if lotto != lotto_after:
        broadcast.broadcast(lotto_after)

msg("Hello, World!")
while True:
    schedule.run_pending()
    time.sleep(1)