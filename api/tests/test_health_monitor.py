import datetime

import pytest
from mixer.backend.django import mixer
from api.backend.interfaces.health_monitor import MonitorProcessor

pytestmark = pytest.mark.django_db


class TestMonitorProcessor(object):
	"""
	class for testing system_status Logger
	"""
	def test_perform_health_check(self):
		"""
		test create system status method
		:return: a system object
		"""
		state = mixer.blend('base.State', name='Active', description='active state')
		system = mixer.blend(
			'core.System', name ='Github', description='A system for saving code', code=1234, state=state
		)
		state = mixer.blend('base.State', name = 'Down')
		endpoint_type = mixer.blend('base.EndpointType', is_queried = True)
		endpoint = mixer.blend(
			'core.Endpoint', endpoint="http://127.0.0.1:8000/a", system=system, endpoint_type=endpoint_type,
			optimal_response_time = datetime.timedelta(milliseconds = 5), state = system.state
		)

		monitor_manager = MonitorProcessor().perform_health_check()
		print (monitor_manager)
		assert monitor_manager is not None, "Should log systems statuses %s " % monitor_manager

	# def test_create_event_if_status_fail(self):
	# 	"""
	# 	test create system state and event if it is a failure
	# 	:return: a system object
	# 	"""
	# 	system = mixer.blend('core.System')
	# 	interface = mixer.blend('core.Interface', system = system)
	# 	state = mixer.blend('base.State', name = 'Down')
	# 	endpoint_type = mixer.blend('base.EndpointType', is_queried =True)
	# 	endpoint = mixer.blend(
	# 		'core.Endpoint', endpoint = "http://127.0.0.1/blah/blah", system = system, endpoint_type= endpoint_type
	# 	)
	# 	escalation_level = mixer.blend('base.EscalationLevel', name='High')
	# 	event_type = mixer.blend('base.EventType', name='Critical')
	# 	kwargs = {
	# 		'response': {u'code': u'800.200.001', u'data': {u'reference': u'A0Z9Z9Z90'}},
	# 		'url': 'http://127.0.0.1/blah/blah',
	# 		'response_time': 0.212627,
	# 		'status_code': 400,
	# 		'code': '800.200.001'
	# 	}
	#
	# 	monitor_manager = MonitorProcessor().save_system_status(**kwargs)
	# 	print (monitor_manager)
	# 	assert monitor_manager is not None, "Should create a system status"
	#
	# def test_create_event_if_slow_response_time(self):
	# 	"""
	# 	test create system state and event if it is a failure
	# 	:return: a system object
	# 	"""
	# 	system = mixer.blend('core.System')
	# 	interface = mixer.blend('core.Interface', system = system)
	# 	state = mixer.blend('base.State', name = 'UP')
	# 	endpoint_type = mixer.blend('base.EndpointType', is_queried =True)
	# 	endpoint = mixer.blend(
	# 		'core.Endpoint', endpoint = "http://127.0.0.1/blah/blah", system = system, endpoint_type= endpoint_type,
	# 		optimal_response_time = datetime.timedelta(milliseconds = 5)
	# 	)
	# 	event_type = mixer.blend('base.EventType', name='Debug')
	# 	kwargs = {
	# 		'response': {u'code': u'800.200.001', u'data': {u'reference': u'A0Z9Z9Z90'}},
	# 		'url': 'http://127.0.0.1/blah/blah',
	# 		'response_time': datetime.timedelta(seconds = 0.212627),
	# 		'status_code': 200,
	# 		'code': '800.200.001'
	# 	}
	#
	# 	monitor_manager = MonitorProcessor().save_system_status(**kwargs)
	# 	print (monitor_manager)
	# 	assert monitor_manager is not None, "Should create a system status"
