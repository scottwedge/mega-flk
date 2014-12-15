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
        u = User(nickname='jonas', email='baptiste.ossipow@gmail.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/fffa91d1b69915096150fcb597b8f881'
        assert avatar[0:len(expected)] == expected

    

    def test_make_unique_nickname(self):
        u = User(nickname='jonas', email='baptiste.ossipow@gmail.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('jonas')
        assert nickname != 'jonas'
        u = User(nickname=nickname, email='bop@web.nl')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('jonas')
        assert nickname2 != 'jonas'
        assert nickname2 != nickname

if __name__ == '__main__':
    unittest.main()
                 
        
