import pytest
from datetime import timedelta

from django.utils import timezone
from mixer.backend.django import mixer

from api.backend.interfaces.dashboard_administration import DashboardAdministration

pytestmark = pytest.mark.django_db


class TestDashboardAdministration(object):
	"""Class for testing dashboard administration"""
	def test_get_dashboard_widgets_data(self):
		"""Tests get_dashboard_widgets_data method"""
		state = mixer.blend('base.State', name = 'Active')
		system = mixer.blend('core.System', name = 'HP', state = state)
		incident = mixer.cycle(4).blend(
			'core.incident', incident_type = mixer.blend('base.IncidentType', name = 'Realtime'))
		widget_data = DashboardAdministration().dashboard_widgets_data(system.id)

		assert widget_data.get('code') == '800.200.001', 'Should get widgets data'

	def test_get_error_rate(self):
		"""Tests get_error_rate method"""
		state = mixer.blend('base.State', name = 'Active')
		event_type = mixer.blend('base.EventType', name = 'Error', state = state)
		system = mixer.blend('core.System', name = 'HP', state = state)
		start_date = timezone.now()
		end_date = start_date - timedelta(days = 1)
		events = mixer.cycle(3).blend('core.Event', event_type = event_type)
		error_rate = DashboardAdministration().get_error_rate(system.id, start_date.isoformat(), end_date.isoformat())

		assert error_rate.get('code') == '800.200.001', 'Should retrieve system error rates'
