from flask import Blueprint, request

from app import db
from app.energy.models import EnergyData, RealTimeEnergyData
from flask.views import View
from datetime import datetime

mod = Blueprint('energy', __name__, url_prefix='/energy')

class InsertEnergyData(View):
	methods = ['POST']

	def dispatch_request(self):
		try:
			email = request.form['userEmail']
			submit_time = request.form['submitTime']
			energy_amount = request.form['energyAmount']

			energy = EnergyData._make_energy_data_with_email(email, submit_time, energy_amount)
			
			db.session.add(energy)
			db.session.commit()

			return 'True'

		except Exception, e:

			print e
			return 'False'

		return 'False'

class SetDataRecycleSmartphone(View):

	methods = ['POST']

	def dispatch_request(self):
		try:
			email = request.form['userEmail']
			energy_amount = request.form['energyAmount']

			if RealTimeEnergyData.query.filter_by(email=email).count() == 0:
				rt = RealTimeEnergyData(email=email, energy_amount=energy_amount)
				db.session.add(rt)
				db.session.commit()

			else:
				rt = RealTimeEnergyData.query.filter_by(email=email).first()
				rt.energy_amount = energy_amount

			return 'True'
		except Exception, e:
			return 'False'

class GetDataRecycleSmartphone(View):
	
	methods = ['POST']

	def dispatch_request(self):
		try:
			
			email = request.form['userEmail']
			rt= RealTimeEnergyData.query.filter_by(email=email)
			
			if rt.count() == 0:
				return '0'
			else:
				return '%d'%rt.first().energy_amount
			
		except Exception, e:
			return 'False'

mod.add_url_rule('/insert/', view_func=InsertEnergyData.as_view('insert_energy_data'))
mod.add_url_rule('/setrecycledata/', view_func=SetDataRecycleSmartphone.as_view('set_data_recycle_smartphone'))
mod.add_url_rule('/getrecycledata/', view_func=GetDataRecycleSmartphone.as_view('get_data_recycle_smartphone'))




