from app import app, lm, db
from flask import render_template, redirect, flash, session, url_for, g
from forms import LoginForm, SignUpForm, EditProfileForm
from datetime import datetime
from flask.ext.login import current_user, login_user, logout_user, login_required
import models

@lm.user_loader
def load_user(id):
	return models.User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	if current_user.is_authenticated():
		current_user.last_seen = datetime.utcnow()
		db.session.add(current_user)
		db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
	user = current_user
	posts = [
	{'author': { 'nickname': 'John' },'body': 'Beautiful day in Portland!'},
	{'author': { 'nickname': 'Susan' }, 'body': 'The Avengers movie was so cool!' }
	]
	return render_template("index.html",title = 'Home', user = user, posts = posts)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	form = SignUpForm()
	if form.validate_on_submit():
		nickname = models.User.make_unique_name(form.nname.data)
		u = models.User(nickname = nickname, email = form.email.data, pwd = form.pwd.data)
		db.session.add(u)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('signup.html', title = 'Sign Up', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))

	form = LoginForm()
	if form.validate_on_submit():
		u = models.User.authenticate(form.email.data, form.pwd.data)
		if u is not None:
			flash("Login Succeed!")
			login_user(u, remember = form.remember_me.data)
			return redirect(url_for('index'))
		flash ("Error in login...")
	return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
	
@app.route('/user/<nickname>')
def user(nickname):
	user = models.User.query.filter_by(nickname = nickname).first()
	if user is None:
		flash("User not found...")
		return redirect(url_for('index'))
	posts = [
		{'author':user, 'body': 'Test Post #1'},
		{'author':user, 'body': 'Test Post #2'}
	]
	return render_template('user.html',user = user, posts = posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(g.user.nickname)
	flash(g.user.nickname)
	
	if form.validate_on_submit():
		print 'inside validate_on_submit'
		g.user.about_me = form.about_me.data
		g.user.nickname = form.nickname.data
		db.session.add(g.user)
		db.session.commit()
		flash("About me save !")
		return redirect(url_for('index'))
		
	return render_template('edit_profile.html', form = form)

@app.errorhandler(404)
def internal_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500



	