import hashlib
import re
import secrets
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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
    if 'username' in session:
        return render_template('index.html', username = session['username'])
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
            name = cur.execute('Call GetName(%s)', (username))
            name = cur.fetchone()
            session['username'] = name[0]
            session['email'] = username
            return redirect(url_for('home'))
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
            name = cur.execute('Call GetName(%s)', (email))
            name = cur.fetchone()
            session['username'] = name[0]
            session['email'] = email
            return render_template('SurveyForm.html', msg = msg, username = session['username'])
    elif request.method == 'POST': 
        msg = 'Please fill out the form!'
    return render_template('registration.html', msg = msg)

@app.route('/search/', methods = ['GET', 'POST'])
def search():
    msg = ""
    data = []
    
    if request.method == 'POST':
        if 'zip' in request.form and 'radius' in request.form:
            resp = zomato_api.search(request.form['zip'], request.form['radius'], "real_distance", request.form['user_id'])
            msg += str(resp["status"])
            for i in range(int(resp["count"])):
                data.append([resp[i]["name"], resp[i]["url"], resp[i]["address"] + " - " + resp[i]["phone_number"]])
        else:
            msg += "Invalid input"
    if 'username' in session:
        return render_template('search.html', msg = msg, username= session['username'])
    return render_template('search.html', msg = msg, data = data)

@app.route('/survey/' , methods = ['GET','POST'])
def survey():
    msg =""
    data = []
    if request.method =='POST':
        if 'zip' in request.form and 'radius' in request.form:
            resp = zomato_api.search(request.form['zip'], request.form['radius'], "real_distance", "")
            msg += str(resp["status"])
            estab = request.form.getlist('EstCheckboxGroup')
            cus = request.form.getlist('CuisCheckboxGroup')
            cat = request.form.getlist('CatCheckboxGroup')
            con = mysql.connect()
            cur = con.cursor()
            fullname = session['username']
            email = session['email']
            name = cur.execute('Call GetUserId(%s, %s)', (fullname, email))
            name = cur.fetchone()
            for i in range(0, len(estab)):
                args = (name[0], int(estab[i]))
                sqlstat = 'Call addUserEstablishment(%s, %s)'
                cur.execute(sqlstat, args)
            con.commit()
            for i in range(0, len(cat)):
                args = (name[0], int(cat[i]))
                sqlstat = 'Call addUserCategories(%s, %s)'
                cur.execute(sqlstat, args)
            con.commit()
            for i in range(0, len(cus)):
                args = (name[0], int(cus[i]))
                sqlstat = 'Call addUserCuisine(%s, %s)'
                cur.execute(sqlstat, args)
            con.commit()
            for i in range(int(resp["count"])):
                data.append([resp[i]["name"], resp[i]["url"], resp[i]["address"] + " - " + resp[i]["phone_number"]])
            return render_template('search.html', msg = msg, data = data)
    if 'username' in session:
        return render_template('SurveyForm.html', msg = msg, username= session['username'])
    return render_template('SurveyForm.html', msg = msg)


if __name__ == '__main__':
    app.run(debug = True)