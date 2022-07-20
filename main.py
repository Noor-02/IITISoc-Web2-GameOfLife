from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "abc"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/iitisoc_database'
db = SQLAlchemy(app)

current_user = None

class user_details(db.Model):
    # sno,username,password,fullName,email
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)


def user_exists(username):
    user = user_details.query.filter_by(username = username).first()
    if(user):
        return True
    else:
        return False


@app.route("/")
def homepage():
    return render_template('homepage.html', current_user = current_user)

@app.route("/login_signup")
def login_signup():
    global current_user
    if(current_user):
        return redirect('/')
    else:
        return render_template('login_signup.html')

@app.route("/feedback", methods = ['GET','POST'])
def feedback():
    return render_template('feedback.html')

@app.route("/login", methods = ['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = user_details.query.filter_by(email=email).first()
    if(user):
        if(password == user.password):
            global current_user
            current_user = user.username
            return redirect('/')
        else:
            return ("Invalid email or password")
    else:
        return ("Invalid email or password")

@app.route("/signup", methods = ['POST'])
def signup():
    username = request.form.get('username')
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if(password!=confirm_password):
        return render_template('login_signup.html')
    elif(user_exists(username)):
        return render_template('login_signup.html')
    else:
        global current_user
        current_user = username
        entry = user_details(username=username, fullname=fullname, email=email, password=password)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')

@app.route("/logout")
def logout():
    global current_user
    current_user = None
    return redirect('/')


@app.route("/Game_of_life")
def Game_of_life():
    return render_template('Game of life.html', current_user = current_user)

@app.route("/users/<string:username>")
def displayProfile(username):
    if(user_exists(username)):
        return render_template('profile.html', username=username, current_user = current_user)
    else:
        return ("Invalid user")
app.run()