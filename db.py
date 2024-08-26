import os, pymysql
from dotenv import load_dotenv

def _init():
    load_dotenv()

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_DATABASE = os.getenv("DB_DATABASE")

    conn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd = DB_PASSWORD, db=DB_DATABASE, port=DB_PORT)
    return conn.cursor()

cursor = _init()