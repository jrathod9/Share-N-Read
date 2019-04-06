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

sessionuser = ''

@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return "Hello Boss!"

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		form = LoginForm()
		con = sqlite3.connect("Database/db.sqlite3")
		con.row_factory=sqlite3.Row
		cur = con.cursor()
		cur.execute("SELECT * FROM users WHERE username=? and password=?",[form.username.data,form.password.data])
		pas = cur.fetchall()
		if form.username.data == "admin" and form.password.data == "password":
			flash("Hi Admin!",'success')
			return redirect(url_for('list'))
		elif pas is not None:
			for ele in pas:
				sessionuser = ele["username"]
				print(sessionuser)
			return render_template('profile.html',pas = pas)
		else:
			flash("Check email or password!",'danger')
			return render_template('login.html')
		return render_template('login.html',title='Login',form=form)
	else:
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

@app.route("/register",methods = ['GET','POST'])
def register():
	form = RegistrationForm()
	sessionuser = ''
	usernm = str(form.username.data)
	emailid = str(form.email.data)
	passwrd = str(form.password.data)
		# usernm.encode('ascii')
		# emailid.encode('ascii')
		# passwrd.encode('ascii')
	mylist = [usernm,emailid,passwrd]
	print(mylist)
	if request.method == "POST":
		con = sqlite3.connect("Database/db.sqlite3")
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?)",[usernm,emailid,passwrd,"","","",""])
		con.commit()
		print(cur.fetchall())	
		flash("Welcome " + usernm + "! Please Login.",'success')
		return render_template('login.html')
	return render_template('register.html',title='Register',form=form)

	# usernm = str(request.form["username"])
	# emailid = str(request.form["email"])
	# passwrd = str(request.form["password"])
		# usernm.encode('ascii')
		# emailid.encode('ascii')
		# passwrd.encode('ascii')
	# mylist = [usernm,emailid,passwrd]
	# print(mylist)
	# if request.method == "POST":
	# 	con = sqlite3.connect("Database/db.sqlite3")
	# 	con.row_factory = sqlite3.Row
	# 	cur = con.cursor()
	# 	cur.execute("INSERT INTO users VALUES(?,?,?)",[usernm,emailid,passwrd])
	# 	con.commit()
	# 	print(cur.fetchall())
	# 	flash("Welcome " + usernm + "!",'success')
	# 	return redirect(url_for('home'))
	# return render_template('register.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    sessionuser = ''
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
