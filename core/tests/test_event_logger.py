# coding=utf-8
"""
Tests for event_creation process
"""

import pytest
from mixer.backend.django import mixer
from api.backend.event_logger import EventLogger

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
        interface = mixer.blend('core.Interface')
        event_type = mixer.blend('base.EventType')
        state = mixer.blend('base.State')
        event_fields = {
            "description": "Test Event description",
            "interface": interface,
            "system": system,
            "event_type": event_type,
            "state": state,
            "code": "12345",
            "response_time": 100
        }
        event_manager = EventLogger(**event_fields)
        assert event_manager is not None, "Should create an event"
        assert event_manager.event.description == "Test Event description", "Description equals Test Event description"

