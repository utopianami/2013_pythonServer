from flask import Blueprint, request

from app import db
from app.users.models import User
from flask.views import View

mod = Blueprint('users', __name__, url_prefix='/users')

class SignUp(View):
	methods = ['GET', 'POST']


	def dispatch_request(self):
		print 'signUp'

		request_data = request.args

		# GET
		email = request_data['userEmail']
		password = request.args['userPassword']
		
		""" POST
		email = request.form['userEmail']
		password = request.form['userPassword']
		"""

		user = User(email=email, password=password)
		print user
		db.session.add(user)
		db.session.commit()
		
		return 'True'

class SignIn(View):
	methods = ['GET', 'POST']

	def dispatch_request(self):
		print 'signIn'

		print ruquest.args
		print request.form

		email = request.form['userEmail']
		password = request.form['userPassword']
		
		if User.query.filter_by(email=email).password == password:
			return 'True'

		return 'False'

mod.add_url_rule('/signup/', view_func=SignUp.as_view('signup_user'))
mod.add_url_rule('/signin/', view_func=SignIn.as_view('signin_user'))


