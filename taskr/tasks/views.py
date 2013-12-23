from taskr import app, db
from flask import Flask, render_template, request, session, flash, redirect, url_for, session, g
from functools import wraps
from taskr.forms import AddTask, RegisterForm, LoginForm
from taskr.models import FTasks, User
from sqlalchemy.exc import IntegrityError

#removed app and app.config to place it in the __init__.py


#objective with views is to make the flashes big and almost gamified when
#a user actually starts using the app
def flash_errors(form):
	for field, errors in form.errors.items():	#trouble tracing the variables here
		for error in errors:
			flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error), 'error')


def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.') #shouldn't this gather from the for loop?
			return redirect(url_for('login'))
	return wrap

#routing is confusing here again
#would like: @app.route("/", "/login/", methods=['GET', 'POST']) but route takes two args only
@app.route("/", methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':	#where do we define what this http method is?
		u = User.query.filter_by(name=request.form['name'], password=request.form['password']).first()
		if u is None:
			error = 'Invalid Credentials. Please try again.' #more complex error message?
		else:
			session['logged_in'] = True #session, another Flask object to familiarize with
			session['user_id'] = u.id
			flash("You are now logged in. Let's get Crazy!!")
			return redirect(url_for('tasks'))
	return render_template('login.html', form=LoginForm(request.form), error=error)

@app.route('/register/', methods=['GET', 'POST'])
def register():
	error = None 
	form = RegisterForm(request.form, csrf_enabled=False)
	if form.validate_on_submit():
		new_user = User(
					form.name.data,
					form.email.data,
					form.password.data,
					#Michael was missing a comma here
					)
		#this was throwing an error because when the page was loading this block was executing
		#I had it outside of the if block above
		try:
			db.session.add(new_user)
			db.session.commit()
			flash('Thanks for registering. Please login.')
			return redirect(url_for('login'))
		except IntegrityError:
			error = 'Oh no! That username and/or email already exist. Please try again.'
		else:
			flash_errors(form)
	return render_template('register.html', form=form, error=error)


@app.route("/logout")
def logout():
	session.pop('logged_in', None)
	session.pop('user_id', None)
#what was this on pg. 213 	flash('You are logged out. Bye. :(')
	flash('You were logged out')
	return redirect(url_for('login'))


#######		tasks pages	   #######
@app.route("/tasks/")
@login_required
def tasks():
	open_tasks = db.session.query(FTasks).filter_by(status='1').order_by(FTasks.due_date.asc())
	closed_tasks = db.session.query(FTasks).filter_by(status='0').order_by(FTasks.due_date.asc())
	return render_template('tasks.html', form=AddTask(request.form), open_tasks=open_tasks, closed_tasks=closed_tasks)


@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
	form = AddTask(request.form, csrf_enabled=False)
	if form.validate_on_submit():
		new_task = FTasks(
			form.name.data,
			form.amount.data,
			form.due_date.data,
			form.priority.data,
			form.posted_date.data,
			'1',
			session['user_id']
			)
		db.session.add(new_task)
		db.session.commit()
		flash('New entry was successfully posted. Thanks.')
	else:
		flash_errors(form)
	return redirect(url_for('tasks'))

#mark tasks as complete WATCH THE COMMA?
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	new_id = task_id
	db.session.query(FTasks).filter_by(task_id=new_id).update({"status":"0"})
	db.session.commit()
	flash('The task was marked as complete. Nice.')
	return redirect(url_for('tasks'))

#delete tasks WATCH THE COMMA?
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	new_id = task_id
	db.session.query(FTasks).filter_by(task_id=new_id).delete()
	db.session.commit()
	flash('The task was deleted.')
	return redirect(url_for('tasks'))

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

@app.errorhandler(404)
def internal_error(error):
	return render_template('404.html'), 404