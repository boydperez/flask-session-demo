import sqlite3
import time
from flask import Flask, render_template, redirect, request, url_for, session
from datetime import timedelta

from validate import Validate


app = Flask(__name__)
app.config['SECRET_KEY'] = "skdfjewif38rf3rirhfn2f9hp23f"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=5)


DATABASE = 'users'

try:
    conn = sqlite3.connect(DATABASE + '.db', check_same_thread=False)
    print(f"Connected to {DATABASE}")
except Exception:
    print("Database not accessible")


def user_authenticated():
    """
    Check if user is already authenticated and has initialized a session. 
    """
    if 'user' in session:
        return True
    else:
        return False


@app.route('/')
def home():
    if user_authenticated(): 
        return redirect(url_for('user', user=session['user']))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["passwd"]
        confirm_password = request.form["confirmPasswd"]

        validate = Validate()
        validate.set_username_validators(min_length=4, max_length=12)

        username_check = validate.validate_username(username.strip())
        password_check = validate.validate_password(password, confirm_password)

        if username_check == 'PASS' and password_check == 'PASS':
            # Insert into database 
            global conn
            params = (username, password)
            conn.execute("INSERT INTO user (username, password) VALUES (?, ?)", params)
            conn.commit()

            session.permanent = True
            session['user'] = username
            return redirect(url_for('login', user=username))
        elif username_check == 'USERNAME_NULL':
            message = "username field is left blank"
        elif username_check == 'USERNAME_LENGTH_VIOLATED':
            message = "username length should be of min 4 and max 12 characters"
        elif username_check == 'USERNAME_VIOLATED':
            message = "username can consist of alphanumeric characters and cannot start with a digit"
        elif password_check == 'PASSWD_UNMATCH':
            message = "passwords do not match"
        elif password_check == 'PASSWD_WEAK':
            message = "weak password"
        else: 
            message = "some error occurred"

        return render_template('register.html', message=message)

    else:
        if user_authenticated(): 
            return render_template('force_logout.html')

    return render_template('register.html', message='')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['passwd']
        
        # Grab the users from the database
        global conn
        cursor = conn.execute("SELECT username, password from user;")
        
        for row in cursor:
            if user == row[0] and password == row[1]:
                session.permanent = True
                session['user'] = user
                return redirect(url_for('user', user=user))
        # TODO: Flash message
        return render_template('login.html')
    else:
        if user_authenticated():
            return redirect(url_for('user', user=session['user']))
    return render_template('login.html')

@app.route('/<user>')
def user(user):
    if user_authenticated() and session['user'] == user:
        return render_template('home.html', user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if user_authenticated():
        session.pop('user')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)