from datetime import datetime, timedelta
from typing import List, Type, Any, Tuple
import sqlalchemy, os, pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine, Row
from sqlalchemy.orm import Session, sessionmaker
from repository.orm import *

load_dotenv()

DB_NAME = 'mariadb'
DB_CONNECTOR = 'pymysql'
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

engine: Engine
session: Session

def open_db(echo=False):
    """
    DB를 열고 세션을 생성한다.
    Args:
        echo: SQL 출력 여부

    """
    global engine, session
    engine = create_engine(f'{DB_NAME}+{DB_CONNECTOR}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}', echo=echo)
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    Base.metadata.create_all(engine)

def close_db():
    """
    DB와 세션을 모두 닫는다.
    Returns:

    """
    session.close_all()
    engine.dispose()

def get_user(username: str = '') -> list[Type[User]] | list[Any] | list[User]:
    """
    Args:
        username: 비워두면 모두 가져온다.

    Returns:
        list: User 객체 리스트
    """
    if username == '':
        users = session.query(User).all()
        return users
    user = session.query(User).filter(User.name == username).first()
    if user is None: return []
    return [user]

def update_user(user: User) -> Type[User]:
    """
    없으면 추가하고 있으면 갱신한다.
    Args:
        user: 추가하거나 업데이트할 User 객체

    Returns: DB에 추가된 User 객체

    """
    u = get_user(user.name)
    if len(u) == 0:
        session.add(user)
        session.commit()
        return user
    else:
        u = u[0]
        u.corrects = user.corrects
        u.submissions = user.submissions
        u.solution = user.solution
        session.commit()
        return u

def add_problem(problem: Problem) -> Problem:
    """
    문제 해결했음을 기록한다.
    Args:
        problem:

    Returns:

    """
    repeatation = (session.query(Problem.name)
                   .filter(Problem.name == problem.name, Problem.problem == problem.problem).count())
    problem.repeatation = repeatation
    session.add(problem)
    session.commit()
    return problem

def get_problems(username: str) -> list[Type[Problem]]:
    problems = session.query(Problem).filter(Problem.name == username).all()
    return problems

def get_users_by_problem(problem_id: int) -> list[Type[User]]:
    users = session.query(User).filter(User.solution == problem_id).all()
    return users

def get_score_by_day(year: int, month: int, day: int) -> list[Row[tuple[str, int]]]:
    start = datetime(year, month, day)
    end = start + timedelta(days=1)
    ret = session.query(Member.name, Problem.level).filter(Problem.name == Member.name,
        Problem.time >= start, Problem.time < end, Problem.repeatation == 0, Problem.level >= -5).all()
    return ret

def get_score_by_problem_and_period(start_time: datetime, end_time: datetime, problem_id: int) -> list[Row[tuple[str, int]]]:
    ret = session.query(Member.name, Problem.level).filter(Problem.name == Member.name,
        Problem.time >= start_time, Problem.time < end_time, Problem.problem == problem_id).all()
    return ret

def get_event_by_month(year: int, month: int ) -> list[Type[Event]]:
    ret = session.query(Event).filter(
        sqlalchemy.extract('year', Event.start_time) == year,
        sqlalchemy.extract('month', Event.start_time) == month).all()
    return ret

def get_bias() -> list[Row[tuple[str, int]]]:
    ret = session.query(Member.name, Member.bias).all()
    return ret

if __name__ == '__main__':
    open_db()
    import db
    db.open_db()
    print(engine)
    # print(update_user(User(name='test', corrects=5, submissions=100, solution=100)))
    # print(add_problem(Problem(name='test', problem=101, time=datetime.now(), level=1, repeatation=1)))
    # print(get_score_by_day(2024, 9, 10))
    e = get_event_by_month(2024, 9)

    engine.dispose()