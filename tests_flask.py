import unittest

from flask.ext.testing import TestCase

from app import app, db
from app.users.models import User, UserInfo
from app.energy.models import EnergyData
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
        
    def test_sign(self):
        u = User('email22', 'password')

        db.session.add(u)
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

    def test_info_setup(self):
        u = User('SetUp', 'User')
        db.session.add(u)
        db.session.commit()
        
        u_id = User.query.filter_by(email='SetUp').first().id
        ui = UserInfo._make_user_info_with_email('SetUp', 1, 1, 1, 1)
        db.session.add(ui)
        db.session.commit()    
        assert ui.__repr__() == UserInfo.query.filter_by(user_id=u_id).first().__repr__() == \
            "<UserInfo> User : %d, Type %d%d%d%d"%(u_id, 1, 1, 1, 1)

        u = User('SetUp2', 'User')
        db.session.add(u)
        db.session.commit()

        rv = self.info_setup('SetUp2', 1, 1, 1, 1)
        
        assert rv.data == 'True'
        assert UserInfo.query.filter_by(user_id=u_id).first().__repr__() == \
            "<UserInfo> User : %d, Type %d%d%d%d"%(u_id, 1, 1, 1, 1)

        rv = self.info_setup('SetUp2', 1, 1, 1, 1)
        assert rv.data == 'True'
        
    def test_insert_energy(self):

        u = User('Energy', 'password')
        db.session.add(u)
        db.session.commit()

        from datetime import datetime
        EnergyData(1, datetime.now(), 10)
        submit_time = datetime(2013, 11, 2)
        rv = self.insert_energy_data('Energy', submit_time, 10)
        assert rv.data == 'True'
        
    def insert_energy_data(self, email, submit_time, energy_amount):
        return self.client.post('/energy/insert/', data = dict(
            userEmail = email,
            submitTime = submit_time,
            energyAmount = energy_amount
            ), follow_redirects=True)



    def info_setup(self, email, house_type, house_area, income_type, cooler_heater_type):
        return self.client.post('/users/setup/', data = dict(
            userEmail = email, 
            houseType = house_type,
            houseArea = house_area,
            incomeType = income_type,
            coolerHeaterType = cooler_heater_type
            ), follow_redirects=True)

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
