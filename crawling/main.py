import time, schedule, os, sys
from info import group_rank, user_info, solvedac_api
from repository import service
import broadcast, logger
from logger import msg, warning, error, debug, LogLevel

logger.set_level(LogLevel.DEBUG)

problems_tier = {}

service.open_db()
scores = service.get_score()
ranks = service.get_score_and_rank(scores)
pre_lotto = service.get_shuffle(ranks)
service.close_db()

def do_crawling():
    global pre_lotto
    msg("크롤링 시작...")
    service.open_db()

    db_people = {}
    for id, name, corrects, submissions, solution in service.get_user():
        db_people[name] = (corrects, submissions, solution)

    people = group_rank.get_group_member()
    for name, corrects, submissions in people:
        # msg(f'{name}님의 정보를 가져오는 중입니다.')
        if corrects == 0: continue  # 맞힌 문제가 0이면 탐색 안함

        if name in db_people:
            if db_people[name][1] == submissions: continue  # 제출 수 변화가 없으면 탐색 안함
            user_tier = solvedac_api.user_tier(name)

            data = user_info.recent_solved_problems(name, db_people[name][2])
            last_solution = db_people[name][2]
            for solution, problem_id, date_time in data:
                last_solution = max(last_solution, solution)

                if not problem_id in problems_tier:
                    problems_tier[problem_id] = solvedac_api.problem_tier(problem_id)

                level = problems_tier[problem_id] - user_tier
                service.add_problem(name, problem_id, level, date_time)

            service.update_user(name, corrects, submissions, last_solution)

            msg(f'{name}님 정보의 업데이트가 완료되었습니다. (새로 푼 문제 수: {len(data)})')

        else:
            solution = user_info.last_solution(name, "init")
            service.update_user(name, corrects, submissions, solution)

            problems = user_info.solved_problems(name, "init")
            for problem_id in problems:
                service.add_problem(name, problem_id, 0)

            msg(f'{name}님 정보를 초기화 했습니다. (맞힌 문제 수: {corrects}, 제출 수: {submissions})')

        time.sleep(1)

    scores = service.get_score()
    ranks = service.get_score_and_rank(scores)
    lotto = service.get_shuffle(ranks)
    if pre_lotto != lotto:
        msg("추첨 결과가 바뀌어 디스코드에 알림을 보냅니다.")
        pre_lotto = lotto
        broadcast.broadcast(lotto)
    else:
        msg("추첨 결과 변화가 없어 디스코드 알림을 보내지 않습니다.")

    broadcast.notify()
    service.close_db()
    msg("크롤링 완료!")

msg("Hello, World!")

schedule.every().hour.at(":00").do(do_crawling)
schedule.every().hour.at(":05").do(do_crawling)
schedule.every().hour.at(":10").do(do_crawling)
schedule.every().hour.at(":15").do(do_crawling)
schedule.every().hour.at(":20").do(do_crawling)
schedule.every().hour.at(":25").do(do_crawling)
schedule.every().hour.at(":30").do(do_crawling)
schedule.every().hour.at(":35").do(do_crawling)
schedule.every().hour.at(":40").do(do_crawling)
schedule.every().hour.at(":45").do(do_crawling)
schedule.every().hour.at(":50").do(do_crawling)
schedule.every().hour.at(":55").do(do_crawling)

while True:
    schedule.run_pending()
    time.sleep(1)