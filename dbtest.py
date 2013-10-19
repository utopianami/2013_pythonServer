from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), unique = True)
	password = db.Column(db.String(120), unique = True)

	def __init__(self, email, password):
		self.email = email
		self.password = password

	def __repr__(self):
		return '<User %r>' % self.email

@app.route('/')
def home():
	return 'hello world'

@app.route('/signup/<email>/<password>')
def signUp(email, password):
	newUser = User(email, password)

	db.session.add(newUser)
	db.session.commit()

	return "email : %s, password : %s" % (newUser.email, newUser.password)

@app.route('/signin/<email>/<password>')
def printUser(userEmail, userPassword):
	user = User.query.filter_by(email = userEmail).first()
	if (user):
		if (user.password == userPassword):
			return True
		else:
			return "password is different"
	else:
		return "ID is difference"

if __name__=='__main__':
	app.run(debug = True, host='0.0.0.0', port = 7000)
