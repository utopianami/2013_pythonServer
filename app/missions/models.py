from app import db

class Mission(db.Model):
	__tablename__ = "missions_missions"

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(30))
	contents = db.Column(db.Text())
	difficulty = db.Column(db.Integer)
	effect = db.Column(db.Integer)

	mission_state = db.relationship('MissionState', backref='mission', lazy='dynamic')

	def __init__(self, title, contents):
		self.title = title
		self.contents = contents

	def __repr__(self):
		return '<Mission %r>' % (self.title)


class MissionState(db.Model):
	__tablename__ = "missions_missionState"

	id = db.Column(db.Integer, primary_key = True) 
	user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
	mission_id = db.Column(db.Integer, db.ForeignKey('missions_missions.id'))
	state = db.Column(db.String(1))

	def __init__(self, title, contents):
		self.title = title
		self.contents = contents

	def __repr__(self):
		return '<MissionState User:%d  Mission:%d   State:%r>' % \
			(self.user_id, self.mission_id, self.state)
