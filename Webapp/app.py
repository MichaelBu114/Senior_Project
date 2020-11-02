import hashlib
import re
import secrets
from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
from flask.helpers import flash
import zomato_api

app = Flask(__name__)
mysql = MySQL()
app.secret_key = secrets.token_urlsafe(16)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'snowflake6365stark'
app.config['MYSQL_DATABASE_DB'] = 'dp_sp'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        con = mysql.connect()
        cur = con.cursor()
        login = cur.callproc('GetLogin', [username,hashed])
        login = cur.fetchone()
        if login:
            session['username'] = username
            user = session['username']
            return render_template('index_login.html', username=user)
        else:
            error = "Invalid username/password, try again."
    return render_template('login.html', error = error)

@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/registration/', methods = ['GET', 'POST'])
def registration():
    msg = ''
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form and 'firstname' in request.form and 'lastname' in request.form:
        password = request.form['password']
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        con = mysql.connect()
        cur = con.cursor()
        login = cur.callproc('GetUsername', [email]) 
        login = cur.fetchone()
        if login: 
            msg = 'Account already exists!'
        else:
            sqlstat = "INSERT INTO Login (username,password,date_changed) VALUES (%s,%s,curdate())"
            sqlstat2 = "call addUser(%s,%s,%s,LAST_INSERT_ID())"
            args2 = (firstname,lastname,email)
            args = (email, hashed)
            cur.execute(sqlstat, args)
            cur.execute(sqlstat2, args2)
            con.commit()
            return render_template('SurveyForm.html', msg = msg)
    elif request.method == 'POST': 
        msg = 'Please fill out the form!'
    return render_template('registration.html', msg = msg)

@app.route('/search/', methods = ['GET', 'POST'])
def search():
    msg = ""
    
    if request.method == 'POST':
        if 'zip' in request.form and 'radius' in request.form:
            resp = zomato_api.search(request.form['zip'], request.form['radius'], "real_distance", "")
            msg += str(resp)
        else:
            msg += "Invalid input"
    
    return render_template('search.html', msg = msg)

@app.route('/survey/' , methods = ['GET','POST'])
def survey():
    if request.method =='POST':
        if 'zip' in request.form and 'radius' in request.form:
            resp = zomato_api.search(request.form['zip'], request.form['radius'], "real_distance", "")
            estab = request.form.getlist('EstCheckboxGroup')
            cat = request.form.getlist('CuisCheckboxGroup')
            cus = request.form.getlist('CatCheckboxGroup')
            return redirect(url_for('search'))
    return render_template('SurveyForm.html')


if __name__ == '__main__':
    app.run(debug = True)