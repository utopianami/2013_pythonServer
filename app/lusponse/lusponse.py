import json

class Lusponse():
	SUCCESS_CODE = 'success'
	FAIL_CODE = 'fail'

	@classmethod
	def make_response(cls, code=FAIL_CODE, message='', data=''):
		response = {'code':code, 'message':message, 'data':data}
		return json.dumps(response)

	@classmethod
	def make_success_response(cls, message='', data=''):
		return cls.make_response(cls.SUCCESS_CODE, message, data)

	@classmethod
	def make_fail_response(cls, message='', data=''):
		return cls.make_response(cls.FAIL_CODE, message, data)
