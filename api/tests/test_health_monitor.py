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
		state1 = mixer.blend('base.State', name='Active', description='active state')
		system = mixer.blend(
			'core.System', name ='Github', description='A system for saving code', code=1234, state=state1
		)
		state = mixer.blend('base.State', name = 'Down')
		endpoint_type = mixer.blend('base.EndpointType', is_queried = True)
		endpoint = mixer.blend(
			'core.Endpoint', endpoint="https://github.com/", system=system, endpoint_type=endpoint_type,
			optimal_response_time = datetime.timedelta(milliseconds = 5), state = system.state
		)
		event_type = mixer.blend('base.EventType', name='Critical', state=state1)

		monitor_manager = MonitorInterface.perform_health_check()
		endpoint2 = mixer.blend(
			'core.Endpoint', endpoint="url", system=system, endpoint_type=endpoint_type,
			optimal_response_time = datetime.timedelta(milliseconds = 5), state = system.state
		)
		failed_monitor = MonitorInterface.perform_health_check()
		assert monitor_manager.get('code') == "800.200.001", "Should return a general success code"
		assert failed_monitor.get('code') == "800.400.001", "Should return a general success code"

