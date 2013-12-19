from taskr import db
from datetime import datetime
from config import DATABASE_PATH
import sqlite3

with sqlite3.connect(DATABASE_PATH) as connection:
	con = connection.cursor()

	con.execute("DROP TABLE old_ftasks2")

	con.execute("""ALTER TABLE ftasks RENAME TO old_ftasks2""")

	db.create_all()

	con.execute("""SELECT name, due_date, posted_date, priority, status FROM old_ftasks2 ORDER BY task_id ASC""")

	data = [(row[0], row[1], row[2], row[3], datetime.now(), 1) for row in con.fetchall()]

	con.executemany("""INSERT INTO ftasks (name, amount, due_date, priority, status, posted_date, user_id) VALUES (?,?,?,?,?,?,?)""", data)

	con.execute("DROP TABLE old_ftasks2")
