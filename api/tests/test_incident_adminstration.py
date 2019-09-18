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
		incident = IncidentAdministrator().log_incident(
			incident_type = incident_type, system = system, escalation_level = escalation_level,
			name = 'Scheduled Maintenance', description = 'Scheduled Maintenance for Hela-Plan', priority_level = "4",
			state = mixer.blend('base.State', name = "Scheduled").name, scheduled_for = '2019-09-19',
			scheduled_until = '2019-09-20'
		)
		failed_incident_creation = IncidentAdministrator().log_incident(
			incident_type = incident_type, system = system, escalation_level = escalation_level,
			name = 'Scheduled Maintenance', description = 'Scheduled Maintenance for Hela-Plan', priority_level = "str",
			state = mixer.blend('base.State', name = "Realtime").name
		)

		assert incident.get('code') == '800.200.001', "Should create an incident"
		assert failed_incident_creation.get('code') == '800.400.001', "Should fail creating an incident"

	def test_update_incident(self):
		"""
		Tests the update_incident method
		"""
		state = mixer.blend('base.State', name = 'Active')
		escalation_level = mixer.blend('base.EscalationLevel', state = state)
		investigating_state = mixer.blend('base.state', name = 'Identified')
		incident = mixer.blend('core.Incident', state = investigating_state)
		incident_update = IncidentAdministrator().update_incident(
			incident.id, state = investigating_state.name, escalation_level = escalation_level, name = incident.name,
			description = "Priority Level Increased to 4 with increased error occurrence", priority_level = "4"
		)
		failing_incident_update = IncidentAdministrator().update_incident(
			incident.id, state = investigating_state.name, escalation_level = escalation_level, name = incident.name,
			description = "Priority Level Increased to 4 with increased error occurrence", priority_level = "str"
		)
		assert incident_update.get('code') == '800.200.001', "Should update the incident successfully"
		assert failing_incident_update.get('code') == '800.400.001', "Should fail updating the incident"

	def test_get_incident(self):
		"""
		Tests the get incident method
		"""
		state = mixer.blend('base.State', name = 'Active')
		system = mixer.blend('core.System', state = state)
		incident = IncidentAdministrator().get_incident(incident_id = 'id', system = system.name)
		assert incident.get('code') == '800.400.001', 'Should get the incident successfully'
