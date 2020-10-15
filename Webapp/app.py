from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
import hashlib
import re

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'snowflake6365stark'
app.config['MYSQL_DATABASE_DB'] = 'dp_sp'
mysql.init_app(app)

@app.route('/')
@app.route('/pagelogin/', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'] 
        password = hashlib.md5(request.form['password'])
        cursor = mysql.connect().cursor()
        cursor.execute('SELECT * FROM Login WHERE username = %s AND password = %s', (username,password,))
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

@app.route('/newAccount', methods = ['GET', 'POST'])
def newAccount():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'] 
        password = hashlib.md5(request.form['password']) 
        cursor = mysql.connect().cursor()
        cursor.execute('SELECT * FROM login WHERE username = % s', (username, )) 
        account = cursor.fetchone() 
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password: 
            msg = 'Please fill out the form !'
        else: 
            cursor.execute('INSERT INTO login VALUES (NULL, % s, % s)', (username, password, )) 
            mysql.connection.commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('', msg = msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
