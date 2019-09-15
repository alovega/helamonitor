import pytest
from mixer.backend.django import mixer

from api.backend.interfaces.incident_administration import IncidentAdministrator

pytestmark = pytest.mark.django_db


class TestIncidentLogger(object):
	"""
	Class for testing incident logger
	"""

	def test_create_incident(self):
		state = mixer.blend('base.State', name = 'Active')
		incident_type = mixer.blend('base.IncidentType', state = state, name = "Scheduled")
		system = mixer.blend('core.System', state = state)
		escalation_level = mixer.blend('base.EscalationLevel', state = state)
		investigating_state = mixer.blend('base.state', name = "Identified")
		incident = IncidentAdministrator().log_incident(
			incident_type = incident_type, system = system, escalation_level = escalation_level,
			name = 'Scheduled Maintenance', description = 'Scheduled Maintenance for Hela-Plan', priority_level = "4",
			state = 'Identified'
		)

		assert incident.get('code') == '800.200.001', "Should create an incident %s " % incident

	def test_update_incident(self):
		"""
		Tests the method for updating an incident's priority_level, resolution status or assignment
		"""
		state = mixer.blend('base.State', name = 'Active')
		log_type = mixer.blend('base.LogType', state = state)
		escalation_level = mixer.blend('base.EscalationLevel', state = state)
		investigating_state = mixer.blend('base.state', name = 'Identified')
		incident = mixer.blend('core.Incident', state = investigating_state)
		incident_update = IncidentAdministrator().update_incident(
			incident, state = investigating_state.name, escalation_level = escalation_level,
			log_type = log_type, description = "Priority Level Increased to 4 with increased error occurrence",
			priority_level = "4"
		)

		assert incident_update.get('code') == '800.200.001', "Should update the incident successfully"
