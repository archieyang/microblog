#!/home/archie/venv/bin/python

import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Post
from datetime import datetime, timedelta


class TestClase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()
	def tearDown(self):
		db.session.remove()
		db.drop_all()
	def test_make_unique_name(self):
		u = User(nickname = 'archie', email = 'yang07@gmail.com', pwd = 'notagoodpwd')
		db.session.add(u)
		db.session.commit()
		nickname = User.make_unique_name('archie')
		assert nickname != 'archie'
		u = User(nickname = nickname, email = 'one@gmail.com', pwd = 'abcef')
		db.session.add(u)
		db.session.commit()
		nickname2 = User.make_unique_name('archie')
		assert nickname2 != 'archie'
		assert nickname2 != nickname

	def test_follow(self):
		u1 = User(nickname = 'archie', email = 'a@b.com', pwd = '333')
		u2 = User(nickname = 'lee', email = 'lee@b.com', pwd = '333')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		assert u1.unfollow(u2) == None 
		u = u1.follow(u2)
		db.session.add(u)
		db.session.commit()
		assert u1.follow(u2) == None
		assert u1.is_following(u2)
		assert u1.followed.count() == 1
		assert u1.followed.first().nickname == 'lee'
		assert u2.followers.count() == 1
		assert u2.followers.first().nickname == 'archie'
		u = u1.unfollow(u2)
		db.session.add(u)
		db.session.commit()

		assert u1.is_following(u2) == False
		assert u1.followed.count() == 0
		assert u2.followers.count() == 0

	def test_follow_posts(self):
		u1 = User(nickname = 'a', email = 'a@a.a', pwd = 'a')
		u2 = User(nickname = 'b', email = 'b@a.a', pwd = 'a')
		u3 = User(nickname = 'c', email = 'c@a.a', pwd = 'a')
		u4 = User(nickname = 'd', email = 'd@a.a', pwd = 'a')
		db.session.add(u1)
		db.session.add(u2)
		db.session.add(u3)
		db.session.add(u4)

		utcnow = datetime.utcnow()
		p1 = Post(body = 'post from a', author = u1, timestamp = utcnow + timedelta(seconds = 1))
		p2 = Post(body = 'post from b', author = u2, timestamp = utcnow + timedelta(seconds = 2))
		p3 = Post(body = 'post from c', author = u3, timestamp = utcnow + timedelta(seconds = 3))
		p4 = Post(body = 'post from d', author = u4, timestamp = utcnow + timedelta(seconds = 4))
		db.session.add(p1)
		db.session.add(p2)
		db.session.add(p3)
		db.session.add(p4)
		db.session.commit()

		u1.follow(u1)
		u1.follow(u2)
		u1.follow(u4)
		u2.follow(u2)
		u2.follow(u3)
		u3.follow(u3)
		u3.follow(u4)
		u4.follow(u4)

		db.session.add(u1)
		db.session.add(u2)
		db.session.add(u3)
		db.session.add(u4)
		db.session.commit()

		f1 = u1.followed_posts().all()
		f2 = u2.followed_posts().all()
		f3 = u3.followed_posts().all()
		f4 = u4.followed_posts().all()


		assert len(f1) == 3
		assert len(f2) == 2
		assert len(f3) == 2
		assert len(f4) == 1

		assert f1 == [p4, p2, p1]
		assert f2 == [p3, p2]
		assert f3 == [p4, p3]
		assert f4 == [p4]




if __name__ == '__main__':
	unittest.main()