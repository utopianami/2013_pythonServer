import unittest

from flask.ext.testing import TestCase

from app import app, db
from app.users.models import User, UserInfo
from app.energy.models import EnergyData, RealTimeEnergyData
from pprint import pprint
from datetime import datetime, timedelta
import random

HOUSE_AREA = [113, 169, 221, 254, 287, 323,352, 360]
HOUSE_TYPE = [0.80, 0.97, 1.04,  1.17]
INCOME_TYPE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
COOLER_HEATER_TYPE = [0, 1, 2, 3]
energy_data_list = []

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

    def test_get_set_energy_data(self):
        rv = self.sign_up('test', 'test')
        
        energy_amount=100
        test_year, test_month, test_day, test_hour, test_minute, test_second = 2013, 11, 29, 16, 59, 50
        time_gap = timedelta(seconds=3)
        time = datetime(test_year, test_month, test_day, test_hour, test_minute, test_second)
        for i in xrange(20):
            print time
            energy_amount+=3
            a = RealTimeEnergyData('test', energy_amount)
            a.submit_time = time
            a.push_data()
            time += time_gap
        
        

    def test_goal(self):
        u = User('goal', 'goal')
        db.session.add(u)
        db.session.commit()
        assert User.query.count() == 1

        ui = UserInfo._make_user_info_with_email('goal', 5, 3, 9, 3)
        db.session.add(ui)
        db.session.commit()

        rv = self.goal('goal', '5')
        
        assert rv.data=='True'

        assert User.query.filter_by(email='goal').first().user_info.first().goal==5

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

    def tmp_test_info_setup(self):
        self.make_users()
        #print 'Make Users : %d'%(len(User.query.all() ) )
        self.ptrol_all_users()

        #print UserInfo.query.count() == 12
        #print User.query.count() == 12
        #pprint(User.query.all())

        test_user = User('test_user5393', '5393')
        db.session.add(test_user)
        db.session.commit()

        test_user_info = UserInfo._make_user_info_with_email('test_user5393', 5, 3, 9, 3)
        db.session.add(test_user_info)
        db.session.commit()
        
        assert UserInfo.query.count() == 13
        assert User.query.count() == 13

        test_user = User.find_by_email('test_user5393')
        test_user_info = test_user.user_info.first()
        
        #print test_user_info.get_avg_energy_data_with_date(datetime(2013, 10, 1, 1), datetime(2013, 10, 31, 23, 59, 59))

        self.sign_up('test_user7193', '7193')   
        self.sign_in('test_user7193', '7193')   
        self.info_setup('test_user7193', 7, 1, 9 , 3)

        test_user = User.find_by_email('test_user7193')
        test_user_info = test_user.user_info.first()
        
        #print test_user_info.get_avg_energy_data_with_date(datetime(2013, 10, 1, 1), datetime(2013, 10, 31, 23, 59, 59))

    def tmp_test_insert_energy(self):

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

    def make_electricity_data(self):
        
        for type_val in HOUSE_AREA:
            temp_list = []
            for area_val in HOUSE_TYPE:
                val = "%d"%(type_val/30 * area_val * 1000 /24) 
                temp_list.append(int(val)) 
            energy_data_list.append(temp_list)
        
        #print 'EnergyData List Success make'
        #pprint(energy_data_list)


                
    def make_users(self):
        for house_area in xrange(5, len(HOUSE_AREA)):
            for house_type in xrange(0,4):
                for income in xrange(9,10):
                    for cooler_heater_type in xrange(3, 4): 
                        user_email = "User%d%d%d%d"%(house_area, house_type, income, cooler_heater_type)
                        password = 'password'
                        
                        u = User(user_email, password)
                        db.session.add(u)
                        db.session.commit()

                        ui = UserInfo._make_user_info_with_email(user_email, house_area, house_type, income, cooler_heater_type)
                        db.session.add(ui)
                        db.session.commit()

    def make_energy_data(self,user_email, energy_amount):
        DEFAULT_YEAR, DEFAULT_MOONTH, DEFAULT_DAY, DEFAULT_TIME = 2013, 10, 1, 0
        minus_flag = -1

        dt = datetime(DEFAULT_YEAR, DEFAULT_MOONTH, DEFAULT_DAY, DEFAULT_TIME)
        for day_plus in xrange(1, 31):
            for time_plus in xrange(0,24):
                
                growth_amount = random.random()*10*minus_flag
                energy_amount += growth_amount
                minus_flag *= -1

                ed = EnergyData._make_energy_data_with_email(user_email, dt, energy_amount)
                db.session.add(ed)
                dt += timedelta(hours=1)

        db.session.commit()
                

    def ptrol_all_users(self):  
        self.make_electricity_data()

        for house_area in xrange(5, len(HOUSE_AREA)):
            for house_type in xrange(0,len(HOUSE_TYPE)):
                for income in xrange(9,len(INCOME_TYPE)):
                    for cooler_heater_type in xrange(3, len(COOLER_HEATER_TYPE)): 
                        energy_amount = (energy_data_list[house_area][house_type])  
                        user_email = "User%d%d%d%d"%(house_area, house_type, income, cooler_heater_type)
                        
                        self.make_energy_data(user_email, energy_amount)

    def info_setup(self, email, house_area, house_type, income_type, cooler_heater_type):
        return self.client.post('/users/setup/', data = dict(
            userEmail = email, 
            houseArea = house_area,
            houseType = house_type,
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
            userPassword=user_password
            ), follow_redirects=True)

    def goal(self, user_email, goal_data):
        return self.client.post('/users/goal/', data = dict(
            userEmail = user_email,
            goalData = goal_data
            ), follow_redirects=True)

    def setrecycledata(self, user_email, energy_amount):
        return self.client.post('/energy/setrecycledata/', data = dict(
            userEmail = user_email,
            energyAmount = energy_amount
            ), follow_redirects=True)

    def getrecycledata(self, user_email):
        return self.client.post('/energy/getrecycledata/', data = dict(
            userEmail = user_email,
            ), follow_redirects=True)        
        

if __name__ == '__main__':
    unittest.main()
