from app import db
from app.missions.models import MissionState
from app.energy.models import EnergyData

class User(db.Model):
	__tablename__ = 'users_user'

	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))
	
	user_relation = db.relationship('UserRelation', backref='user', lazy='dynamic') 
	mission_state = db.relationship('MissionState', backref='user', lazy='dynamic')
	energy_data = db.relationship('EnergyData', backref='user', lazy='dynamic') 


	def __init__(self, email=None, password=None):
		self.password = password;
		self.email = email

	def __repr__(self):
		return '<User %r>' % (self.email)

class UserRelation(db.Model):
	__tablename__ = "users_relation"

	id = db.Column(db.Integer, primary_key = True)
	myself_user = db.Column(db.Integer, db.ForeignKey('users_user.id'))
	relativity_user = db.Column(db.Integer)
	state = db.Column(db.String(1))

	def __init__(self, myself_user, relativity_user, state='1'):
		self.myself_user=myself_user
		self.relativity_user=relativity_user
		self.state=state

	def __repr__(self):
		return '<UserRelation %d -> %d >'%(self.myself_user, self.relativity_user)

	@classmethod
	def relation_user(cls, src, dst, state='1'):
		src_to_dst_relation = UserRelation(src, dst)
		dst_to_src_relation = UserRelation(dst, src)
		db.session.add(src_to_dst_relation)
		db.session.add(dst_to_src_relation)
		db.session.commit()
