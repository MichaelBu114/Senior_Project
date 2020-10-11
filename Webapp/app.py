from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
import re
app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'snowflake6365stark'
app.config['MYSQL_DATABASE_DB'] = 'dp_sp'

mysql = MySQL()
mysql.init_app(app)

@app.route('/pagelogin/', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'] 
        password = request.form['password']
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM Login WHERE username = %s AND password = %s', (username,password,))
        login = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = login['login_id']
            session['username'] = login['username']
            return 'Login successful'
        else:
            msg = 'Incorrect username/password'
    return render_template('', msg='')

@app.route('/pagelogin/logout')
def logout():
    session.pop('loggedin', None)
    seesion.pop('id', None)
    seesion.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
