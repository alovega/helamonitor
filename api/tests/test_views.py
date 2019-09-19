# -*- coding: utf-8 -*-
"""
Tests for Api views
"""
import json

import pytest
from mixer.backend.django import mixer

from django.test import TestCase, RequestFactory

from api.views import report_event, create_incident, update_incident, get_incident, health_check, get_access_token

pytestmark = pytest.mark.django_db


class TestViews(TestCase):
	"""
	Tests for the views
	"""

	def setUp(self):
		"""Initialize the common variables for the tests"""
		self.factory = RequestFactory()

	def test_report_event(self):
		"""Tests the view for reporting an event"""
		state = mixer.blend('base.State', name = 'Active')
		system = mixer.blend('core.System', state = state)
		interface = mixer.blend('core.Interface', state = state)
		event_type = mixer.blend('base.EventType', state = state)
		request = self.factory.post(
			'api/report_event', {
				'system': system.name, 'event_type': event_type.name, 'interface': interface.name,
				'response': 'response', 'request': 'request', 'code': '404', 'description': 'Error occurred'
			}
		)
		response = report_event(request)
		response = json.loads(response.content)
		assert response.get('code') == '800.200.001', 'Should log a reported event successfully'

	def test_create_incident(self):
		"""Tests create_incident view"""
		state = mixer.blend('base.State', name = 'Active')
		system = mixer.blend('core.System', state = state)
		escalation_level = mixer.blend('base.EscalationLevel', state = state)
		mixer.blend('base.State', name = 'Scheduled')
		mixer.blend('base.IncidentType', name = 'Scheduled', state = state)
		request = self.factory.post(
			'api/create_incident', {
				'incident_type': 'Scheduled', 'system': system.name, 'escalation_level': escalation_level.name,
				'name': 'HP Upgrade', 'description': 'Scheduled Upgrade of HP to v3', 'scheduled_for': '2019-09-20',
				'scheduled_until': '2019-09-21', 'state': 'Scheduled', 'priority_level': '5'
			}
		)
		response = create_incident(request)
		response = json.loads(response.content)
		assert response.get('code') == '800.200.001', 'Should create an incident successfully'

	def test_update_incident(self):
		"""Tests update incident view"""
		state = mixer.blend('base.State', name = 'Active')
		mixer.blend('core.System', state = state)
		incident = mixer.blend('core.Incident')
		escalation_level = mixer.blend('base.EscalationLevel', state = state)
		mixer.blend('base.State', name = 'Identified')
		request = self.factory.post(
			'api/update_incident', {
				'incident_id': incident.id, 'name': 'Increased number of errors in HP', 'state': 'Identified',
				'escalation_level': escalation_level.name, 'description': 'Increased errors affecting TakeLoan',
				'priority_level': '4'
			}
		)
		response = update_incident(request)
		response = json.loads(response.content)
		assert response.get('code') == '800.200.001', 'Should update an incident successfully'

	def test_health_check(self):
		state = mixer.blend('base.State', name = 'Active')
		system = mixer.blend('core.System', name = 'github', state = state)
		endpoint_type = mixer.blend(
			'base.EndpointType', state = state, is_queried = True, name = 'healthcheck-endpoint')
		mixer.blend(
			'core.Endpoint', system = system, state = state, endpoint_type = endpoint_type,
			endpoint = 'https://github.com'
		)
		request = self.factory.get('api/health_check')
		response = health_check(request)
		response = json.loads(response.content)
		assert response.get('code') == '800.200.001', 'should return a general success code'

	def test_get_incident(self):
		state = mixer.blend('base.State', name = 'Active')
		system = mixer.blend('core.System', state = state, name = 'HP')
		incident = mixer.blend('core.Incident', state = state, system = system)
		request = self.factory.get('api/get_incident', {'system': system.name, 'incident_id': incident.id})
		response = get_incident(request)
		response = json.loads(response.content)
		bad_response = json.loads(get_incident("test").content)
		assert response.get('code') == '800.200.001', 'Should get an incident successfully'
		assert response.get('data').get('affected_system') == "HP", 'Should match the corresponding system name'
		assert bad_response.get('code') == '800.400.002', 'Should return the status code for bad request parameters'

	def test_get_access_code(self):
		"""Tests get_access code view"""
		pass
		state = mixer.blend('base.State', name = 'Active')
		app = mixer.blend('api.App', state =state)
		app_user = mixer.blend('api.AppUser', app = app)
		request = self.factory.post('api/get_access_token', {
			'client_id': app.id, 'username': app_user.user.username, 'password': app_user.user.password})
		response = get_access_token(request)
		response = json.loads(response.content)
		assert response.get('code') == '800.200.001', 'Should create an access token'
		assert response['data'].get('token') is not None, 'Should return a token'

