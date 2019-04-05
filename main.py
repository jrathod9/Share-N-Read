from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
from forms import RegistrationForm, LoginForm
import os
import sqlite3
#SAMPLE DATABASE
con = sqlite3.connect('Database/db.sqlite3')
# print "Opened database successfully";

# conn.execute('CREATE TABLE users (username TEXT, email TEXT, password TEXT)')
# print "Table created successfully";
# conn.close() 

app = Flask(__name__)

@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return "Hello Boss!"

@app.route('/login', methods=['POST'])
def login():
# form = LoginForm()
	# if form.validate_on_submit():
	con = sqlite3.connect("Database/db.sqlite3")
	con.row_factory=sqlite3.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM users WHERE username=? and password=?",[request.form['username'],request.form['password']])
	pas = cur.fetchall()

	if request.form['username'] == "admin" and request.form['password'] == "password":
		flash("You have logged in!",'success')
		return redirect(url_for('list'))
	elif pas is not None:
		print(pas)
		return render_template('profile.html',pas = pas)
	else:
		flash("Check email or password!",'danger')
	return render_template('login.html')
	# title='Login',form=form


# def do_admin_login():
# 	if request.form['password'] == 'password' and request.form['username'] == 'admin':
# 		session['logged_in'] = True
# 	else:
# 		flash('wrong password!')
# 	return home()
@app.route("/list")
def list():
	con = sqlite3.connect("Database/db.sqlite3")
	con.row_factory=sqlite3.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM users")
	rows = cur.fetchall()
	return render_template('list.html',rows = rows)

# @app.route("/register")
# def register():
# 	usernm = str(form.request["username"])
# 	emailid = str(form.email.data)
# 	passwrd = str(form.password.data)
# 		# usernm.encode('ascii')
# 		# emailid.encode('ascii')
# 		# passwrd.encode('ascii')
# 	mylist = [usernm,emailid,passwrd]
# 	print(mylist)
# 	if request.method == "POST":
# 		con = sqlite3.connect("Databases/db.sqlite3")
# 		con.row_factory = sqlite3.Row
# 		cur = con.cursor()
# 		cur.execute("INSERT INTO users VALUES(?,?,?)",[usernm,emailid,passwrd])
# 		con.commit()
# 		print(cur.fetchall())
# 	flash("Welcome " + usernm + "!",'success')
# 	return redirect(url_for('home'))
# return render_template('register.html',title='Register',form=form)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
