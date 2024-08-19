import db

cursor = db.get_cursor()
cursor.execute("SHOW TABLES")
print(cursor.fetchall())