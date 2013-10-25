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
	#http://10.73.44.20:2074/users/signin/?userEmail=asdf&userPassword=pasaps
	def dispatch_request(self):

		email = request.args.get('userEmail')
		password = request.args.get('userPassword')
	
		if User.query.filter_by(email=email).first().password == password:
			return 'True'

		return 'False'


class Test(View):
	method = ['GET', 'POST']

	def dispatch_request(self):
		print 'TEST'
		return 'Hi man'	

mod.add_url_rule('/signup/', view_func=SignUp.as_view('signup_user'))
mod.add_url_rule('/signin/', view_func=SignIn.as_view('signin_user'))
mod.add_url_rule('/test/', view_func=Test.as_view('test'))


