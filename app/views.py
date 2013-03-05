from app import app
from flask import render_template, redirect, flash
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname':'Archie'}
	posts = [
	{'author': { 'nickname': 'John' },'body': 'Beautiful day in Portland!'},
	{'author': { 'nickname': 'Susan' }, 'body': 'The Avengers movie was so cool!' }
	]
	return render_template("index.html",title = 'Home', user = user, posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash("Message" + form.oid.data + str(form.remember_me.data))
		return redirect('/index')
	return render_template('login.html', title = 'Sign In', form = form)

	