
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