#-*- coding:utf8 -*-
from flask import Blueprint, request

from app.missions.models import Mission, MissionState
from app.users.models import User
from flask.views import View
from app.lusponse.lusponse import Lusponse


mod = Blueprint('missions', __name__, url_prefix='/missions')

class WriteMission(View):
	methods = ['POST']

	def dispatch_request(self):
		try:
			user = request.form['userEmail']
			title = request.form['missionTitle'].encode('utf-8')
			contents = request.form['missionContents'].encode('utf-8')
			difficulty = request.form['missionDifficulty']
			effect = request.form['missionEffect']

			effect = int(effect)
			difficulty = int(difficulty)

			m = Mission(title, contents, difficulty, effect)
			m.push_data()

			m = Mission.get_mission(title)
			u = User.find_by_email(user)
		
			ms = MissionState(u.id, m.id, '1')
			ms.push_data()

			response = Lusponse.make_success_response('success make missions', '')
			return response

		except Exception, e:
			response = Lusponse.make_fail_response('fail make missions', "%r"%e)
			return response

class ReadMission(View):
	methods = ['POST']

	def dispatch_request(self):
		try:
			m_list = Mission.get_mission_list()
			
			response = Lusponse.make_success_response('success return missions', m_list)
			return response

		except Exception, e:
			response = Lusponse.make_fail_response('success return missions', "%r"%e)
			return response

mod.add_url_rule('/write/', view_func=WriteMission.as_view('write_mission'))
mod.add_url_rule('/read/', view_func=ReadMission.as_view('read_mission'))
