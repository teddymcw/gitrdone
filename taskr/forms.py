#from flask.ext.wtf import Form, TextField, DateField, IntegerField, SelectField, Required
#note: import practices and namespaces changed in WTForms 9.0
#using WTF-0.9.3

from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, SelectField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(Form):
	name = TextField('Username', validators=[DataRequired(), Length(min=4, max=25)])
	email = TextField('Email', validators=[DataRequired(), Length(min=6, max=40)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
	#check the upper or lowercase on the 'Password' below, at very end!
	confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

class LoginForm(Form):
	name = TextField('Username', validators=[DataRequired()])
	#check the upper or lowercase on the 'Password' below
	password = PasswordField('password', validators=[DataRequired()])


class AddTask(Form):
	task_id = IntegerField('Priority')
	name = TextField('Item name', validators=[DataRequired()])
	amount = IntegerField('Amount', validators=[DataRequired()])
	due_date = DateField('Date Due (mm/dd/yyyy)', validators=[DataRequired()], format='%m/%d/%Y')
	posted_date = DateField('Posted Date (mm/dd/yyyy)', validators=[DataRequired()], format='%m/%d/%Y')
	priority = SelectField('Priority', validators=[DataRequired()], choices=[('1', '1'),
																		('2', '2'),
																		('3', '3'),
																		('4', '4'),
																		('5', '5')
																		])
	status = IntegerField('Status')

