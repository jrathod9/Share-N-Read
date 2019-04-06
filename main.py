from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
from forms import RegistrationForm, LoginForm, BookForm 
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
@app.route('/requests',methods=['GET','POST'])
def requests():
	con = sqlite3.connect("Database/db.sqlite3")
	con.row_factory=sqlite3.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM currentsession")
	sessionuser = cur.fetchall()
	# print(sessionuser["username"])
	cur.execute("SELECT * FROM requests WHERE owner = ?",[sessionuser["username"]])
	requestlist = cur.fetchall()
	return render_template('requests.html',requestlist = requestlist);

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		form = LoginForm()
		con = sqlite3.connect("Database/db.sqlite3")
		con.row_factory=sqlite3.Row
		cur = con.cursor()
		cur.execute("SELECT * FROM users WHERE username=? and password=?",[form.username.data,form.password.data])
		pas = cur.fetchall()
		cur.execute("SELECT * FROM books WHERE username=?",[form.username.data])
		books = cur.fetchall()
		mylist = [form.username.data,books]
		# for ele in pas:
		# 	print(ele)
		if form.username.data == "admin" and form.password.data == "password":
			flash("Hi Admin!",'success')
			return redirect(url_for('list'))
		elif pas is not None:
			cur.execute("INSERT INTO currentsession VALUES(?)",[mylist[0]])
			con.commit()
			for ele in pas:
				sessionuser = ele["username"]
				print(sessionuser)
			return render_template('profile.html',mylist = mylist)
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
@app.route("/addbook",methods=['GET','POST'])
def addbook():
	form = BookForm()
	name = str(form.name.data)
	author = str(form.author.data)
	ISBN = form.ISBN.data
	genre = str(form.genre.data)
	if request.method == "POST":
		con = sqlite3.connect("Database/db.sqlite3")
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute("SELECT * FROM currentsession")
		tempvar = cur.fetchone()
		username = tempvar["username"]
		cur.execute("INSERT INTO books VALUES(?,?,?,?,?,?,?)",[username,name,author,ISBN,"live","",genre])
		cur.commit()
		cur.execute("SELECT * FROM users WHERE username=? and password=?",[form.username.data,form.password.data])
		pas = cur.fetchall()
		cur.execute("SELECT * FROM books WHERE username=?",[form.username.data])
		books = cur.fetchall()
		mylist = [form.username.data,books]
		flash("Book Added",'success')
	return render_template('addbook.html',form=form)	
@app.route("/list")
def list():
	print(sessionuser)
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
	con = sqlite3.connect("Database/db.sqlite3")
	con.row_factory=sqlite3.Row
	cur = con.cursor()
	cur.execute("DELETE FROM currentsession")
	con.commit()
	sessionuser = ''
	session['logged_in'] = False
	return home()

@app.route("/search")
def search():
	
	query = str(form.search.data)
	con = sqlite3.connect("Database/db.sqlite3")
	cur = con.cursor()
	cur.execute("SELECT * FROM books WHERE name=?",[query])
	results = cur.fetchall()
	return render_template('search.html',results = results,form = form)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
