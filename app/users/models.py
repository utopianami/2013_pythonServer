from app import db

from app.missions.models import MissionState
from app.energy.models import EnergyData

class User(db.Model):
	__tablename__ = 'users_user'

	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))
	
	user_info = db.relationship('UserInfo', backref='user', lazy='dynamic')
	mission_state = db.relationship('MissionState', backref='user', lazy='dynamic')
	energy_data = db.relationship('EnergyData', backref='user', lazy='dynamic') 


	def __init__(self, email=None, password=None):
		self.password = password;
		self.email = email

	def __repr__(self):
		return '<User %r>' % (self.email)

	@classmethod
	def find_by_email(cls, email):
		return User.query.filter_by(email=email).first()

class UserInfo(db.Model):
	__tablename__ = "users_userinfo"
	
	id = db.Column(db.Integer, primary_key = True)
	
	user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'), unique=True)
	house_area = db.Column(db.Integer)
	house_type = db.Column(db.Integer)
	income_type  = db.Column(db.Integer)
	cooler_heater_type = db.Column(db.Integer)

	def __init__(self, user_id, house_area, house_type, \
					income_type, cooler_heater_type):
		self.user_id = user_id
		self.house_type = house_type
		self.house_area = house_area
		self.income_type = income_type
		self.cooler_heater_type = cooler_heater_type
	
	def __repr__(self):
		return '<UserInfo> User : %r[%d], Type %d%d%d%d'%\
			(self.user.email, self.user_id, self.house_area, self.house_type, self.income_type, self.cooler_heater_type)

	def get_avg_energy_data_with_date(self, start_date, end_date):
		try:
			user_infos = UserInfo.query.filter_by( house_area=self.house_area \
				,house_type=self.house_type\
				,income_type=self.income_type\
				,cooler_heater_type=self.cooler_heater_type).all()

			watt_sum = 0
			count = 0
			for user_info in user_infos:
				user_id = user_info.user.id
				eds = EnergyData.get_energy_datas_with_date(user_id, start_date, end_date)
				for ed in eds:
					count+=1
					watt_sum += ed.energy_amount
			count = (count/24)*len(user_infos)
			result = "%.2f"%(float(watt_sum)/count)
		except Exception, e:
			print e
			print user_infos
			return 0
		
		return result

	@classmethod
	def _make_user_info_with_email(cls, email, house_area, house_type, \
										income_type, cooler_heater_type):
		user_id = User.find_by_email(email).id
		return UserInfo(user_id, house_area, house_type, income_type, cooler_heater_type)

