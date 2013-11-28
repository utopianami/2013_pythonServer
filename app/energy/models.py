from app import db

from datetime import datetime
from dateutil import parser

class EnergyData(db.Model):
	__tablename__ = "energy_energydata"

	id = db.Column(db.Integer, primary_key = True)
	
	user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
	submit_time = db.Column(db.DateTime, default=datetime.now())
	energy_amount = db.Column(db.Integer)
	
	def __init__(self, user_id,submit_time, energy_amount):
		if type(submit_time) == type(datetime.now()):
			self.submit_time = submit_time
		else:
			self.submit_time = parser.parse(submit_time)
		self.user_id = user_id
		self.energy_amount = energy_amount

	def __repr__(self):
		return '<EnergyData User %r, %d, %r >' % \
			(self.user, self.energy_amount, self.submit_time)
	
	@classmethod
	def get_energy_data_with_date(user_id, start_date, end_date):
		return EnergyData.query.filter(EnergyData.user_id==user_id, \
			EnergyData.submit_time>start_date, \
			EnergyData.submit_time<end_date \
			)	

	@classmethod
	def _make_energy_data_with_email(cls, email, submit_time, energy_amount):
		from app.users.models import User
		user_id = User.find_by_email(email).id
		return EnergyData(user_id, submit_time, energy_amount)
	
	@classmethod
	def get_energy_datas_with_date(cls, user_id, start_date, end_date):
		return EnergyData.query.filter(EnergyData.user_id==user_id). \
			filter(EnergyData.submit_time>start_date). \
			filter(EnergyData.submit_time<end_date).all()

class RealTimeEnergyData(db.Model):
	__tablename__ = "energy_realtimeenergydata"

	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120))
	energy_amount = db.Column(db.Integer)

	def __init__(self, email, energy_amount):
		self.email = email
		self.energy_amount = energy_amount

	def set_energy_amount(self,energy_amount):
		self.energy_amount = energy_amount



