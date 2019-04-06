from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=2, max=20)])
	email = StringField('Email',validators=[DataRequired(), Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	# confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=2, max=20)])
	# email = StringField('Email',validators=[DataRequired(), Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	# confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	# remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class BookForm(FlaskForm):
	name = StringField('Name',validators=[DataRequired(),Length(min=2, max=50)])
	author = StringField('Author',validators=[DataRequired(),Length(min=2, max=50)])
	ISBN = IntegerField('ISBN',validators=[DataRequired(),Length(13)])
	genre = StringField('Genre',validators=[DataRequired(),Length(min=2, max=50)])
	# email = StringField('Email',validators=[DataRequired(), Email()])
	# password = PasswordField('Password',validators=[DataRequired()])
	# confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Add Book')