from flask import Blueprint, request

from app import db
from app.users.models import User
from flask.views import View

mod = Blueprint('users', __name__, url_prefix='/users')

class SignUp(View):
	methods = ['GET', 'POST']

	def dispatch_request(self):
		email = request.form['userEmail']
		password = request.form['userPassword']

		user = User(email=email, password=password)
		db.session.add(user)
		db.session.commit()
		

class SignIn(View):
	methods = ['GET', 'POST']

	def dispatch_request(self):
		email = request.form['userEmail']
		password = request.form['userPassword']
		
		if User.query.filter_by(email=email).password == password:
			return 'True'

		return 'False'

mod.add_url_rule('/signup/', view_func=SignUp.as_view('signup_user'))
mod.add_url_rule('/signin/', view_func=SignIn.as_view('signin_user'))


