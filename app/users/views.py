from flask import Blueprint, request

from app import db
from app.users.models import User, UserInfo
from flask.views import View
from sqlalchemy.exc import IntegrityError

from datetime import datetime

mod = Blueprint('users', __name__, url_prefix='/users')

class SignUp(View):
	methods = ['POST']

	def dispatch_request(self):
		try:
			email = request.form['userEmail']
			password = request.form['userPassword']
			
			if(User.query.filter_by(email=email).first() ):
				raise Exception('AleadyUseEmailException')

			user = User(email=email, password=password)
			db.session.add(user)
			db.session.commit()

		except Exception, e:
			#print e
			return 'False'
		
		return 'True'

class SignIn(View):
	methods = ['POST']

	def dispatch_request(self):
		try:
			email = request.form['userEmail']
			password = request.form['userPassword']

			user = User.query.filter_by(email=email).first()
			if user == None:
				raise Exception('NotExistUser')
			if user.password == password:
				return 'True'
	
		except Exception, e:
			#print e
			return 'False'
		
		return 'False'

class InfoSetUp(View):
	methods = ['POST']

	def dispatch_request(self):
		try:
			email = request.form['userEmail']
			house_type = int(request.form['houseType'])
			house_area = int(request.form['houseArea'])
			income_type  = int(request.form['incomeType'])
			cooler_heater_type = int(request.form['coolerHeaterType'])

			ui = UserInfo._make_user_info_with_email(email, house_area, house_type, \
				income_type, cooler_heater_type)

			db.session.add(ui)
			db.session.commit()

			user_info = UserInfo.query.filter_by(house_area=house_area, house_type=house_type\
				, income_type=income_type, cooler_heater_type=cooler_heater_type).first()
			avg_data = user_info.get_avg_energy_data_with_date(datetime(2013, 11, 1, 1), datetime(2013, 11, 31, 23, 59, 59))

			return str(avg_data)

		except IntegrityError, e:
			print 'Aleady Exist User Info for %r'%email
			return '10'
			
		except Exception, e:
			print 'Set Up Error  : %r '%e
			return 'False'

		return 'False'

class GoalSetUp(View):
	methods = ['POST']

	def dispatch_request(self):
		try:
			email = request.form['userEmail']
			goal = request.form['goalData']
			
			user = User.query.filter_by(email=email).first()

			user.user_info.first().goal = float(goal)

			return 'True'

		except Exception, e:
			
			return 'False'

mod.add_url_rule('/signup/', view_func=SignUp.as_view('signup_user'))
mod.add_url_rule('/signin/', view_func=SignIn.as_view('signin_user'))
mod.add_url_rule('/setup/', view_func=InfoSetUp.as_view('setup_user'))
mod.add_url_rule('/goal/', view_func=GoalSetUp.as_view('goal_user'))

