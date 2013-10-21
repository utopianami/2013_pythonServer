from app import db

class User(db.Model):
	__tablename__ = 'users_user'
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))

	def __init__(self, email=None, password=None):
		self.password = password;
		self.email = email

	def __repr__(self):
		return '<User %r>' % (self.email)
