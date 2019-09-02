# coding=utf-8
"""
Tests for models in core module
"""

import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestBaseModels(object):
    """
    Test class for core models
    """
    def test_state(self):
        state = mixer.blend("base.State")
        assert state is not None, "Should create a State model"
        assert type(str(state)) == str, "State should be a str object"

    def test_event_type(self):
        event_type = mixer.blend('base.EventType')
        assert event_type is not None, 'should create an EventType model'
        assert type(str(event_type)) == str, 'event_type should be a str object'

    def test_priority_level(self):
        priority_level = mixer.blend('base.PriorityLevel')
        assert priority_level is not None, 'should create a PriorityLevel model'
        assert type(str(priority_level)) == str, 'priority_level should be a str object'

    def test_log_type(self):
        log_type = mixer.blend('base.LogType')
        assert log_type is not None, 'should create a LogType model'
        assert type(str(log_type)) == str, 'log_type should be a str object'

    def test_endpoint_type(self):
        endpoint_type = mixer.blend('base.EndpointType')
        assert endpoint_type is not None, 'should create an EndpointType model'
        assert type(str(endpoint_type)) == str, 'endpoint_type should be a str object'

    def test_occurrence(self):
        occurrence = mixer.blend('base.Occurrence')
        assert occurrence is not None, 'should create an Occurrence model'
        assert type(str(occurrence)) == str, 'occurrence should be a str object'

    def test_notification_type(self):
        notification_type = mixer.blend("base.NotificationType")
        assert notification_type is not None, "Should create a NotificationType model"
        assert type(str(notification_type)) == str, "NotificationType should be a str object"

    def test_escalation_level(self):
        escalation_level = mixer.blend("base.EscalationLevel")
        assert escalation_level is not None, "Should create an EscalationLevel model"
        assert type(str(escalation_level)) == str, "EscalationLevel should be a str object"

    def test_incident_type(self):
        incident_type = mixer.blend("base.IncidentType")
        assert incident_type is not None, "Should create an IncidentType model"
        assert type(str(incident_type)) == str, "IncidentType should be a str object"