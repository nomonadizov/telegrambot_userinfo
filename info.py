import sqlite3

conn = sqlite3.connect('userinfo.db')

cursor = conn.cursor()

cursor.execute("SELECT * FROM info_of_user")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
