from app import app, lm, db
from flask import render_template, redirect, flash, session, url_for, g
from forms import LoginForm, SignUpForm, EditProfileForm, PostForm, SearchForm
from datetime import datetime
from flask.ext.login import current_user, login_user, logout_user, login_required
from models import User, Post
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	if current_user.is_authenticated():
		current_user.last_seen = datetime.utcnow()
		db.session.add(current_user)
		db.session.commit()
		g.search_form = SearchForm()


@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page = 1):
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body = form.post.data, timestamp = datetime.utcnow(), author = g.user)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))

	posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
	return render_template("index.html",title = 'Home', form = form, posts = posts)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	form = SignUpForm()
	if form.validate_on_submit():
		nickname = User.make_unique_name(form.nname.data)
		u = User(nickname = nickname, email = form.email.data, pwd = form.pwd.data)
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
		u = User.authenticate(form.email.data, form.pwd.data)
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
@app.route('/user/<nickname>/<int:page>')
def user(nickname, page = 1):
	user = User.query.filter_by(nickname = nickname).first()
	if user is None:
		flash("User not found...")
		return redirect(url_for('index'))
	posts = user.sorted_posts().paginate(page, POSTS_PER_PAGE, False)
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


@app.route('/follow/<nickname>')
def follow(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	if user == None:
		flash('User ' + nickname +' not found')
		return redirect(url_for('index'))
	if user == g.user:
		flash("You can't follow yourself")
		return redirect(url_for('user', nickname = nickname))

	u = g.user.follow(user)
	if u is None:
		flash("Can't follow" + nickname + '.')
		return redirect(url_for('user', nickname = nickname))

	db.session.add(u)
	db.session.commit()

	flash ("Your are now following " + nickname)
	return redirect(url_for('user', nickname = nickname))

@app.route('/unfollow/<nickname>')
def unfollow(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	if user == None:
		flash('User ' + nickname +' not found')
		return redirect(url_for('index'))
	if user == g.user:
		flash("You can't unfollow yourself")
		return redirect(url_for('user', nickname = nickname))
	u = g.user.unfollow(user)
	if u is None:
		flash("Can't unfollow" + nickname + '.')
		return redirect(url_for('user', nickname = nickname))
	db.session.add(u)
	db.session.commit()
	flash("Your have stopped following " + nickname + '.')
	return redirect(url_for('user', nickname = nickname))

@app.route('/search',methods = ['POST'])
def search():
	if not g.search_form.validate_on_submit():
		return redirect(url_for('index'))
	return redirect(url_for('search_result', query = g.search_form.search.data))

@app.route('/search_result/<query>')
def search_result(query):
	results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
	return render_template('search_result.html', query = query , results = results)

@app.errorhandler(404)
def internal_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500



	