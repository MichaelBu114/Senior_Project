import hashlib
import re
from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
from flask.helpers import flash


app = Flask(__name__)
app.secret_key = 'SeniorProject'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'snowflake6365stark'
app.config['MYSQL_DATABASE_DB'] = 'dp_sp'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql = MySQL()
mysql.init_app(app)



@app.route('/')
def home():
    if 'login' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        db = mysql.connect()
        cursor = db.cursor()
        login = cursor.callproc('GetLogin', [username, password])
        login = cursor.fetchone()
        if login:
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful')
            return redirect(url_for('home'))
        else:
            error = "Invalid username/password, try again."
    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/registration/', methods = ['GET', 'POST'])
def registration():
    msg = ''
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form and 'firstname' in request.form and 'lastname' in request.form:
        password = request.form['password']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        db = mysql.connect() 
        cursor = db.cursor()
        cursor.callproc('GetUsername', [email]) 
        login = cursor.fetchone()
        if login: 
            msg = 'Account already exists!'
        elif not email or not password: 
            msg = 'Please fill out the form!'
        else: 
            cursor.callproc('newUser', [password, email, firstname, lastname])
            return render_template('survey.html')
    elif request.method == 'POST': 
        msg = 'Please fill out the form!'
    return render_template('registration.html', msg = msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug = True)