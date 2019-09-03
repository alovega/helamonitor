import pytest
from mixer.backend.django import mixer
import requests
from api.backend.system_status import MonitorProcessor
from core.backend.services import EndpointService

pytestmark = pytest.mark.django_db


class TestMonitorProcessor(object):
	"""
	class for testing system_status Logger
	"""
	def test_create_system_status(self):
		"""
		test create system status method
		:return: a system object
		"""
		system = mixer.blend('core.System')
		state = mixer.blend('base.State', name='operational')
		response_time = 300
		endpoint = mixer.blend('core.Endpoint', endpoint="http://127.0.0.1/blah/blah")
		kwargs = {
			'response': {u'code': u'800.200.001', u'data': {u'reference': u'A0Z9Z9Z90'}},
			'url': 'http://127.0.0.1/blah/blah',
			'system': system,
			'state': state,
			'response_time': 0.212627,
			'status_code': '200',
			'code': 200
		}

		# system_monitor_fields = {
		# 	'status_code': 200,
		# 	'system': system,
		# 	'state': state,
		# 	'endpoint': endpoint,
		# 	'response_time': response_time
		# }

		monitor_manager = MonitorProcessor().save_system_status(**kwargs)
		print kwargs['system']
		print monitor_manager
		assert monitor_manager is not None, "Should create a system status"
		assert monitor_manager.system == system
