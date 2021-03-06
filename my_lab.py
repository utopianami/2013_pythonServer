# -*- coding:utf-8 -*-
from app import app, db
from app.users.models import User, UserInfo
from app.energy.models import EnergyData

from pprint import pprint
from datetime import datetime, timedelta
import random

HOUSE_AREA = [113, 169, 221, 254, 287, 323,352, 360]
HOUSE_TYPE = [0.80, 0.97, 1.04,  1.17]
INCOME_TYPE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
COOLER_HEATER_TYPE = [0, 1, 2, 3]
energy_data_list = []

	
def getUserLikeType():
	return UserInfo.query.filter_by(house_type=1, house_area=1, income_type=1, cooler_heater_type=1)

def getEnergyDataWithDate(user_id, start_date, end_date):
	return EnergyData.query.filter(EnergyData.user_id==user_id, \
		EnergyData.submit_time>start_date, \
		EnergyData.submit_time<end_date \
		)

def make_electricity_data():
	
	for type_val in HOUSE_AREA:
		temp_list = []
		for area_val in HOUSE_TYPE:
			val = "%d"%(type_val/30 * area_val * 1000 /24) 
			temp_list.append(int(val)) 
		energy_data_list.append(temp_list)
	
	print 'EnergyData List Success make'
	pprint(energy_data_list)


			
def make_users():
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

def make_energy_data(user_email, energy_amount):
	DEFAULT_YEAR, DEFAULT_MOONTH, DEFAULT_DAY, DEFAULT_TIME = 2013, 12, 1, 0
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
			

def ptrol_all_users():	
	make_electricity_data()

	for house_area in xrange(5, len(HOUSE_AREA)):
		for house_type in xrange(0,len(HOUSE_TYPE)):
			for income in xrange(9,len(INCOME_TYPE)):
				for cooler_heater_type in xrange(3, len(COOLER_HEATER_TYPE)): 
					energy_amount = (energy_data_list[house_area][house_type])	
					user_email = "User%d%d%d%d"%(house_area, house_type, income, cooler_heater_type)
					
					make_energy_data(user_email, energy_amount)
					
def make_special_user():
	house_area, house_type, income, cooler_heater_type = 1, 1, 1, 1
	user_email = "User%d%d%d%d"%(house_area, house_type, income, cooler_heater_type)
	password = 'password'
	
	u = User(user_email, password)
	db.session.add(u)
	db.session.commit()

	ui = UserInfo._make_user_info_with_email(user_email, house_area, house_type, income, cooler_heater_type)
	db.session.add(ui)
	db.session.commit()

	DEFAULT_YEAR, DEFAULT_MOONTH, DEFAULT_DAY, DEFAULT_TIME = 2013, 12, 1, 0

	special_energy_set = [3, 3, 5, 4, 6, 5, 2, 9, 1, 8, 5, 7, 4, 9, 3, 5, 2, 7, 7, 6, 1, 1, 1, 1, 6, 2, 9, 5, 9, 5]

	dt = datetime(DEFAULT_YEAR, DEFAULT_MOONTH, DEFAULT_DAY, DEFAULT_TIME)
	for day_plus in xrange(1, 31):
		for time_plus in xrange(0,24):
			
			
			energy_amount = special_energy_set[day_plus-1]*200

			ed = EnergyData._make_energy_data_with_email(user_email, dt, energy_amount)
			db.session.add(ed)
			dt += timedelta(hours=1)

	db.session.commit()

def make_special_user2():
	house_area, house_type, income, cooler_heater_type = 1,1, 1, 1
	user_email = "test2"
	password = 'test2'
	
	u = User(user_email, password)
	db.session.add(u)
	db.session.commit()

	ui = UserInfo._make_user_info_with_email(user_email, house_area, house_type, income, cooler_heater_type)
	db.session.add(ui)
	db.session.commit()

	DEFAULT_YEAR, DEFAULT_MOONTH, DEFAULT_DAY, DEFAULT_TIME = 2013, 12, 1, 0

	special_energy_set = [1, 2, 4, 3, 2, 4, 3, 3, 4, 6, 5, 7, 4, 9, 3, 5, 2, 7, 7, 6, 1, 1, 1, 1, 6, 2, 9, 5, 9, 5]
	dt = datetime(DEFAULT_YEAR, DEFAULT_MOONTH, DEFAULT_DAY, DEFAULT_TIME)
	for day_plus in xrange(1, 31):
		for time_plus in xrange(0,24):
			
			
			energy_amount = special_energy_set[day_plus-1]*200

			ed = EnergyData._make_energy_data_with_email(user_email, dt, energy_amount)
			db.session.add(ed)
			dt += timedelta(hours=1)

	db.session.commit()

		

make_special_user()
make_special_user2()

make_users()
print 'Make Users : %d'%(len(User.query.all() ) )
ptrol_all_users()
