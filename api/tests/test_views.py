# -*- coding: utf-8 -*-
"""
Tests for Api views
"""
import json

import pytest
from mixer.backend.django import mixer

from django.test import TestCase, RequestFactory

from api.views import report_event, create_incident, update_incident, get_incident

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
		assert response.get('code') == '800.200.001', 'Should log a reported incident successfully'
