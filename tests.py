#!../bin/python

import os
import unittest

from config import basedir
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(nickname='jonas', email='jonas.ossipow@gmail.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/b8ff9eed8d1431c043ef0a460971a0c7'
        assert avatar[0:len(expected)] == expected

        
    def test_make_unique_nickname(self):
        u = User(nickname='jonas', email='jonas.ossipow@gmail.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('jonas')
        assert nickname != 'jonas'
        u = User(nickname=nickname, email='nati@web.nl')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('jonas')
        assert nickname2 != 'jonas'
        assert nickname2 != nickname

    def test_follow(self):
        u1 = User(nickname='jonas', email='jonas.ossipow@gmail.com')
        u2 = User(nickname='nati', email='nati@web.nl')
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
        assert u1.followed.first().nickname == 'nati'
        assert u2.followers.count() == 1
        assert u2.followers.first().nickname == 'jonas'
        u = u1.unfollow(u2)
        assert u is not None
        db.session.add(u)
        db.session.commit()
        assert not u1.is_following(u2)
        assert u1.followed.count() == 0
        assert u2.followers.count != 0
        

if __name__ == '__main__':
    unittest.main()
                 
        
