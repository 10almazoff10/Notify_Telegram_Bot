import sqlite3
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
user_status = 3
id_user = 758952233


sql = "SELECT * FROM users_data WHERE id=?"
cursor.execute(sql, [(id_user)])
print(cursor.fetchone())
status = cursor.fetchone()[5]
print(status)