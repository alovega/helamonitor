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
		print (monitor_manager)
		assert monitor_manager is not None, "Should log systems statuses %s "
		assert monitor_manager.get('code') == "800.200.001", "Should return a general success code"

