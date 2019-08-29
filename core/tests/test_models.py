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

    def test_system(self):
        system = mixer.blend('core.System')
        assert system is not None, "Should create a System model"
        assert type(str(system)) == str, "system should be a str object"

    def test_interface(self):
        interface = mixer.blend('core.Interface')
        assert interface is not None, "Should create an Interface model"
        assert type(str(interface)) == str, 'interface should be a str object'

    def test_system_credential(self):
        system_credential = mixer.blend('core.SystemCredential')
        assert system_credential is not None, 'Should create a SystemCredential model'
        assert type(str(system_credential)) == str, 'system_credential should be a str object'

    def test_system_monitor(self):
        system_monitor = mixer.blend('core.SystemMonitor')
        assert system_monitor is not None, 'Should create a SystemMonitor model'
        assert type(str(system_monitor)) == str, 'sytem_monitor should be a str object'

    def test_recipient(self):
        recipient = mixer.blend('core.Recipient')
        assert recipient is not None, 'Should create a Recipient model'
        assert type(str(recipient)) == str, 'recipient should be a str object'

    def test_system_recipient(self):
        system_recipient = mixer.blend('core.SystemRecipient')
        assert system_recipient is not None, 'should create a SystemRecipient model'
        assert type(str(system_recipient)) == str, 'system_recipient should be a str object'

    def test_event_type(self):
        event_type = mixer.blend('core.EventType')
        assert event_type is not None, 'should create an EventType model'
        assert type(str(event_type)) == str, 'event_type should be a str object'

    def test_priority_level(self):
        priority_level = mixer.blend('core.PriorityLevel')
        assert priority_level is not None, 'should create a PriorityLevel model'
        assert type(str(priority_level)) == str, 'priority_level should be a str object'

    def test_log_type(self):
        log_type = mixer.blend('core.LogType')
        assert log_type is not None, 'should create a LogType model'
        assert type(str(log_type)) == str, 'log_type should be a str object'

    def test_endpoint_type(self):
        endpoint_type = mixer.blend('core.EndpointType')
        assert endpoint_type is not None, 'should create an EndpointType model'
        assert type(str(endpoint_type)) == str, 'endpoint_type should be a str object'

    def test_occurrence(self):
        occurrence = mixer.blend('core.Occurrence')
        assert occurrence is not None, 'should create an Occurrence model'
        assert type(str(occurrence)) == str, 'occurrence should be a str object'

    def test_endpoint(self):
        endpoint = mixer.blend('core.Endpoint')
        assert endpoint is not None, 'should create an Endpoint model'
        assert type(str(endpoint)) == str, 'endpoint should be a str object'