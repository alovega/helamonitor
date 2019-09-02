import pytest
from mixer.backend.django import mixer

from base.backend.services import StateService, LogTypeService, EndpointTypeService, \
    EventTypeService, NotificationTypeService, EscalationLevelService, IncidentTypeService

pytestmark = pytest.mark.django_db


class TestStateService(object):
    """
    Test the State Model Services
    """

    def test_get(self):
        """
        Test  State get service
        """
        mixer.blend('base.State', name="Active")
        state = StateService().get(name="Active")
        assert state is not None, 'Should have an State object'

    def test_filter(self):
        """
        Test State filter service
        """
        mixer.cycle(3).blend('base.State')
        states = StateService().filter()
        assert len(states) == 3, 'Should have 3 State objects'

    def test_create(self):
        """
        Test State create service
        """
        state = StateService().create(name = "Active")
        assert state is not None, 'Should have a State object'
        assert state.name == "Active", "Created State name is equals to Active"

    def test_update(self):
        """
        Test State update service
        """
        state = mixer.blend('base.State')
        state = StateService().update(state.id, name = "Active")
        assert state.name == "Active", 'Should have the same name'


class TestLogTypeService(object):
    """
    Tests for LogType model Services
    """
    def test_get(self):
        """
        Test LogType get service
        """
        state = mixer.blend('base.State')
        mixer.blend('base.LogType', state=state)
        log_type = LogTypeService().get(state=state.id)
        assert log_type is not None, 'Should get a created  LogType object'

    def test_filter(self):
        """
        Test LogType filter service
        """
        mixer.cycle(3).blend('base.LogType')
        log_type = LogTypeService().filter()
        assert len(log_type) == 3, 'Should return 3 LogType objects'

    def test_create(self):
        """
        Test LogType create service
        """
        state = mixer.blend('base.State')
        log_type = LogTypeService().create(state=state, description='Incident1')
        assert log_type is not None, 'Should create a LogType Object'
        assert log_type.description == 'Incident1', ' LogType description is equals to Incident1'

    def test_update(self):
        """
        Test LogType update service
        """
        log_type = mixer.blend('base.LogType')
        log_type = LogTypeService().update(log_type.id, description='response2')
        assert log_type is not None, 'Should create a System Monitor object'
        assert log_type.description == 'response2', 'IncidentLog description has been updated to response2'


class TestEventTypeService(object):
    """
    Tests for EventType model Services
    """
    def test_get(self):
        """
        Test EventType get service
        """
        state = mixer.blend('base.State')
        mixer.blend('base.EventType', state=state)
        event_type = EventTypeService().get(state=state.id)
        assert event_type is not None, 'Should get a created EventType object'

    def test_filter(self):
        """
        Test EventType filter service
        """
        mixer.cycle(3).blend('base.EventType')
        event_type = EventTypeService().filter()
        assert len(event_type) == 3, 'Should return 3 EventType objects'

    def test_create(self):
        """
        Test EventType create service
        """
        state = mixer.blend('base.State')
        event_type = EventTypeService().create( state=state, description='Incident1')
        assert event_type is not None, 'Should create an EventType Object'
        assert event_type.description == 'Incident1', ' EventType description is equals to Incident1'

    def test_update(self):
        """
        Test IncidentLog update service
        """
        event_type = mixer.blend('base.EventType')
        event_type = EventTypeService().update(event_type.id, description='response2')
        assert event_type is not None, 'Should create an EventType object'
        assert event_type.description == 'response2', 'EventType description has been updated to response2'


class TestIncidentTypeService(object):
    """
    Test the IncidentType Model Services
    """

    def test_get(self):
        """
        Test IncidentType get service
        """
        mixer.blend('base.IncidentType', name="scheduled")
        incident_type = IncidentTypeService().get(name="scheduled")
        assert incident_type is not None, 'Should have an Incident Type object'

    def test_filter(self):
        """
        Test Incident Type filter service
        """
        mixer.cycle(3).blend('base.IncidentType')
        incident_types = IncidentTypeService().filter()
        assert len(incident_types) == 3, 'Should have 3 Incident Type objects'

    def test_create(self):
        """
        Test Incident Type create service
        """
        state = mixer.blend('base.State')
        incident_type = IncidentTypeService().create(name = "scheduled", state=state)
        assert incident_type is not None, 'Should have a Incident Type object'
        assert incident_type.name == "scheduled", "Created Incident Type name is equals to Active"

    def test_update(self):
        """
        Test Incident Type update service
        """
        state = mixer.blend('base.State')
        incident_type = mixer.blend('base.IncidentType', state=state)
        incident_type = IncidentTypeService().update(incident_type.id, name = "scheduled")
        assert incident_type.name == "scheduled", 'Should have the same name'


class TestEscalationLevelService(object):
    """
    Test the EscalationLevel Model Services
    """
    def test_get(self):
        """
        Test EscalationLevel get service
        """
        state = mixer.blend('base.State')
        mixer.blend('base.EscalationLevel', name="Critical", state=state)
        escalation_level = EscalationLevelService().get(name="Critical")
        assert escalation_level is not None, 'Should have an EscalationLevel object'

    def test_filter(self):
        """
        Test EscalationLevel filter service
        """
        mixer.cycle(3).blend('base.EscalationLevel')
        escalation_levels = EscalationLevelService().filter()
        assert len(escalation_levels) == 3, 'Should have 3 Escalation Level objects'

    def test_create(self):
        """
        Test Escalation Levels create service
        """
        state = mixer.blend('base.State')
        escalation_level = EscalationLevelService().create(name="Critical", state=state)
        assert escalation_level is not None, 'Should have an Escalation Level object'
        assert escalation_level.name == "Critical", "Created Escalation Level name is equals to Active"

    def test_update(self):
        """
        Test Escalation Level update service
        """
        escalation_level = mixer.blend('base.EscalationLevel')
        escalation_level = EscalationLevelService().update(escalation_level.id, name = "Critical")
        assert escalation_level.name == "Critical", 'Should have the same name'


class TestNotificationTypeService(object):
    """
    Test the NotificationType Model Services
    """

    def test_get(self):
        """
        Test NotificationType get service
        """
        state = mixer.blend('base.State')
        mixer.blend('base.NotificationType', name="SMS", state=state)
        notification_type = NotificationTypeService().get(name="SMS")
        assert notification_type is not None, 'Should have a NotificationType object'

    def test_filter(self):
        """
        Test NotificationType filter service
        """
        mixer.cycle(3).blend('base.NotificationType')
        notification_types = NotificationTypeService().filter()
        assert len(notification_types) == 3, 'Should have 3 NotificationType objects'

    def test_create(self):
        """
        Test NotificationType create service
        """
        state = mixer.blend('base.State')
        notification_type = NotificationTypeService().create(name="SMS", state=state)
        assert notification_type is not None, 'Should have a NotificationType object'
        assert notification_type.name == "SMS", "Created NotificationType name should be equal to Active"

    def test_update(self):
        """
        Test NotificationType update service
        """
        notification_type = mixer.blend('base.NotificationType')
        notification_type = NotificationTypeService().update(notification_type.id, name="SMS")
        assert notification_type.name == "SMS", 'Should have the same name'
