#!/home/archie/venv/bin/python

import os
import unittest

from config import basedir
from app import app, db
from app.models import User

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

if __name__ == '__main__':
	unittest.main()