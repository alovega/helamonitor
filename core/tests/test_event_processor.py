# coding=utf-8
"""
Tests for event_creation process
"""

import pytest
from datetime import timedelta
from mixer.backend.django import mixer
from api.backend.event_processor import EventProcessor

pytestmark = pytest.mark.django_db


class TestEventLogger(object):
    """
    Class to test event creator
    """
    def test_create(self):
        """
        Tests create event method
        """
        system = mixer.blend('core.System')
        interface = mixer.blend('core.Interface', system=system)
        event_type = mixer.blend('base.EventType')
        state = mixer.blend('base.State')
        escalation_rule = mixer.blend(
            "core.EscalationRule", system=system, event_type=event_type, nth_event=1, duration=timedelta(seconds=5)
        )
        event_fields = {
            "description": "Test Event description",
            "interface": interface.name,
            "system": system.name,
            "event_type": event_type.name,
            "state": state.name,
            "code": "12345",
        }
        event_log = EventProcessor().log_event(**event_fields)
        assert event_log is not None, "Should create an event and return incident_data"
