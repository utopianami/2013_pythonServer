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

class UserInfo(db.Model):
	__tablename__ = "users_userinfo"
	
	id = db.Column(db.Integer, primary_key = True)
	
	user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
	house_type = db.Column(db.Integer)
	house_area = db.Column(db.Integer)
	income_type  = db.Column(db.Integer)
	cooler_heater_type = db.Column(db.Integer)

	def __init__(self, user_id, house_type, house_area, \
					income_type, cooler_heater_type):
		self.user_id = user_id
		self.house_type = house_type
		self.house_area = house_area
		self.income_type = income_type
		self.cooler_heater_type = cooler_heater_type

	@classmethod
	def _make_user_info_with_email(cls, email, house_type, house_area, \
										income_type, cooler_heater_type):
		user_id = User.query.filter_by(email=email).first().id
		return UserInfo(user_id, house_type, house_area, income_type, cooler_heater_type)

	def __repr__(self):
		return '<UserInfo> User : %d, Type %d%d%d%d'%\
			(self.user_id, self.house_type, self.house_area, self.income_type, self.cooler_heater_type)
