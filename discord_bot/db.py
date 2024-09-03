import os, pymysql
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

conn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd = DB_PASSWORD, db=DB_DATABASE, port=DB_PORT)

__cursor = conn.cursor()

def close():
    __cursor.close()
    conn.close()

def get_event():
    sql = "SELECT * FROM event"
    rows = __cursor.execute(sql)
    return __cursor.fetchall()

def truncate_event():
    sql = "DELETE FROM event"
    rows =  __cursor.execute(sql)
    sql = "ALTER TABLE event AUTO_INCREMENT = 1;"
    __cursor.execute(sql)
    conn.commit()
    return rows

def add_event(description, start_time, end_time, problem_id):
    sql = "INSERT INTO event (description, start_time, end_time, problem_id) VALUES (%s, %s, %s, %s)"
    rows = __cursor.execute(sql, (description, start_time, end_time, problem_id))
    conn.commit()
    return rows

def delete_event_by_id(id):
    sql = "DELETE FROM event WHERE id = %s"
    rows = __cursor.execute(sql, (id))
    conn.commit()
    return rows

def delete_event_by_description(description):
    sql = "DELETE FROM event WHERE description = %s"
    rows = __cursor.execute(sql, (description))
    conn.commit()
    return rows

def get_member():
    sql = "SELECT name FROM member"
    rows = __cursor.execute(sql)
    return __cursor.fetchall()

def add_member(name):
    sql = "INSERT INTO member (name) VALUES (%s)"
    rows = __cursor.execute(sql, (name))
    conn.commit()
    return __cursor.fetchall()

def truncate_member():
    sql = "DELETE FROM member"
    rows =  __cursor.execute(sql)
    sql = "ALTER TABLE member AUTO_INCREMENT = 1;"
    __cursor.execute(sql)
    return rows

def delete_member(name):
    sql = "DELETE FROM member WHERE name = %s"
    rows = __cursor.execute(sql, (name))
    return rows