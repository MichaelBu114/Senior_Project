import hashlib
import re
import gc
from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
from flask.helpers import flash

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'snowflake6365stark'
app.config['MYSQL_DB'] = 'dp_sp'
mysql.init_app(app)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    error = ''
    try:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.get_db().cursor()
            login = cursor.callproc('GetLogin', [request.form('username'), request.form('password')])
            login = cursor.fetchone()
            if login:
                session['logged_in'] = True
                session['username'] = request.form('username')
                flash('Login successful')
                return redirect(url_for('home'))
            else:
                error = "Invalid username/password, try again."
        gc.collect()
        return render_template('login_test/html', error = error)
    except Exception as e:
        error = 'Invalid username/password, try again.'
        return render_template('login_test.html', error = error)

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
        cursor = mysql.get_db().cursor()
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)