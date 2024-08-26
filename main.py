import db

cursor = db.cursor
cursor.execute("SHOW TABLES")
print(cursor.fetchall())