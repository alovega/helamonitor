import pytest
from mixer.backend.django import mixer
from api.backend.system_status import SystemStatusLogger

pytestmark = pytest.mark.django_db


class TestSystemStatusLogger(object):
	"""
	class for testing system_status Logger
	"""
	def test_create_system_status(self):
		"""
		test create system status method
		:return: a system object
		"""
		system = mixer.blend('core.System')
		state = mixer.blend('base.State')
		response_time = 300
		endpoint = mixer.blend('core.Endpoint')

		system_monitor_fields = {
			'system': system,
			'state': state,
			'endpoint': endpoint,
			'response_time': response_time
		}

		monitor_manager = SystemStatusLogger().create_system_status(**system_monitor_fields)
		print monitor_manager
		assert monitor_manager is not None, "Should create a system status"
		assert monitor_manager.system == system
