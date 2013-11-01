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
        A = User('A', 'A')
        B = User('B', 'B')
        C = User('C', 'C')

        db.session.add(A)
        db.session.add(B)
        db.session.add(C)
        db.session.commit()

        UserRelation.make_relation_two_user(A.id, B.id)
        UserRelation.make_relation_two_user(B.id, C.id)

        assert len(UserRelation.query.filter_by(user_id=A.id).all()) == 1
        assert len(UserRelation.query.filter_by(user_id=B.id).all()) == 2
        assert len(UserRelation.query.filter_by(user_id=C.id).all()) == 1

        
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
