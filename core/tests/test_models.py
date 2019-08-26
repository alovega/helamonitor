# coding=utf-8
"""
Tests for models in core module
"""

import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestCoreModels(object):
    """
    Test class for core models
    """
    def test_state(self):
        state = mixer.blend("core.State")
        assert state is not None, "Should create a State model"
        assert type(str(state)) == str, "State should be a str object"

    def test_notification_type(self):
        notification_type = mixer.blend("core.NotificationType")
        assert notification_type is not None, "Should create a NotificationType model"
        assert type(str(notification_type)) == str, "NotificationType should be a str object"

    def test_escalation_level(self):
        escalation_level = mixer.blend("core.EscalationLevel")
        assert escalation_level is not None, "Should create an EscalationLevel model"
        assert type(str(escalation_level)) == str, "EscalationLevel should be a str object"

    def test_incident_type(self):
        incident_type = mixer.blend("core.IncidentType")
        assert incident_type is not None, "Should create an IncidentType model"
        assert type(str(incident_type)) == str, "IncidentType should be a str object"

    def test_event(self):
        event = mixer.blend("core.Event")
        assert event is not None, "Should create an Event model"
        assert type(str(event)) == str, "Event Should be a str object"

    def test_incident(self):
        incident = mixer.blend("core.Incident")
        assert incident is not None, "Should create an Incident"
        assert type(str(incident)) == str, "Incident Should be a str object"

    def test_incident_log(self):
        incident_log = mixer.blend("core.IncidentLog")
        assert incident_log is not None, "Should create an IncidentLog"
        assert type(str(incident_log)) == str, "Incident Log should be a str object"

    def test_notification(self):
        notification = mixer.blend("core.Notification")
        assert notification is not None, "Should create a Notification"
        assert type(str(notification)) == str, "Notification should be a str object"

