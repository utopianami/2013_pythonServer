from flask import Blueprint, request

from app import db
from app.energy.models import EnergyData
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
	
mod.add_url_rule('/insert/', view_func=InsertEnergyData.as_view('insert_energy_data'))




