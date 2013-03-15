#!/home/archie/venv/bin/python
from coverage import coverage
cov = coverage(branch=True, omit=['test.py', '/home/archie/venv/lib/*'])
cov.start()
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Post
from datetime import datetime, timedelta


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '/tmp/test.db')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        u = User(nickname='nick', email='nick@amail.com', pwd='abcd')
        db.session.add(u)
        db.session.commit()
        assert u.is_authenticated() is True
        assert u.is_active() is True
        assert u.is_anonymous() is False
        assert u.id == int(u.get_id())

    def test_make_unique_name(self):
        u = User(nickname='archie', email='yang07@gmail.com', pwd='notagoodpwd')
        db.session.add(u)
        db.session.commit()

        nickname = User.make_unique_name('archie')
        assert nickname != 'archie'
        u = User(nickname=nickname, email='one@gmail.com', pwd='abcef')
        db.session.add(u)
        db.session.commit()

        nickname2 = User.make_unique_name('archie')
        assert nickname2 != 'archie'
        assert nickname2 != nickname

        u = User.make_unique_name('wohahah')
        assert u == 'wohahah'

    def test_follow(self):
        u1 = User(nickname='teste', email='a@balala.com', pwd='333')
        u2 = User(nickname='leeww', email='leeww@b.com', pwd='333')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) is None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().nickname == 'leeww'
        assert u2.followers.count() == 1
        assert u2.followers.first().nickname == 'teste'
        u = u1.unfollow(u2)
        db.session.add(u)
        db.session.commit()

        assert u1.is_following(u2) is False
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

    def test_follow_posts(self):
        u1 = User(nickname='a', email='a@a.a', pwd='a')
        u2 = User(nickname='b', email='b@a.a', pwd='a')
        u3 = User(nickname='c', email='c@a.a', pwd='a')
        u4 = User(nickname='d', email='d@a.a', pwd='a')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)

        utcnow = datetime.utcnow()
        p1 = Post(body='post from a', author=u1, timestamp=utcnow + timedelta(seconds=1))
        p2 = Post(body='post from b', author=u2, timestamp=utcnow + timedelta(seconds=2))
        p3 = Post(body='post from c', author=u3, timestamp=utcnow + timedelta(seconds=3))
        p4 = Post(body='post from d', author=u4, timestamp=utcnow + timedelta(seconds=4))
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

        # import pdb
        assert len(f1) == 3
        assert len(f2) == 2
        assert len(f3) == 2
        assert len(f4) == 1
        # import pdb
        #
        # assert f1 == [p4, p2, p1]
        # assert f2 == [p3, p2]
        # assert f3 == [p4, p3]
        # assert f4 == [p4]
        assert f1[0].id == p4.id
        assert f1[1].id == p2.id
        assert f1[2].id == p1.id
        assert f2[0].id == p3.id
        assert f2[1].id == p2.id
        assert f3[0].id == p4.id
        assert f3[1].id == p3.id
        assert f4[0].id == p4.id

    def test_delete_post(self):
        u = User(nickname='Jafqqnny', email='jannyjqqanny@gmail.com', pwd='abcedf')
        p = Post(body='test_post', author=u, timestamp=datetime.utcnow())
        db.session.add(u)
        db.session.add(p)

        db.session.commit()

        p = Post.query.get(1)
        db.session.remove()

        db.session = db.create_scoped_session()
        db.session.delete(p)
        db.session.commit()

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass

    cov.stop()
    cov.save()
    print '\nCoverage Report:\n'
    cov.report()
    print 'HTML version:' + os.path.join(basedir, 'tmp/coverage/index.html')
    cov.html_report(directory='tmp/coverage')
    cov.erase()
