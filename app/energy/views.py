from flask import Blueprint, request

from app import db
from app.energy.models import EnergyData, RealTimeEnergyData
from flask.views import View
from datetime import datetime
import json

mod = Blueprint('energy', __name__, url_prefix='/energy')

class InsertEnergyData(View):
	methods = ['POST']

	def dispatch_request(self):
		try:
			email = request.form['userEmail']
			submit_time = request.form['submitTime']
			energy_amount = int(request.form['energyAmount'])

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
			energy_amount = int(request.form['energyAmount'])

			rt = RealTimeEnergyData(email=email, energy_amount=energy_amount)
			rt.push_data()

			return 'True'
		except Exception, e:
			print 'SetDataRecycle : %r'%e
			return 'False'

class GetDataRecycleSmartphone(View):
	
	methods = ['POST']

	def dispatch_request(self):
		try:
			
			email = request.form['userEmail']
			rt= RealTimeEnergyData.query.filter_by(email=email).all()

			if len(rt)== 0:
				return '0'
			else:
				rt.reverse()
				return '%d'%rt[0].energy_amount
			
		except Exception, e:
			print 'GetDataRecycle : %r'%e
			return 'False'

class GetMonthData(View):
	methods = ['POST']

	def dispatch_request(self):
		try:
			date = datetime.now().day
			
			email = request.form['userEmail']

			daily_datas = EnergyData.get_month_energy_datas(email)
			standby_datas = EnergyData.get_month_standby_datas(email)
			friend_dats = EnergyData.get_month_energy_datas('User7293')

			result = {'daily_datas':daily_datas, 'standby_datas':standby_datas, 'friend_dats':friend_dats}
			result = json.dumps(result)
			return result

		except Exception, e:
			print e
			return 'False'

mod.add_url_rule('/insert/', view_func=InsertEnergyData.as_view('insert_energy_data'))
mod.add_url_rule('/setrecycledata/', view_func=SetDataRecycleSmartphone.as_view('set_data_recycle_smartphone'))
mod.add_url_rule('/getrecycledata/', view_func=GetDataRecycleSmartphone.as_view('get_data_recycle_smartphone'))
mod.add_url_rule('/getmonthdata/', view_func=GetMonthData.as_view('get_month_data'))




