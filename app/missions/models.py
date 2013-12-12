from app import db

import base64

class Mission(db.Model):
	__tablename__ = "missions_missions"

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(30))
	contents = db.Column(db.Text())
	difficulty = db.Column(db.Integer)
	effect = db.Column(db.Integer)

	mission_state = db.relationship('MissionState', backref='mission', lazy='dynamic')

	def __init__(self, title, contents, difficulty, effect):
		self.title = base64.encodestring(title)
		self.contents = base64.encodestring(contents)
		self.difficulty = difficulty
		self.effect = effect

	def __repr__(self):
		return '<Mission %r>' % (base64.decodestring(self.title))

	def push_data(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def get_mission_list(cls):
		try:
			mission_list = []
			for mission in cls.query.all():
				mission_info = [mission.id, base64.decodestring(mission.title), base64.decodestring(mission.contents),\
					mission.difficulty, mission.effect]
				mission_list.append(mission_info)
			#mission_list.reverse()
			return mission_list

		except Exception, e:
			print e
			return []

	@classmethod
	def get_mission(cls, mission_title):
		try:
			mission_title = base64.encodestring(mission_title)
			m = cls.query.filter_by(title=mission_title).first()
			return m
		except Exception, e:
			return None

class MissionState(db.Model):
	__tablename__ = "missions_missionState"

	id = db.Column(db.Integer, primary_key = True) 
	user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
	mission_id = db.Column(db.Integer, db.ForeignKey('missions_missions.id'))
	state = db.Column(db.String(1))

	def __init__(self, user_id, mission_id, state):
		self.user_id = user_id
		self.mission_id = mission_id	
		self.state = state

	def __repr__(self):
		return '<MissionState User:%d  Mission:%d   State:%r>' % \
			(self.user.id, self.mission.id, self.state)

	def push_data(self):
		db.session.add(self)
		db.session.commit()
