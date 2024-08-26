import os, pymysql, datetime
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

conn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd = DB_PASSWORD, db=DB_DATABASE, port=DB_PORT)

_cursor = conn.cursor()

def close():
    _cursor.close()
    conn.close()

def get_user(username=''):
    if username == '':
        sql = "SELECT * FROM user"
        rows = _cursor.execute(sql)
    else:
        sql = "SELECT * FROM user WHERE name = %s"
        rows = _cursor.execute(sql, username)
    return _cursor.fetchall()

def update_user(username, corrects, submissions, solution):
    sql = "SELECT * FROM user WHERE name = %s"
    rows = _cursor.execute(sql, (username))
    if rows == 0:
        sql = "INSERT INTO user (corrects, submissions, solution, name) VALUES (%s, %s, %s, %s)"
    else:
        sql = "UPDATE user SET corrects = %s, submissions = %s, solution = %s WHERE name = %s"
    rows = _cursor.execute(sql, (corrects, submissions, solution, username))
    conn.commit()
    return rows

# time = "2024-08-25 19:52:59"
# time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
def add_problem(username, problem_id, time):
    sql = "SELECT * FROM problem WHERE name = %s AND problem = %s"
    rows = _cursor.execute(sql, (username, problem_id))
    if rows != 0:
        sql = "UPDATE problem SET time = %s WHERE name = %s AND problem = %s"
        rows = _cursor.execute(sql, (time, username, problem_id))
    else:
        sql = "INSERT INTO problem (name, problem, time) VALUES (%s, %s, %s)"
        rows = _cursor.execute(sql, (username, problem_id, time))
    conn.commit()
    return rows

def get_problems(username):
    sql = "SELECT * FROM problem WHERE name = %s"
    rows = _cursor.execute(sql, (username))
    return _cursor.fetchall()

def get_users_by_problem(problem_id):
    sql = "SELECT * FROM problem WHERE problem = %s"
    rows = _cursor.execute(sql, (problem_id))
    return _cursor.fetchall()

# print(update_user("qwe", 12, 2, 3))
# print(get_user("awj1052"))
# print(add_problem("awj1052", 2, datetime.datetime.now()))
# print(get_problems("awj1052"))