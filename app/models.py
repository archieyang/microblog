from app import db
import hashlib, time
ROLE_USER = 0
ROLE_ADMIM = 1


followers = db.Table('followers', db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	salt = db.Column(db.Integer)
	secure_hashed_pwd = db.Column(db.String(120))
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)

	followed = db.relationship('User', 
		secondary = followers,
		primaryjoin = (followers.c.follower_id == id),
		secondaryjoin = (followers.c.followed_id == id),
		backref = db.backref('followers', lazy = 'dynamic'),
		lazy = 'dynamic'
		)

	def __init__(self, nickname, email, pwd):
		self.nickname = nickname
		self.email = email
		self.salt = int(time.time())
		self.secure_hashed_pwd = User.__secure_hash(pwd, self.salt)

	@staticmethod
	def authenticate(email, password):
		user = User.query.filter_by(email = email).first()
		if user is None:
			return None
		if user.secure_hashed_pwd != User.__secure_hash(password, str(user.salt),):
			return None
		return user

		
	@staticmethod
	def __secure_hash(pwd, salt):
		return hashlib.sha1(pwd + '--' + str(salt) ).hexdigest()

	@staticmethod
	def make_unique_name(nickname):
		if User.query.filter_by(nickname = nickname).first() == None:
			return nickname
		version = 2
		while True:
			new_nickname = nickname +str(version)
			if User.query.filter_by(nickname = new_nickname).first() == None:
				return new_nickname
			version += 1
		return new_nickname

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0
		
		
	def followed_posts(self):
		return Post.query.join(followers, (followers.c.followed_id == Post.user_id))\
		.filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())
		

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User email: %r, nickname: %r, salt: %r>' % (self.email, self.nickname, self.salt)


class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)



		
