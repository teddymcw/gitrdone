import sqlite3
from config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
	con = connection.cursor()
	#AUTOINCREMENT means that an id is automatically generated I believe
	con.execute("""
				CREATE TABLE ftasks(
				task_id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL, 
				due_date TEXT NOT NULL, 
				priority INTEGER NOT NULL,
				status INTEGER NOT NULL
				)
				""")

	#dummy data 
	con.execute('INSERT INTO ftasks (name, due_date, priority, status) VALUES("Finish this tutorial", "02/03/2013", 10, 1)')

	con.execute('INSERT INTO ftasks (name, due_date, priority, status) VALUES("Finish my book", "02/03/2013", 10, 1)')

@app.route("/tasks/")
@login_required
def tasks():
	g.db = connect_db()
	cur = g.db.execute('select name, due_date, priority, task_id from ftasks where status=1')
	#list comprehension for open_tasks var
	open_tasks = [dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in cur.fetchall()]
	cur = g.db.execute('select name, due_date, priority, task_id from ftasks where status=0')
	#list comprehension for closed_tasks var
	closed_tasks = [dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in cur.fetchall()]
	g.db.close()
	return render_template('tasks.html', open_tasks=open_tasks, closed_tasks=closed_tasks)

#single login looks much different than multiple logins

@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
	g.db = connect_db()
	name = request.form['name']
	date = request.form['due_date']
	priority = request.form['priority']
	if not name or not date or not priority:
		flash("All fields are required. Please try again.")
		return redirect(url_for('tasks'))
	else:	
	#two line insert statement
		g.db.execute('insert into ftasks (name, due_date, priority, status) values (?, ?, ?, 1)', 
			[request.form['name'], request.form['due_date'], request.form['priority']])
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted. Thanks.')
		return redirect(url_for('tasks'))

#mark tasks as complete WATCH THE COMMA?
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	g.db = connect_db()
	cur = g.db.execute('update ftasks set status = 0 where task_id='+str(task_id))
	g.db.commit()
	g.db.close()
	flash('The task was marked as complete.')
	return redirect(url_for('tasks'))

#delete tasks WATCH THE COMMA?
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	g.db = connect_db()
	cur = g.db.execute('delete from ftasks where task_id='+str(task_id))
	g.db.commit()
	g.db.close()
	flash('The task was deleted.')
	return redirect(url_for('tasks'))