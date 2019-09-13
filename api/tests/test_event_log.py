# coding=utf-8
"""
Tests for event_creation process
"""
from datetime import timedelta
import pytest
from mixer.backend.django import mixer
from api.backend.interfaces.event_log import EventLog

pytestmark = pytest.mark.django_db


class TestEventLog(object):
    """
    Class to test event creator
    """
    def test_create(self):
        """
        Tests create event method
        """
        state = mixer.blend('base.State', name="Active")
        system = mixer.blend('core.System', state=state)
        interface = mixer.blend('core.Interface', system=system, state=state)
        event_type = mixer.blend('base.EventType', state=state)
        event = EventLog.log_event(
            system=system.name, event_type=event_type.name, description = "Test Event description",
            interface = interface.name, state = state.name, code = "12345"
        )
        assert event.get('code') == '800.200.001', "Should create an event successfully"

    def test_escalate_event(self):
        """
        Tests if a created event is escalated successfully
        """
        state = mixer.blend('base.State', name='Active')
        system = mixer.blend('core.System', state=state)
        interface = mixer.blend('core.Interface', system=system, state=state)
        event_type = mixer.blend('base.EventType', state=state, name='Critical')
        escalation_level = mixer.blend("base.EscalationLevel", state=state, name='High')
        incident_type = mixer.blend('base.IncidentType', state=state, name="Realtime")
        event = mixer.blend(
            'core.Event', event_type=event_type, system=system, interface=interface, state=state,
            description='description', code='123'
        )
        escalation_rule = mixer.blend(
            "core.EscalationRule", system=system, event_type=event_type, nth_event=1,
            duration = timedelta(seconds=5), state = state, escalation_level=escalation_level
        )

        event_escalation = EventLog().escalate_event(event)
        assert event_escalation.get('code') == '800.200.001', "Should escalate event successfully"
