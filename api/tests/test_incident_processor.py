import pytest
from mixer.backend.django import mixer

from api.backend.incident_processor import IncidentProcessor
from core.backend.services import EventService

pytestmark = pytest.mark.django_db


class TestIncidentProcessor(object):
	"""
	Class for testing incident processor
	"""
	def test_create_incident(self):
		incident_type = mixer.blend("base.IncidentType")
		event_type = mixer.blend('base.EventType')
		system = mixer.blend('core.System')
		state = mixer.blend('base.State')
		events = mixer.cycle(3).blend('core.Event', event_type=event_type)

		escalation_data = {
			"event_type": event_type,
			"events": EventService().filter(),
		}

		incident = IncidentProcessor().create_incident(
			"test name", "description", incident_type.name, system.name, state.name, 1, **escalation_data)

		assert incident is None, "Should create an incident %s " % incident
