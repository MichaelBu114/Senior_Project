from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
import hashlib
import re

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'snowflake6365stark'
app.config['MYSQL_DATABASE_DB'] = 'dp_sp'
mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pagelogin/', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'] 
        password = hashlib.md5(request.form['password'])
        cursor = mysql.connect().cursor()
        cursor.callproc('GetLogin', [username,password])
        login = cursor.fetchone()
        if login:
            session['loggedin'] = True
            session['id'] = login['login_id']
            session['username'] = login['username']
            return 'Login successful'
        else:
            msg = 'Incorrect username/password'
    return render_template('login_test.html', msg='')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/newAccount/', methods = ['GET', 'POST'])
def newAccount():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'firstName' in request.form and 'lastName' in request.form:
        username = request.form['username'] 
        password = hashlib.md5(request.form['password'])
        email = request.form['emai']
        firstname = request.form['firstName']
        lastname = request.form['lastName'] 
        cursor = mysql.connect().cursor()
        cursor.callproc('GetUsername', ['username']) 
        login = cursor.fetchone()
        if login: 
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password: 
            msg = 'Please fill out the form!'
        else: 
            cursor.callproc('newUser', [username, password, email, firstname, lastname]) 
            mysql.connection.commit() 
            msg = 'You have successfully registered!'
    elif request.method == 'POST': 
        msg = 'Please fill out the form!'
    return render_template('index.html', msg = msg)


app.run(host='0.0.0.0', debug = True)