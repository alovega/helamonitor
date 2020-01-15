import datetime

import pytest
from mixer.backend.django import mixer
from api.backend.interfaces.health_monitor import MonitorInterface

pytestmark = pytest.mark.django_db


class TestMonitorInterface(object):
	"""
	class for testing system_status Logger
	"""
	def test_perform_health_check(self):
		"""
		test create system status method
		:return: a system object
		"""
		state = mixer.blend('base.State', name='Operational', description='active state')
		default = mixer.blend('base.State', name = 'Active', description = 'active state')
		system = mixer.blend(
			'core.System', name ='Github', description='A system for saving code', code=1234, state = default
		)
		endpoint_type = mixer.blend('base.EndpointType', is_queried = True)
		mixer.blend(
			'core.Endpoint', url="http://127.0.0.1:8000/api/get_systems/", system = system,
			endpoint_type = endpoint_type,
			optimal_response_time = datetime.timedelta(milliseconds = 10), state = system.state
		)
		mixer.blend('base.State', name = 'Major Outage')
		mixer.blend('base.EventType', name = 'Critical', state = default)
		monitor_manager = MonitorInterface.perform_health_check()
		mixer.blend(
			'core.Endpoint', url = "url", system = system, endpoint_type = endpoint_type,
			optimal_response_time = datetime.timedelta(milliseconds = 5), state = system.state
		)
		failed_monitor = MonitorInterface.perform_health_check()
		# assert monitor_manager.get('data').get('systems')[0] == '100.200.001'
		assert monitor_manager.get('code') == '800.200.001', "Should return a general success code"
		assert failed_monitor.get('code') == '800.400.001', "Should return a general error code"
