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
def do_admin_login():
	if request.form['password'] == 'password' and request.form['username'] == 'admin':
		session['logged_in'] = True
	else:
		flash('wrong password!')
	return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
