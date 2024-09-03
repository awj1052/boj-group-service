import os, pymysqlpool
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

config={'host': DB_HOST, 'user': DB_USER, 'password': DB_PASSWORD, 'database': DB_DATABASE, 'autocommit':True}

pool = pymysqlpool.ConnectionPool(size=5, maxsize=10, pre_create_num=5, name='pool1', **config)

# conn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd = DB_PASSWORD, db=DB_DATABASE, port=DB_PORT)

def get_score_by_day(year, month, day):
    conn = pool.get_connection()
    res = None
    with conn.cursor() as cursor:
        sql = "SELECT name, level FROM problem WHERE repeatation = 0 AND YEAR(time) = %s AND MONTH(time) = %s AND DAY(time) = %s;"
        rows = cursor.execute(sql, (year, month, day))
        res = cursor.fetchall()
    conn.close()
    return res

def get_score_by_problem_and_period(year, month, start_time, end_time, problem_id):
    conn = pool.get_connection()
    res = None
    with conn.cursor() as cursor:
        sql = "SELECT name, level FROM problem WHERE YEAR(time) = %s AND MONTH(time) = %s AND (time BETWEEN %s AND %s) AND problem = %s;"
        rows = cursor.execute(sql, (year, month, start_time, end_time, problem_id))
        res = cursor.fetchall()
    conn.close()
    return res

def get_event():
    conn = pool.get_connection()
    res = None
    with conn.cursor() as cursor:
        sql = "SELECT * FROM event"
        rows = cursor.execute(sql)
        res = cursor.fetchall()
    conn.close()
    return res

def get_event_by_month(year, month):
    conn = pool.get_connection()
    res = None
    with conn.cursor() as cursor:
        sql = "SELECT * FROM event WHERE YEAR(time) = %s AND MONTH(time) = %s"
        rows = cursor.execute(sql)
        res = cursor.fetchall()
    conn.close()
    return res