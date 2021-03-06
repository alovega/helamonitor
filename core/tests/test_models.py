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
        assert type(str(system_monitor)) == str, 'system_monitor should be a str object'

    def test_system_recipient(self):
        system_recipient = mixer.blend('core.SystemRecipient')
        assert system_recipient is not None, 'should create a SystemRecipient model'
        assert type(str(system_recipient)) == str, 'system_recipient should be a str object'

    def test_endpoint(self):
        endpoint = mixer.blend('core.Endpoint')
        assert endpoint is not None, 'should create an Endpoint model'
        assert type(str(endpoint)) == str, 'endpoint should be a str object'
