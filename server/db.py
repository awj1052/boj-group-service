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

# SELECT m.name, p.level FROM member m LEFT JOIN problem p ON p.name = m.name WHERE p.problem > 5000;

def get_score_by_day(year, month, day):
    conn = pool.get_connection()
    res = None
    with conn.cursor() as cursor:
        sql = """
            SELECT 
                m.name, 
                p.level
            FROM member m
            LEFT JOIN problem p
            ON m.name = p.name
            WHERE YEAR(p.time) = %s AND MONTH(p.time) = %s AND DAY(p.time) = %s AND p.repeatation = 0 AND p.level >= -5
        """
        rows = cursor.execute(sql, (year, month, day))
        res = cursor.fetchall()
    conn.close()
    return res

def get_score_by_problem_and_period(year, month, start_time, end_time, problem_id):
    conn = pool.get_connection()
    res = None
    with conn.cursor() as cursor:
        sql = """
            SELECT 
                m.name, 
                p.level
            FROM member m
            LEFT JOIN problem p
            ON m.name = p.name
            WHERE YEAR(p.time) = %s AND MONTH(p.time) = %s AND (p.time BETWEEN %s AND %s) AND p.problem = %s;
        """
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

def get_log_by_month(year, month):
    conn = pool.get_connection()
    res = None
    with conn.cursor() as cursor:
        sql = """
            SELECT 
                m.name, 
                p.time 
            FROM member m
            LEFT JOIN problem p
            ON m.name = p.name 
            WHERE YEAR(p.time) = %s AND MONTH(p.time) = %s AND p.repeatation = 0 AND p.level >= -5 ORDER BY p.time DESC LIMIT 10;
        """
        rows = cursor.execute(sql, (year, month))
        res = cursor.fetchall()
    conn.close()
    return res