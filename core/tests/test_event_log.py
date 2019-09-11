# coding=utf-8
"""
Tests for event_creation process
"""

import pytest
from datetime import timedelta
from mixer.backend.django import mixer
from api.backend.processors.event_log import EventLog

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
        escalation_rule = mixer.blend(
            "core.EscalationRule", system=system, event_type=event_type, nth_event=1, duration=timedelta(seconds=5),
            state=state
        )
        event_fields = {
            "description": "Test Event description",
            "interface": interface.name,
            "state": state.name,
            "code": "12345",
        }
        event_log = EventLog().log_event(event_type.name, system.name, **event_fields)
        assert event_log is not None, "Should create an event and return incident_data %s" % event_log
