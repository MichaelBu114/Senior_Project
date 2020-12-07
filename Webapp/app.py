import hashlib
import re
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flaskext.mysql import MySQL
from flask.helpers import flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import zomato_api

app = Flask(__name__)
mysql = MySQL()
app.config.from_pyfile('config.py')
mysql.init_app(app)
mail = Mail(app)
result = None
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        con = mysql.connect()
        cur = con.cursor()
        login = cur.callproc('GetLogin', [username, hashed])
        login = cur.fetchone()
        if login:
            name = cur.execute('Call GetName(%s)', (username))
            name = cur.fetchone()
            sesId = cur.execute('Call GetUserId(%s, %s)', (name[0], username))
            sesId = cur.fetchone()
            session['username'] = name[0]
            session['email'] = username
            session['password'] = password
            session['id'] = sesId[0]
            con.close()
            return redirect(url_for('home'))
        else:
            msg = "Login: Invalid username/password, try again."
            flash(msg)
            con.close()
    return redirect(url_for('home'))


@app.route('/logout/')
def logout():
    global result
    session.pop('username', None)
    session.pop('email', None)
    session.pop('id', None)
    session.pop('password', None)
    result = {}
    return redirect(url_for('home'))


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        if 'psw' in request.form and 'email' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'psw-repeat' in request.form:
            password = request.form['psw']
            hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
            hRepeat = hashlib.sha256(request.form['psw-repeat'].encode('utf-8')).hexdigest()
            email = request.form['email']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            con = mysql.connect()
            cur = con.cursor()
            login = cur.callproc('GetUsername', [email])
            login = cur.fetchone()
            if login:
                flash('Register: Account already exists!')
            elif hashed != hRepeat:
                flash('Register: Passwords do not match')
            else:
                sqlstat = "Call newUser(%s,%s,%s,%s)"
                args = (hashed,firstname, lastname, email)
                cur.execute(sqlstat, args)
                con.commit()
                name = cur.execute('Call GetName(%s)', (email))
                name = cur.fetchone()
                sesId = cur.execute('Call GetUserId(%s, %s)', (name[0], email))
                sesId = cur.fetchone()
                session['username'] = name[0]
                session['email'] = email
                session['password'] = password
                session['id'] = sesId[0]
                token = generate_confirmation_token(email)
                confirm_url = url_for('confirm_email', token=token, _external=True)
                regestrationMessage(email, confirm_url)
                con.close()
                return render_template('preferences.html', username=session['username'])
        else:
            flash('Please fill out the form!')
    return redirect(url_for('home'))

@app.route('/search_results/<int:pageNum>/<int:Next>/<int:prev>')
def search_results(pageNum,Next,prev):
    if 'username' in session:
        sesid = session['id']
    else:
        sesid = 0
    data = result.get(sesid)
    return render_template('search.html',username = session['username'],data = data, pageNum= pageNum, next=Next,prev=prev)

@app.route('/search/', methods=['GET', 'POST'])
def search():
    global result
    msg = ""
    data = []
    pageNum = 0
    if 'username' in session:
        sesId = session['id']
        uname = session['username']
    else:
        sesId = 0
    if request.method == 'POST':
        if 'zip' in request.form and 'radius' in request.form:
            pageNum = 1
            UserZipCode = request.form['zip']
            UserDistance = request.form['radius']
            UserRating = int(request.form['rating'])
            UserRange = int(request.form['cost'])
            # if 'username' in session:
            #     sesId = session['id']
            # else:
            #     sesId = 0
            resp = zomato_api.search(UserZipCode, UserDistance, "real_distance", sesId)
            if resp["status"] != 'OK':
                msg += resp["status"]
            for i in range(int(resp["count"])):
                data.append([resp[i]["name"], resp[i]["id"], resp[i]["address"], resp[i]["phone_number"],
                             resp[i]["aggregate_rating"], resp[i]["menu_url"], resp[i]["featured_image"],
                             resp[i]["rating_icon"]])
            result = {sesId:data}
            return render_template('search.html', msg=msg, data=data, username=uname,
                                   userZipcode=UserZipCode, userDistance=UserDistance,
                                   userRating=UserRating, userRange=UserRange,pageNum = pageNum, next = 11, prev=0)
    else:
        return render_template('search.html', msg=msg, data=data, username=uname,pageNum = pageNum, next = 0, prev= 0)


@app.route('/details/', methods=['GET', 'POST'])
def details():
    msg = ""
    mapapikey = "ed2bc3219ed1439cb0502f05dc7a881b"
    res_id = request.args.get('res_id')
    resp = zomato_api.restaurant_details(res_id)
    estList = str(resp["establishment"]).lstrip("[").rstrip("]").replace("'", "")
    highlightsList = str(resp["highlights"]).lstrip("[").rstrip("]").replace("'", "")
    con = mysql.connect()
    cur = con.cursor()
    commentsList = cur.callproc('getComments', [res_id])
    commentsList = cur.fetchall()
    if not commentsList:
        commentsList = 'empty'
    if resp["status"] != 'OK':
        msg += resp["status"]
    if 'username' in session:
        username = session['username']
    else:
        username = ''

    return render_template('details.html', msg=msg, restaurantID=resp["id"], name=resp['name'], address=resp['address'],
                           city=resp["city"], phone_numbers=resp["phone_numbers"],
                           latitude=resp["latitude"], longitude=resp["longitude"],
                           locality_verbose=resp["locality_verbose"],
                           cuisines=resp["cuisines"], timings=resp["timings"],
                           average_cost_for_two=resp["average_cost_for_two"],
                           price_range=resp["price_range"], currency=resp["currency"], highlights=highlightsList,
                           aggregate_rating=resp["aggregate_rating"], rating_text=resp["rating_text"],
                           menu_url=resp["menu_url"],
                           featured_image=resp["featured_image"], has_online_delivery=resp["has_online_delivery"],
                           is_delivering_now=resp["is_delivering_now"],
                           is_table_reservation_supported=resp["is_table_reservation_supported"],
                           has_table_booking=resp["has_table_booking"], establishment=estList, username=username,
                           mapimageapikey=mapapikey, commentsList=commentsList)


@app.route('/comment/', methods=['GET', 'POST'])
def comment():
    if request.method == 'POST' and 'username' in session:
        print('Posted:')
        rating = request.form['star']
        commentTitle = request.form['title']
        commentVal = request.form['comment']
        restID = request.form["restaurantID"]
        print('Rating: ' + str(rating) + ' - Comment: ' + commentVal + ' - restID: ' + str(restID))
        con = mysql.connect()
        cur = con.cursor()
        cur.execute('CALL addComment(%s,%s,%s,%s,%s)',
                    (session["id"], int(rating), commentTitle, commentVal, int(restID)))
        con.commit()
        flash(restID)
        con.close()

    return redirect(url_for('details', res_id=restID))


@app.route('/survey/', methods=['GET', 'POST'])
def survey():
    msg = ""
    data = []
    if 'username' in session:
        con = mysql.connect()
        cur = con.cursor()
        sesId = session['id']
        pref = cur.execute('CALL getPreferences(%s)', (sesId))
        pref = cur.fetchone()
        cur.execute('Call getUserEstablishments(%s)', (sesId))
        estList = [val for sublist in cur.fetchall() for val in sublist]
        cur.execute('Call getUserCuisines(%s)', (sesId))
        cuisineList = [val for sublist in cur.fetchall() for val in sublist]
        cur.execute('Call getUserCategories(%s)', (sesId))
        categoryList = [val for sublist in cur.fetchall() for val in sublist]
        if request.method == 'POST':
            if 'zip' in request.form and 'radius' in request.form:
                UserZipCode = request.form['zip']
                UserDistance = request.form['radius']
                UserRating = request.form['rating']
                UserRange = request.form['cost']
                estab = request.form.getlist('EstCheckboxGroup')
                estab = [int(i) for i in estab]
                estab.sort()
                cus = request.form.getlist('CuisCheckboxGroup')
                cus = [int(i) for i in cus]
                cus.sort()
                cat = request.form.getlist('CatCheckboxGroup')
                cat = [int(i) for i in cat]
                cat.sort()
                newPref = updateUserPref(pref, sesId, UserZipCode, int(UserDistance), int(UserRating), int(UserRange))
                updateUserList(estList, estab, sesId, 'Call addUserEstablishment(%s,%s)',
                               'CALL deleteUserEstablishment(%s,%s)')
                updateUserList(cuisineList, cus, sesId, 'Call addUserCuisine(%s,%s)', 'Call deleteUserCuisine (%s,%s)')
                updateUserList(categoryList, cat, sesId, 'Call addUserCategories(%s,%s)',
                               'Call deleteUserCategories(%s,%s)')
                resp = zomato_api.search(UserZipCode, UserDistance, "real_distance", sesId, 0, 0, 0)
                msg += str(resp["status"])
                for i in range(int(resp["count"])):
                    data.append([resp[i]["name"], resp[i]["id"], resp[i]["address"], resp[i]["phone_number"],
                                 resp[i]["aggregate_rating"], resp[i]["menu_url"], resp[i]["featured_image"],
                                 resp[i]["rating_icon"]])
                return render_template('search.html', msg=msg, data=data, username=session['username'],
                                       userRange=newPref[3],
                                       userDistance=round(newPref[1] / 1609), userZipcode=newPref[0],
                                       userRating=newPref[2],pageNum = 1,next=0,prev=0)
        else:
            return render_template('preferences.html', msg=msg, data=data, username=session['username'],
                                   userRange=pref[3],
                                   userDistance=pref[1], userZipcode=str(pref[0]), userRating=pref[2],
                                   estList=estList, cuisineList=cuisineList, categoryList=categoryList)
    else:
        if request.method == 'POST':
            if 'zip' in request.form and 'radius' in request.form:
                UserZipCode = request.form['zip']
                UserDistance = int(request.form['radius'])
                UserRating = int(request.form['rating'])
                UserRange = int(request.form['cost'])
                estab = request.form.getlist('EstCheckboxGroup')
                estab = [int(i) for i in estab]
                estab.sort()
                cus = request.form.getlist('CuisCheckboxGroup')
                cus = [int(i) for i in cus]
                cus.sort()
                cat = request.form.getlist('CatCheckboxGroup')
                cat = [int(i) for i in cat]
                cat.sort()
                resp = zomato_api.search(UserZipCode, UserDistance, "real_distance", 0, cat, cus, estab)
                msg += str(resp["status"])
                for i in range(int(resp["count"])):
                    data.append([resp[i]["name"], resp[i]["id"], resp[i]["address"], resp[i]["phone_number"],
                                 resp[i]["aggregate_rating"], resp[i]["menu_url"], resp[i]["featured_image"],
                                 resp[i]["rating_icon"]])
                return render_template('search.html', msg=msg, data=data, userRange=UserRange,
                                       userDistance=round(UserDistance / 1609),
                                       userZipcode=UserZipCode, userRating=UserRating,pageNum = 1,next =0,prev=0)
        return render_template('preferences.html', msg=msg)


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    msg = ''
    if request.method == 'POST':
        if request.form['button'] == 'Save Changes':
            #if 'email' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'pwd' in request.form and 'pwd-rpt' in request.form:
            if 'email' in request.form and 'firstname' in request.form and 'lastname' in request.form:
                if request.form['email'] != '' or request.form['firstname'] != '' or request.form['lastname'] != '':
                    con = mysql.connect()
                    cur = con.cursor()
                    hashed = ''
                    rptHashed = ''
                    #hashed = hashlib.sha256(session['pwd'].encode('utf-8')).hexdigest()
                    #rptHashed = hashlib.sha256(session['pwd-rpt'].encode('utf-8')).hexdigest()

                    if hashed != rptHashed:
                        msg = 'Password do not match'
                    else:
                        sesId = session['id']
                        email = request.form['email']
                        fname = request.form['firstname']
                        lname = request.form['lastname']
                        args = (sesId, email, hashed, fname, lname)
                        cur.execute('CALL updateProfile(%s,%s,%s,%s,%s)', args)
                        updated = cur.execute('CALL getProfile(%s)', sesId)
                        updated = cur.fetchone()
                        fname = updated[0]
                        lname = updated[1]
                        email = updated[2]
                        con.commit()
                        session['username'] = (fname + " " + lname)
                        con.close()
                        return render_template('profile.html', username=session['username'], msg=msg,
                                               password=hashed, email=email, firstname=fname, lastname=lname)
                else:
                    msg = 'You must fill in at least one entry to Save your Changes.'
                    return render_template('profile.html', username=session['username'],
                           msg=msg, password=session['password'], email=session['email'],
                           firstname=session['username'].split()[0], lastname=session['username'].split()[-1])
        elif request.form['button'] == 'Logout':
            return redirect(url_for('logout'))
        elif request.form['button'] == 'Modify Preferences':
            return redirect(url_for('survey'))
    return render_template('profile.html', username=session['username'],
                           msg=msg, password=session['password'], email=session['email'],
                           firstname=session['username'].split()[0], lastname=session['username'].split()[-1])


# Updates the user preference if it was changeded on the survey page
def updateUserPref(pref, uId, UserZip, UserDis, UserRate, UserRange):
    con = mysql.connect()
    cur = con.cursor()
    if UserZip != str(pref[0]):
        cur.execute('CALL updateZipcode(%s,%s)', (int(UserZip), uId))
        con.commit()
        newZip = UserZip
    else:
        newZip = str(pref[0])
    if UserDis != pref[1]:
        cur.execute('CALL updateDistance(%s,%s)', (UserDis, uId))
        con.commit()
        newDis = UserDis
    else:
        newDis = pref[1]
    if UserRate != pref[3]:
        cur.execute('CALL updateRange(%s,%s)', (UserRate, uId))
        con.commit()
        newRate = UserRate
    else:
        newRate = pref[3]
    if UserRange != pref[2]:
        cur.execute('CALL updateRating(%s,%s)', (UserRange, uId))
        con.commit()
        newRange = UserRange
    else:
        newRange = pref[2]
    con.commit()
    con.close()
    return [newZip, newDis, newRate, newRange]


def updateUserList(userList, userCheckBox, uId, addFunction, deleteFunction):
    con = mysql.connect()
    cur = con.cursor()
    if userList != userCheckBox:
        for i in userList:
            if i in userCheckBox:
                userCheckBox.remove(i)
            elif i not in userCheckBox:
                args = (uId, i)
                cur.execute(deleteFunction, args)
            con.commit()
        if userCheckBox:
            for i in userCheckBox:
                args = (uId, i)
                cur.execute(addFunction, args)
            con.commit()
    con.close()

@app.route('/howitworks/', methods=['GET', 'POST'])
def howitworks():
    return render_template('howitworks.html')


@app.route('/termspolicy/', methods=['GET', 'POST'])
def termspolicy():
    return render_template('termspolicy.html')

@app.route('/facebooklink/', methods=['GET', 'POST'])
def facebooklink():
    return render_template('facebooklink.html')

@app.route('/instagramlink/', methods=['GET', 'POST'])
def instagramlink():
    return render_template('instagramlink.html')

@app.route('/twitterlink/', methods=['GET', 'POST'])
def twitterlink():
    return render_template('twitterlink.html')

@app.route('/connect/', methods=['GET', 'POST'])
def connect():
    msg = ''
    confirmed = []
    pending = []
    declined = []
    sesId = session['id']
    if request.method == 'POST':
        if request.form['findFriend'] == 'Submit' and 'friends' in request.form:
            friend = request.form['friends']
            con = mysql.connect()
            cur = con.cursor()
            name = cur.execute('Call GetName(%s)', (friend))
            name = cur.fetchone()
            if name == None:
                msg = ('No Results Found for ' + '"' + friend + '"')
                flash(msg)
            elif friend == session['email']:
                msg = ('Invalid')
                flash(msg)
            else:
                friendId = cur.execute('Call GetUserId(%s, %s)', (name[0], friend))
                friendId = cur.fetchone()
                addFriend(friendId[0], sesId)
                con.close
                msg = ('Friend request sent')
                flash(msg)
    friendsList = getFriends(sesId)
    for friend in friendsList:
        if friend[3] == 0:
            pending.append(friend)
        elif friend[3] == 1:
            confirmed.append(friend)
        else:
            declined.append(friend)
    return render_template('AddFriends.html', username=session['username'], data=confirmed, pending=pending, declined=declined)


# Need to determine if group calls go here or inside request.method.

def addFriend(friendId, userId):
    con = mysql.connect()
    cur = con.cursor()
    status = 0
    if (status != 1 and friendId != userId):
        cur.execute('CALL addFriend(%s,%s,%s)', (userId, friendId,status))
        con.commit()
    con.close()


def getFriends(Fk_user):
    con = mysql.connect()
    cur = con.cursor()
    friendsList = cur.execute('CALL getFriends(%s)', (Fk_user))
    friendsList = cur.fetchall()
    con.commit()
    con.close()
    return friendsList


def deleteFriend(friends_id, Fk_user, status):
    con = mysql.connect()
    cur = con.cursor()
    if (status == 1 and friends_id != Fk_user):
        cur.execute('CALL deleteFriend(%s, %s)', (friends_id, Fk_user))
        con.commit()
    con.close()

@app.route('/update/<int:friends_id>/<int:Fk_user>/<int:status>', methods = ['GET','POST'])
def updateFriend(friends_id,Fk_user,status):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('CALL updateFriend(%s, %s, %s)', (friends_id, Fk_user, status))
    con.commit()
    con.close()
    return redirect(url_for('connect'))


def regestrationMessage(email, url):
    msg = Message('Confirmation Email', sender = mail.MAIL_USERNAME, recipients =[email])
    msg.body = "Please confirm your email " + url
    mail.send(msg)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token,expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token,salt=app.config['SECURITY_PASSWORD_SALT'] ,max_age=expiration)
    except:
        return False
    return email

def confirm_email(token):
    con = mysql.connect()
    cur = con.cursor()
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.')
        cur.execute("CALL updateUserActivity", (2,session['id']))
        con.commit()
    active = cur.execute("CALL getActivity(%s)", (email))
    active = cur.fetchall()
    if active[0] == 1:
        flash('Account is already confirmed.')
    else:
        cur.execute("CALL updateUserActivity", (1,session['id']))
        cur.commit()
        con.close()
        flash('Your email is confirmed, thank you')
    return redirect(url_for('home'))
    
if __name__ == '__main__':
    app.run(debug=True)
