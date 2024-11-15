import sqlite3

conn = sqlite3.connect('storage.db')

cursor = conn.cursor()

cursor.execute("SELECT * FROM your_table_name")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
