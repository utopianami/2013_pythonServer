from flask import Blueprint, request

from app.missions.models import Mission
from flask.views import View
import json

mod = Blueprint('missions', __name__, url_prefix='/missions')

class WriteMission(View):
	methods = ['POST']

	def dispatch_request(self):
		try:
			title = request.form['missionTitle']
			contents = request.form['missionContents']
			difficulty = request.form['missionDifficuty']
			effect = request.form['missionEffect']

			effect = int(effect)
			difficulty = int(difficulty)

			m = Mission(title, contents, difficulty, effect)
			m.push_data()

		except Exception, e:
			return 'False'

class ReadMission(View):
	methods = ['POST']

	def dispatch_request(self):
		try:
			m_list = Mission.get_mission_list()
			#for mission in m_list:

		except Exception, e:
			return 'False'

mod.add_url_rule('/write/', view_func=InsertEnergyData.as_view('write_mission'))
