from app import db

from datetime import datetime, timedelta
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
	submit_time = db.Column(db.DateTime, default=datetime.now())
	energy_amount = db.Column(db.Integer)

	def __init__(self, email, energy_amount):
		self.email = email
		self.energy_amount = energy_amount
	
	def __repr__(self):
		return '<RealTimeEnergyData %r, %d, %r >' % \
			(self.email, self.energy_amount, self.submit_time)

	def push_data(self):
		try:
			recently_time = RealTimeEnergyData.get_recently_data_time(self.email)
			if datetime.now().hour != recently_time.hour:
				hour = datetime.now().hour
				year = datetime.now().year
				month = datetime.now().month
				day = datetime.now().day
				time = datetime(year, month, day, hour)

				energy_amount = RealTimeEnergyData.get_energy_amount_for_hour(self.email, time)
				print 'energy_amount : %r'%energy_amount
				e = EnergyData._make_energy_data_with_email(self.email, time, energy_amount)

				db.session.add(e)
				db.session.commit()

			db.session.add(self)
			db.session.commit()
		except Exception, e:
			print 'push_data : %r'%e

	@classmethod
	def get_recently_data_time(cls, email):
		try:
			datas = cls.query.filter_by(email=email).all()
			datas.reverse()
			return datas[0].submit_time
		except Exception, e: 
			return datetime.now()

	@classmethod
	def get_energy_amount_for_hour(cls, email, time):
		try:
			energy_amount_sum = 0

			start_time = time - timedelta(hours=1)
			end_time = time
			data_list = RealTimeEnergyData.query.filter(RealTimeEnergyData.email==email). \
				filter(RealTimeEnergyData.submit_time>start_time). \
				filter(RealTimeEnergyData.submit_time<end_time).all()

			for data in data_list:
				energy_amount_sum+=data.energy_amount
			result = energy_amount_sum/len(data_list)

			return result
		except Exception, e:
			print 'get_energy_amount_for_hour : %r'%e
			return 0
