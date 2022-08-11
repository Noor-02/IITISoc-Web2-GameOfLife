from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "abc"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/iitisoc_database'
db = SQLAlchemy(app)


class user_details(db.Model):
    # sno,username,password,fullName,email
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)


class Feedback(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(3000), nullable=False)


def user_exists(username):
    user = user_details.query.filter_by(username = username).first()
    if(user):
        return True
    else:
        return False


@app.route("/")
def homepage():
    username = request.cookies.get('username')
    return render_template('homepage.html', current_user = username)
@app.route("/about")
def imadeit():
    return render_template('abtus1.html')

@app.route("/login_signup")
def login_signup():
    username = request.cookies.get('username')
    if(username):
        return redirect('/')
    else:
        return render_template('login_signup.html')

@app.route("/feedback", methods = ['GET','POST'])
def feedback():
    if(request.method=='POST'):
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        rating = request.form.get('stars')
        message = request.form.get('message')
        entry = Feedback(fullname=fullname, email=email, rating=rating, message=message)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('feedback.html')

@app.route("/login", methods = ['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = user_details.query.filter_by(email=email).first()
    if(user):
        if(password == user.password):
            flash("Successful login")
            resp = make_response(redirect('/'))
            resp.set_cookie('username', user.username)
            return resp
        else:
            flash('Incorrect Password')
            return redirect(url_for('login_signup'))
    else:
        flash('User does not exist')
        return redirect(url_for('login_signup'))

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
        entry = user_details(username=username, fullname=fullname, email=email, password=password)
        db.session.add(entry)
        db.session.commit()
        resp = make_response(redirect('/'))
        resp.set_cookie('username', username)
        return resp

@app.route("/logout")
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('username')
    return resp

@app.route("/Game_of_life")
def Game_of_life():
    current_user = request.cookies.get('username')
    return render_template('Game of life.html', current_user=current_user)

@app.route("/users/<string:username>")
def displayProfile(username):
    current_user = request.cookies.get('username')
    if(user_exists(username)):
        return render_template('profile.html', username=username, current_user=current_user)
    else:
        return ("Invalid user")
app.run()