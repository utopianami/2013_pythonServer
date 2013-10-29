import unittest

from flask.ext.testing import TestCase

from app import app, db
from app.users.models import User, UserRelation
from pprint import pprint

class ManyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_relation(self):
        pass
        
    def test_sign(self):

        a = User('email22', 'password')

        db.session.add(a)
        db.session.commit()
        assert len(User.query.all()) == 1

        rv = self.sign_up('Hi', 'Man')
        assert rv.data == 'True'
        assert len(User.query.all()) == 2 

        rv = self.sign_up('Hi', 'Man')
        assert rv.data == 'False'
        assert len(User.query.all()) == 2         

        rv = self.sign_in('Hi', 'Man')
        assert rv.data == 'True'

        rv = self.sign_in('Ha', 'Man')
        assert rv.data == 'False'

    def sign_up(self, user_email, user_password):
        return self.client.post('/users/signup/', data = dict(
            userEmail=user_email, 
            userPassword=user_password
            ), follow_redirects=True)

    def sign_in(self, user_email, user_password):
        return self.client.post('/users/signin/', data = dict(
            userEmail=user_email,
            userPassword=user_password)
        , follow_redirects=True)

if __name__ == '__main__':
    unittest.main() 
