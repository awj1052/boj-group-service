import os, pymysql, datetime
from dotenv import load_dotenv
from pymysql.connections import Connection
from pymysql.cursors import Cursor

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

conn: Connection
__cursor: Cursor

def open_db():
    global conn, __cursor
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd = DB_PASSWORD, db=DB_DATABASE, port=DB_PORT)
    __cursor = conn.cursor()

def close_db():
    __cursor.close()
    conn.close()

def get_user(username: str = '') -> tuple:
    """
    Args:
        username (str): 비워두면 모두 가져온다.

    Returns:
        tuple: (id, name, corrects, submissions, solution)
    """
    if username == '':
        sql = "SELECT * FROM user"
        rows = __cursor.execute(sql)
    else:
        sql = "SELECT * FROM user WHERE name = %s"
        rows = __cursor.execute(sql, username)
    return __cursor.fetchall()

def update_user(username: str, corrects: int, submissions: int, solution: int) -> int:
    """
    없으면 추가하고, 있으면 갱신한다.
    Args:
        username (str): 이름
        corrects (int): 맞은 문제
        submissions (int): 제출
        solution (int): 마지막 제출번호

    Returns:
        int: 변경된 행 수
    """
    sql = "SELECT name FROM user WHERE name = %s"
    rows = __cursor.execute(sql, (username))
    if rows == 0:
        sql = "INSERT INTO user (corrects, submissions, solution, name) VALUES (%s, %s, %s, %s)"
    else:
        sql = "UPDATE user SET corrects = %s, submissions = %s, solution = %s WHERE name = %s"
    rows = __cursor.execute(sql, (corrects, submissions, solution, username))
    conn.commit()
    return rows

# time = "2024-08-25 19:52:59"
# time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
def add_problem(username: str, problem_id: int, level: int, time = datetime.datetime.fromtimestamp(0)) -> int:
    """
    문제 해결했음을 기록한다.
    Args:
        username (str): 이름
        problem_id (int): 문제 번호
        level (int): 문제티어 - 유저티어
        time (datetime): 푼 시간
    Returns:
        int: 변경된 행 수
    """
    sql = "SELECT name FROM problem WHERE name = %s AND problem = %s"
    rows = __cursor.execute(sql, (username, problem_id))
    sql = "INSERT INTO problem (name, problem, time, level, repeatation) VALUES (%s, %s, %s, %s, %s)"
    rows = __cursor.execute(sql, (username, problem_id, time, level, rows))
    conn.commit()
    return rows

def get_problems(username: str) -> tuple:
    """
    특정 유저가 푼 문제들을 모두 가져온다
    Args:
        username (str): 이름

    Returns:
        tuple: (id, name, problem, time, level, repeatation)
    """
    sql = "SELECT * FROM problem WHERE name = %s"
    rows = __cursor.execute(sql, (username))
    return __cursor.fetchall()

def get_users_by_problem(problem_id: int) -> tuple:
    """
    특정 문제 번호의 데이터를 가져온다.
    Args:
        problem_id (int): 문제 번호

    Returns:
        tuple: (id, name, problem, time, level, repeatation)
    """
    sql = "SELECT * FROM problem WHERE problem = %s"
    rows = __cursor.execute(sql, (problem_id))
    return __cursor.fetchall()

# print(update_user("qwe", 12, 2, 3))
# print(get_user("awj1052"))
# print(add_problem("awj1052", 2, datetime.datetime.now()))
# print(get_problems("awj1052"))

def get_score_by_day(year, month, day):
    sql = """
        SELECT 
            m.name, 
            p.level
        FROM member m
        LEFT JOIN problem p
        ON m.name = p.name
        WHERE YEAR(p.time) = %s AND MONTH(p.time) = %s AND DAY(p.time) = %s AND p.repeatation = 0 AND p.level >= -5
    """
    rows = __cursor.execute(sql, (year, month, day))
    return __cursor.fetchall()

def get_score_by_problem_and_period(year, month, start_time, end_time, problem_id):
    sql = """
        SELECT 
            m.name, 
            p.level
        FROM member m
        LEFT JOIN problem p
        ON m.name = p.name
        WHERE YEAR(p.time) = %s AND MONTH(p.time) = %s AND (p.time BETWEEN %s AND %s) AND p.problem = %s;
    """
    rows = __cursor.execute(sql, (year, month, start_time, end_time, problem_id))
    return __cursor.fetchall()

def get_event_by_month(year, month):
    sql = "SELECT * FROM event WHERE YEAR(start_time) = %s AND MONTH(start_time) = %s"
    rows = __cursor.execute(sql, (year, month))
    return __cursor.fetchall()