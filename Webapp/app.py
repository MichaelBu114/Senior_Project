import hashlib
import re
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flaskext.mysql import MySQL
from flask.helpers import flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import random
import zomato_api
from config import MAIL_USERNAME, MAPAPIKEY

"""
Configues app
MySQl and the email are configured from the config.py file
and results is initlized to an empty dictionary 
"""
app = Flask(__name__)
mysql = MySQL()
app.config.from_pyfile('config.py')
mysql.init_app(app)
mail = Mail(app)
result = {}

"""
The home page of the app with a check to see if the users 'username' is in session
if in session, renders the page with the username variable equal to the persons 'username'
else renders the page with no parameters
"""
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')

"""
Checks to see if the request method is post and if the person filled out the username and password fields
if true, takes the values in the username and password field, hashes the password, and calls a mysql procedure to see if
that persons loging exist in the database
if it does, then if gets the persons name, email, and id and stores them as session variables along with their password, aftewards
sending the user back the home page
else is displays error message saying one of the two is invalid and sending the user back the home page.   
"""
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

"""
Removes all the users session values and if the user has results removes the user results from the list
"""
@app.route('/logout/')
def logout():
    global result
    session.pop('username', None)
    session.pop('email', None)
    session.pop('id', None)
    session.pop('password', None)
    if len(result) != 0:
        result.popitem()
    return redirect(url_for('home'))

"""
Checks to see if the person creating a new account has their email, fullname, password, and repeated password in the request form
if true, gets the passwords hashes them and then gets the email, firstname, and lastname values
Checks to see if the username is in the database and if the passwords that were hashed match
if either one are true displays the correspoding error message and returns the user back the home page
else adds the person and their loging info into the database, stores the seession values, and sends a confirmation email with a secure token
lastly it sends the new user to the prefereces page
"""
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

"""
Gets the results for the user and filtering the results depending on what page the user is on
"""
@app.route('/search_results/<int:pageNum>/<int:Next>/<int:prev>/<int:rand>')
def search_results(pageNum,Next,prev,rand):
    if 'username' in session:
        sesId = session['id']
        data = result.get(sesId)
        return render_template('search.html', username=session['username'], data=data, pageNum=pageNum, next=Next, prev=prev,random=rand)
    else:
        data = result.get(0)
        return render_template('search.html', data=data, pageNum=pageNum, next=Next, prev=prev,random=rand)
   
"""
Uses zip code, radius, price range, and rating that the user provides to do an api call that gets up to 100 results
the resutls are append into a list of lists, sorted by highest rating, and then mapped to the users id or 0 if they are not logged in
lastly returns the render of page with all the data provided  
If a page is redirct to the search there is a check to see if the key-value pair is true
results returns None if key-value pair does not exists
"""
@app.route('/search/', methods=['GET', 'POST'])
def search():
    global result
    msg = ""
    data = []
    pageNum = 0
    qd = 0
    if 'username' in session:
        sesId = session['id']
        uname = session['username']
    else:
        sesId = 0
        uname = ''
    if request.method == 'POST':
        if 'zip' in request.form and 'radius' in request.form:
            pageNum = 1
            UserZipCode = request.form['zip']
            UserDistance = request.form['radius']
            UserRating = int(request.form['rating'])
            UserRange = int(request.form['cost'])
            rangePair = getRange(UserRange)
            resp = zomato_api.search(UserZipCode, UserDistance, "real_distance", sesId, UserRating, rangePair)
            
            msg = zomato_api.get_msg(resp)
            
            for i in range(int(resp["count"])):
                data.append([resp[i]["name"], resp[i]["id"], resp[i]["address"], resp[i]["phone_number"],
                         resp[i]["aggregate_rating"], resp[i]["menu_url"], resp[i]["featured_image"],
                         resp[i]["rating_icon"]])
            data.sort(reverse = True,key = lambda x: float(x[4]))
            if len(data) == 0:
                session['random'] = 0
                msg = "No results found"
            else:
                session['random'] = resp['random']['id']

            if result == {}:
                result = {sesId: data}
            else:
                result.popitem()
                result[sesId] = data
            return render_template('search.html', msg=msg, data=data, username=uname,
                                   userZipcode=UserZipCode, userDistance=UserDistance,
                                   userRating=UserRating, userRange=UserRange, pageNum=pageNum, next=10, prev=0, random=session['random'],qd=qd)
    else:
        if result.get(sesId) == None:
            return render_template('search.html', msg=msg, data = data, username=uname, pageNum=pageNum, next=0, prev=0,random =0)
        elif result.get(sesId):
            return render_template('search.html', msg=msg, data = result.get(sesId), username=uname, pageNum=1, next=10, prev=0, random = session['random'])
        else:
            return render_template('search.html', msg=msg, data = data, username=uname, pageNum=pageNum, next=0, prev=0,random=0)

"""
Does a quick search using the prefrences that the users has provideded through there survey
"""
@app.route('/quicksearch/', methods=['GET', 'POST'])
def quickSearch():
    global result
    msg = ""
    data = []
    qd = 1

    sesId = session['id']
    uname = session['username']
    
    con = mysql.connect()
    cur = con.cursor()
    pref = cur.execute('CALL getPreferences(%s)', (sesId))
    pref = cur.fetchone()
        
    defult_zip = pref[0]
    dist = round(pref[1] / 1609)
    UserRating = pref[3]
    UserRange = pref[2]
    rangePair = getRange(UserRange)
        
    resp = zomato_api.search(defult_zip, dist, "real_distance", sesId, UserRating, rangePair, 0, 0, 0)
    msg = zomato_api.get_msg(resp)
        
    for i in range(int(resp["count"])):
        data.append([resp[i]["name"], resp[i]["id"], resp[i]["address"], resp[i]["phone_number"],
                     resp[i]["aggregate_rating"], resp[i]["menu_url"], resp[i]["featured_image"],
                     resp[i]["rating_icon"]])
                     
    data.sort(reverse = True,key = lambda x: float(x[4]))
    if len(data) == 0:
        session['random'] = 0
    else:
        session['random']= resp['random']['id']
    if result == {}:
        result = {sesId: data}
    else:
        result.popitem()
        result[sesId] = data
    con.close()
    return redirect(url_for('details', username = uname,res_id=session['random'], qd=qd))

"""
Rerolls your quick search results
"""
@app.route('/reroll/', methods =['GET','POST'])
def reroll():
    data = result.get(session['id'])
    i = random.randint(0,(len(data)-1))
    randId = data[i][1]
    return redirect(url_for('details', res_id=randId, qd=1))

"""
Uses the int that is stored in the users range in the database and creates a pair of float values
"""
def getRange(range):
    if range == 1:
        pair = [0.01,10.0]
    elif range == 2:
        pair = [10.01,17.0]
    elif range == 3:
        pair = [17.01,24.0]
    elif range == 4:
        pair = [24.01,31.0]
    else:
        pair = [31.01,1000.0]
    return pair

"""
Displays the details of the resturant chosen by the user  
"""
@app.route('/details/', methods=['GET', 'POST'])
def details():
    msg = ""
    history = 0
    favorite = 0
    if request.args.get('qd'):
        qd = request.args.get('qd')
    else:
        qd = 0
    if 'rest_id' in session:
        if request.args.get('res_id') != session['rest_id']:
            session['rest_id'] = request.args.get('res_id')
            session['history'] = -1
    else:
        session['rest_id'] = request.args.get('res_id')
    res_id = session['rest_id']

    if 'history' in session:
        history = session['history']
    else:
        session['history'] = -1
        history = session['history']

    resp = zomato_api.restaurant_details(res_id)
    estList = str(resp["establishment"]).lstrip("[").rstrip("]").replace("'", "")
    highlightsList = str(resp["highlights"]).lstrip("[").rstrip("]").replace("'", "")
    con = mysql.connect()
    cur = con.cursor()
    commentsList = cur.callproc('getComments', [res_id])
    commentsList = cur.fetchall()
    print("Quick Decide: " + str(qd))

    if not commentsList:
        commentsList = 'empty'
    msg = zomato_api.get_msg(resp)
    if 'username' in session:
        username = session['username']
        favorite = cur.execute('CALL getRestFavorite(%s,%s)', (session['id'], [res_id]))
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
                           mapimageapikey=MAPAPIKEY, commentsList=commentsList, favorite=favorite, history=history,qd=qd)

"""
Allows users to leave comments on a resturant
"""
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
        session['history'] -= 1

    return redirect(url_for('details', res_id=restID))

"""
A users can take a surey and get results based on those, if the user is logged in it will get a user defult prefrence and the users establishment, cuisine, and catagory list
Just like in search it will take in the same fields but if anything a field is different i.e. a new zip code it will update it in the database for the next time
Updates the three list corresponding to the checkbox list on the prefrences page.  
"""
@app.route('/survey/', methods=['GET', 'POST'])
def survey():
    global result
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
                newPref = updateUserPref(pref, sesId, UserZipCode, int(UserDistance), UserRating, UserRange)
                rangePair = getRange(UserRange)
                updateUserList(estList, estab, sesId, 'Call addUserEstablishment(%s,%s)','CALL deleteUserEstablishment(%s,%s)')
                updateUserList(cuisineList, cus, sesId, 'Call addUserCuisine(%s,%s)', 'Call deleteUserCuisine (%s,%s)')
                updateUserList(categoryList, cat, sesId, 'Call addUserCategories(%s,%s)','Call deleteUserCategories(%s,%s)')
                resp = zomato_api.search(UserZipCode, UserDistance, "real_distance", sesId, UserRating, rangePair, 0, 0, 0)
                
                msg = zomato_api.get_msg(resp)
                
                for i in range(int(resp["count"])):
                    data.append([resp[i]["name"], resp[i]["id"], resp[i]["address"], resp[i]["phone_number"],
                             resp[i]["aggregate_rating"], resp[i]["menu_url"], resp[i]["featured_image"],
                             resp[i]["rating_icon"]])
                data.sort(reverse = True,key = lambda x: float(x[4]))
                if len(data) == 0:
                    session['random'] = 0
                    msg = "No results found"
                else:
                    session['random'] = resp['random']['id']
                if result == {}:
                    result = {sesId: data}
                else:
                    result.popitem()
                    result[sesId] = data
                return redirect(url_for('search', msg=msg, username=session['username'],
                                       userRange=newPref[2],
                                       userDistance=round(newPref[1] / 1609), userZipcode=newPref[0],
                                       userRating=newPref[3], pageNum=1, next=10, prev=0,random =session['random']))
        else:
            return render_template('preferences.html', msg=msg, data=data, username=session['username'],
                                   userRange=pref[2], userDistance=pref[1], userZipcode=str(pref[0]), userRating=pref[3],
                                   estList=estList, cuisineList=cuisineList, categoryList=categoryList)
    else:
        if request.method == 'POST':
            if 'zip' in request.form and 'radius' in request.form:
                UserZipCode = request.form['zip']
                UserDistance = int(request.form['radius'])
                UserRating = int(request.form['rating'])
                UserRange = int(request.form['cost'])
                rangePair = getRange(UserRange)
                estab = request.form.getlist('EstCheckboxGroup')
                estab = [int(i) for i in estab]
                estab.sort()
                cus = request.form.getlist('CuisCheckboxGroup')
                cus = [int(i) for i in cus]
                cus.sort()
                cat = request.form.getlist('CatCheckboxGroup')
                cat = [int(i) for i in cat]
                cat.sort()
                resp = zomato_api.search(UserZipCode, UserDistance, "real_distance", 0, UserRating, rangePair, cat, cus, estab)
                msg = zomato_api.get_msg(resp)
                
                for i in range(int(resp["count"])):
                    data.append([resp[i]["name"], resp[i]["id"], resp[i]["address"], resp[i]["phone_number"],
                             resp[i]["aggregate_rating"], resp[i]["menu_url"], resp[i]["featured_image"],
                             resp[i]["rating_icon"]])
                data.sort(reverse = True,key = lambda x: float(x[4]))
                if len(data) == 0:
                    session['random'] = 0
                    msg = "No results found"
                else:
                    session['random'] = resp['random']['id']
                if result == {}:
                    result = {sesId:data}
                else:
                    result.popitem()
                    result[sesId] = data
                return redirect(url_for('search', msg=msg, userRange=UserRange,
                                       userDistance=round(UserDistance / 1609),
                                       userZipcode=UserZipCode, userRating=UserRating, pageNum=1, next=10, prev=0,random=session['random']))
        return render_template('preferences.html', msg=msg)

"""
Shows the users information. the user can update their name and email if needed, update there prefrences and showing you your new results, and allows the user to log out
of the website. 
"""
@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    msg = ''
    if request.method == 'POST':
        if request.form['button'] == 'Save Changes':
            if 'email' in request.form or 'firstname' in request.form or 'lastname' in request.form:
                if request.form['email'] != '' or request.form['firstname'] != '' or request.form['lastname'] != '':
                    con = mysql.connect()
                    cur = con.cursor()
                    if request.form['pwd'] != '' and request.form['pwd-rpt'] != '':
                        hashed = hashlib.sha256(request.form['pwd'].encode('utf-8')).hexdigest()
                        rptHashed = hashlib.sha256(request.form['pwd-rpt'].encode('utf-8')).hexdigest()
                    else:
                        hashed = hashlib.sha256(session['password'].encode('utf-8')).hexdigest()
                        rptHashed = hashlib.sha256(session['password'].encode('utf-8')).hexdigest()
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
                                               email=email, firstname=fname, lastname=lname)
                else:
                    msg = 'You must fill in at least one entry to Save your Changes.'
                    return render_template('profile.html', username=session['username'],
                           msg=msg,email=session['email'],firstname=session['username'].split()[0], lastname=session['username'].split()[-1])
        elif request.form['button'] == 'Logout':
            return redirect(url_for('logout'))
        elif request.form['button'] == 'Modify Preferences':
            return redirect(url_for('survey'))
    return render_template('profile.html', username=session['username'],
                           msg=msg, email=session['email'],
                           firstname=session['username'].split()[0], lastname=session['username'].split()[-1])

#Adds a resturant to the favertes list
@app.route('/addFavorite/', methods=['POST'])
def addFavorite():
    restID = request.form["restaurantID"]
    resName = request.form["restaurantName"]
    print("The session is: " + str(session["id"]) + " - " + str(restID))
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('CALL addFavorite(%s,%s,%s)', (session["id"], restID, resName))
    con.commit()
    con.close()
    session['history'] -= 1
    return redirect(url_for('details', res_id=restID))

#Removes the a resturant from the favorites list
@app.route('/deleteFavorite/', methods=['POST'])
def deleteFavorite():
    restID = request.form["restaurantID"]
    print("The session is: " + str(session["id"]) + " - " + str(restID))
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('CALL deleteFavorite(%s,%s)', (session["id"], restID))
    con.commit()
    con.close()
    session['history'] -= 1
    return redirect(url_for('details', res_id=restID))

#Shows all the users favorate resturants
@app.route('/favorites/', methods=['GET', 'POST'])
def favorites():
    sesId = session['id']
    favoritesList = getFavorites(sesId)
    return render_template('favorites.html', username=session['username'], favoritesList=favoritesList)

#Gets the users favorite resturants
def getFavorites(user_id):
    con = mysql.connect()
    cur = con.cursor()
    favoritesList = cur.execute('CALL getFavorites(%s)', user_id)
    favoritesList = cur.fetchall()
    con.commit()
    con.close()
    return favoritesList


# Updates the user preference if it was changed on the survey page
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
        cur.execute('CALL updateRating(%s,%s)', (UserRate, uId))
        con.commit()
        newRate = UserRate
    else:
        newRate = pref[3]
    if UserRange != pref[2]:
        cur.execute('CALL updateRange(%s,%s)', (UserRange, uId))
        con.commit()
        newRange = UserRange
    else:
        newRange = pref[2]
    con.commit()
    con.close()
    return [newZip, newDis, newRate, newRange]

# Updates the bridging tables in the database based on the checkbox list on the prefrences page
def updateUserList(userList, userCheckBox, uId, addFunction, deleteFunction):
    con = mysql.connect()
    cur = con.cursor()
    if userList != userCheckBox and len(userList) !=0:
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


@app.route('/contactus/', methods=['GET', 'POST'])
def contactus():
    return render_template('contactus.html')


@app.route('/help/', methods=['GET', 'POST'])
def help():
    return render_template('help.html', username=session['username'])

"""
The displays all the users friends, in/out going friend request, and groups
If the user want to send a request checks to see if that user existed or if the user puts in ther own email, display the corresponding error message
else adds the user to the friends list with a pending status.
"""
@app.route('/connect/', methods=['GET', 'POST'])
def connect():
    msg = ''
    confirmed = []
    outPending = []
    inPending = []
    declined = []
    sesId = session['id']
    con = mysql.connect()
    cur = con.cursor()
    if request.method == 'POST':
        if request.form['findFriend'] == 'Submit' and 'friends' in request.form:
            friend = request.form['friends']
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
    groupList = getGroups(sesId)
    for friend in friendsList:
        if friend[3] == 0:
            if friend[5] != sesId:
                outPending.append(friend)
            else:
                pend = cur.execute('CALL getProfile(%s)', (friend[6]))
                pend = cur.fetchone()
                pend = pend + (friend[3],friend[4],friend[5],friend[6])
                inPending.append(pend)
        elif friend[3] == 1 and friend[5] != sesId:
            confirmed.append(friend)
        elif friend[3] == 2 and friend[5] != sesId:
            declined.append(friend)
    return render_template('AddFriends.html', username=session['username'], data=confirmed, inPending = inPending ,outPending=outPending, declined=declined, groups = groupList)

#Adds a friend to the pending list the other users has to either accept or decline their friend request
def addFriend(friendId, userId):
    con = mysql.connect()
    cur = con.cursor()
    status = 0
    if (status != 1 and friendId != userId):
        cur.execute('CALL addFriend(%s,%s,%s)', (userId, friendId,status))
        con.commit()
    con.close()

#Gets all your friends regardless of status
def getFriends(Fk_user):
    con = mysql.connect()
    cur = con.cursor()
    friendsList = cur.execute('CALL getFriends(%s)', (Fk_user))
    friendsList = cur.fetchall()
    con.commit()
    con.close()
    return friendsList

#Removes a friend from your friends list
def deleteFriend(friends_id, Fk_user, status):
    con = mysql.connect()
    cur = con.cursor()
    if (status == 1 and friends_id != Fk_user):
        cur.execute('CALL deleteFriend(%s, %s)', (friends_id, Fk_user))
        con.commit()
    con.close()

#Updates the pending user either accepting or declining their friend request.
@app.route('/update/<int:friends_id>/<int:Fk_user>/<int:status>', methods = ['GET','POST'])
def updateFriend(friends_id,Fk_user,status):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('CALL updateFriend(%s, %s, %s)', (friends_id, Fk_user, status))
    cur.execute('CALL addFriend(%s,%s,%s)', (friends_id,Fk_user,status))
    con.commit()
    con.close()
    return redirect(url_for('connect'))

@app.route('/editGroups/<int:fk_group>', methods = ['GET','POST'])
def editGroup(fk_group):
    uname = session['username']
    return render_template('editGroupPage.html', username = uname)

#Creates a new group with the name given by the user and make them the creator/owner. Returns you back to the connect page
@app.route('/addGroup/', methods =['GET','POST'])
def addGroup():
    if request.method == 'POST':
        if 'addgroup' in request.form:
            groupname = request.form['addgroup']
            user_id = session['id']
            con = mysql.connect()
            cur = con.cursor()
            cur.execute('CALL addGroup(%s,%s,@status)', (groupname, user_id))
            con.commit()
            con.close()
    return redirect(url_for('connect'))

#Adds a new user to the group
def addToGroup(group_id, user_id):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('CALL addToGroup(%s, %s, @status)', (group_id, user_id)) 
    con.commit()
    con.close()

#Gets the groups name, id, and all members with the group. The first member id in the group is the also the creator/owner of the group
def getGroups(user_id):
    con = mysql.connect()
    cur = con.cursor()
    groupMembers = []
    groupsList = cur.execute('CALL getGroups(%s)', (user_id))
    groupsList =  cur.fetchall()
    for i in groupsList:
        membersList = cur.execute('CALL getGroupMembers(%s)',(i[1]))
        membersList = [val for sublist in cur.fetchall() for val in sublist]
        membersList = [i[0]]+[i[1]]+membersList
        groupMembers.append(membersList) 
    print(groupMembers)
    con.commit()
    con.close()
    return groupMembers

#Removes the user from the group
def deleteFromGroup(group_id, user_id):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('CALL deleteFromGroup(%s, %s)', (group_id, user_id))
    con.commit()
    con.close()

#Deletes the Group created by the user
@app.route('/deleteGroup/<int:user_id>/<int:fk_group>', methods = ['GET','POST']) 
def deleteUserGroup(user_id, fk_group):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('CALL deleteUserGroup(%s, %s)', (user_id, fk_group))
    con.commit()
    con.close()
    return redirect(url_for('connect'))

#sends the confirmation email to the user
def regestrationMessage(email, url):
    msg = Message('Confirmation Email', sender = MAIL_USERNAME, recipients =[email])
    msg.body = "Please confirm your email " + url
    mail.send(msg)

#creates a token using the apps secret key and mask the value with salt value
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

#Checks to see if the token is accociate with an email, if true returns the email, else returns false
def confirm_token(token,expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token,salt=app.config['SECURITY_PASSWORD_SALT'] ,max_age=expiration)
    except:
        return False
    return email

"""
when the user clicks the url in the confirmation email, checks to see if the token in the email corresponds with token created by the email
if the account is not currently active, updates the database to mark the account as an active account
then sends the user to the home page
"""
@app.route('/connect/<token>')
def confirm_email(token):
    con = mysql.connect()
    cur = con.cursor()
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.')
    active = cur.execute("CALL getActivity(%s)", (email))
    active = cur.fetchall()
    if active[0] == 1:
        flash('Account is already confirmed.')
    else:
        cur.execute("CALL updateUserActivity(%s,%s)", (1,session['id']))
        con.commit()
        con.close()
        flash('Your email is confirmed, thank you')
    return redirect(url_for('home'))
    
if __name__ == '__main__':
    app.run(debug=True)
