from app import db

class EnergyData(db.Model):
	__tablename__ = "energy_energydata"

	id = db.Column(db.Integer, primary_key = True)
	
	submit_time = db.Column(db.DateTime())
	energy_amount = db.Column(db.Integer())
	user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))

	def __init__(self, submit_time, energy_amount, user_id):
		self.submit_time = submit_time
		self.energy_amount = energy_amount
		self.user = user_id

	def __repr__(self):
		return '<EnergyData User %r, %d, %r >' % \
			(self.user, self.energy_amount, self.submit_time)