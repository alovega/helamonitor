import pytest
from mixer.backend.django import mixer

from api.backend.processors.incident_logger import IncidentLogger
from core.backend.services import EventService

pytestmark = pytest.mark.django_db


class TestIncidentLogger(object):
	"""
	Class for testing incident logger
	"""
	def test_create_incident(self):
		state = mixer.blend('base.State', name='Active')
		incident_type = mixer.blend('base.IncidentType', state=state)
		system = mixer.blend('core.System', state=state)

		incident = IncidentLogger().create_incident(
			incident_type = incident_type, system = system, name='Scheduled Maintenance',
			description='Scheduled Maintenance for Hela-Plan'
		)

		assert incident != {'code': '200.400.002'}, "Should create an incident %s " % incident
