# -*- coding: utf-8 -*-
"""
This is the Core services tests module.
"""
import datetime
import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User

# noinspection SpellCheckingInspection
from core.backend.services import NotificationTypeService, EscalationLevelService, IncidentTypeService, \
    SystemService, InterfaceService, SystemCredentialService, RecipientService, SystemRecipientService, \
    SystemMonitorService, EventService, IncidentService, IncidentEventService, IncidentLogService, NotificationService, \
    EndpointService, LogTypeService, PriorityLevelService, EventTypeService, OccurrenceService, EndpointTypeService

pytestmark = pytest.mark.django_db


class TestNotificationTypeService(object):
    """
    Test the NotificationType Model Services
	"""

    def test_get(self):
        """
		Test NotificationType get service
		"""
        state = mixer.blend('base.State')
        mixer.blend('core.NotificationType', name="SMS", state=state)
        notification_type = NotificationTypeService().get(name="SMS")
        assert notification_type is not None, 'Should have a NotificationType object'

    def test_filter(self):
        """
		Test NotificationType filter service
		"""
        mixer.cycle(3).blend('core.NotificationType')
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
        notification_type = mixer.blend('core.NotificationType')
        notification_type = NotificationTypeService().update(notification_type.id, name="SMS")
        assert notification_type.name == "SMS", 'Should have the same name'


class TestEscalationLevelService(object):
    """
	Test the EscalationLevel Model Services
	"""

    def test_get(self):
        """
		Test EscalationLevel get service
		"""
        state = mixer.blend('base.State')
        mixer.blend('core.EscalationLevel', name="Critical", state=state)
        escalation_level = EscalationLevelService().get(name="Critical")
        assert escalation_level is not None, 'Should have an EscalationLevel object'

    def test_filter(self):
        """
		Test EscalationLevel filter service
		"""
        mixer.cycle(3).blend('core.EscalationLevel')
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
        escalation_level = mixer.blend('core.EscalationLevel')
        escalation_level = EscalationLevelService().update(escalation_level.id, name = "Critical")
        assert escalation_level.name == "Critical", 'Should have the same name'


class TestIncidentTypeService(object):
    """
	Test the IncidentType Model Services
	"""

    def test_get(self):
        """
		Test IncidentType get service
		"""
        mixer.blend('core.IncidentType', name="scheduled")
        incident_type = IncidentTypeService().get(name="scheduled")
        assert incident_type is not None, 'Should have an Incident Type object'

    def test_filter(self):
        """
		Test Incident Type filter service
		"""
        mixer.cycle(3).blend('core.IncidentType')
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
        incident_type = mixer.blend('core.IncidentType', state=state)
        incident_type = IncidentTypeService().update(incident_type.id, name = "scheduled")
        assert incident_type.name == "scheduled", 'Should have the same name'


class TestSystemService(object):
    """
	Test the System Model Services
	"""

    def test_get(self):
        """
		Test System get service
		"""
        mixer.blend('core.System', name="Helaplan")
        system = SystemService().get(name="Helaplan")
        assert system is not None, 'Should have a System object'

    def test_filter(self):
        """
		Test System filter service
		"""
        mixer.cycle(3).blend('core.System')
        systems = SystemService().filter()
        assert len(systems) == 3, 'Should have 3 System objects'

    def test_create(self):
        """
		Test System create service
		"""
        state = mixer.blend('base.State')
        admin = mixer.blend(User)
        system = SystemService().create(name="Helaplan", state=state, admin=admin)
        assert system is not None, 'Should have a System object'
        assert system.name == "Helaplan", "Created System name is equals to Helaplan"

    def test_update(self):
        """
		Test System update service
		"""
        system = mixer.blend('core.System')
        system = SystemService().update(system.id, name = "Helaplan")
        assert system.name == "Helaplan", 'Should have the same name'


class TestInterfaceService(object):
    """
	Test the Interface Model Services
	"""

    def test_get(self):
        """
		Test Interface get service
		"""
        mixer.blend('core.Interface', name="take_loan")
        interface = InterfaceService().get(name="take_loan")
        assert interface is not None, 'Should have an Interface object'

    def test_filter(self):
        """
		Test Interface filter service
		"""
        mixer.cycle(3).blend('core.Interface')
        interfaces = InterfaceService().filter()
        assert len(interfaces) == 3, 'Should have 3 Interface objects'

    def test_create(self):
        """
		Test Interface create service
		"""
        state = mixer.blend('base.State')
        system = mixer.blend('core.System')
        interface = InterfaceService().create(name = "take_loan", state=state, system=system)
        assert interface is not None, 'Should have an Interface object'
        assert interface.name == "take_loan", "Created Interface name is equals to take_loan"

    def test_update(self):
        """
		Test Interface update service
		"""
        interface = mixer.blend('core.Interface')
        interface = InterfaceService().update(interface.id, name = "take_loan")
        assert interface.name == "take_loan", 'Should have the same name'


class TestSystemCredentialService(object):
    """
    Test SystemCredential model service
    """
    def test_get(self):
        """
        Test SystemCredential get service
        """
        mixer.blend('core.SystemCredential', username='credential')
        system_credential = SystemCredentialService().get(username='credential')
        assert system_credential is not None, 'Should create a SystemCredential object'

    def test_filter(self):
        """
        Test SystemCredential FilterService
        """
        mixer.cycle(3).blend('core.SystemCredential')
        system_credentials = SystemCredentialService().filter()
        assert len(system_credentials) == 3, 'Should filter the 3 created System Credentials'

    def test_update(self):
        """
        Test SystemCredential UpdateService
        """
        system_credential = mixer.blend('core.SystemCredential')
        system_credential = SystemCredentialService().update(system_credential.id, username='credential')
        assert system_credential is not None, 'Should create a SystemCredential object'
        assert system_credential.username == 'credential', 'Updated name is equals to credential'

    def test_create(self):
        """
        Test SystemCredential CreateService
        """
        state = mixer.blend('base.State')
        system = mixer.blend('core.System')
        system_credential = SystemCredentialService().create(
            username='credential', expires_at=datetime.datetime.now(), state=state, system=system
        )
        assert system_credential is not None, 'Should create a SystemCredential object'
        assert system_credential.username == 'credential', 'Created name is equals to credential'


class TestSystemMonitorService(object):
    """
    Tests for SystemMonitor model Services
    """
    def test_get(self):
        """
        Test SystemMonitor get service
        """
        system = mixer.blend('core.System')
        mixer.blend('core.SystemMonitor', system=system)
        system_monitor = SystemMonitorService().get(system=system.id)
        assert system_monitor is not None, 'Should create a SystemMonitor object'

    def test_filter(self):
        """
        Test SystemMonitor filter service
        """
        mixer.cycle(3).blend('core.SystemMonitor')
        system_monitors = SystemMonitorService().filter()
        assert len(system_monitors) == 3, 'Should return 3 SystemMonitor objects'

    def test_create(self):
        """
        Test SystemMonitor create service
        """
        system = mixer.blend('core.System')
        endpoint = mixer.blend('core.Endpoint')
        state = mixer.blend('base.State')
        system_monitor = SystemMonitorService().create(system=system, state=state, endpoint=endpoint, response_time=300)
        assert system_monitor is not None, 'Should create a SystemMonitor Object'
        assert system_monitor.response_time == 300, 'Response time is equals to 300'

    def test_update(self):
        """
        Test SystemMonitor update service
        """
        system_monitor = mixer.blend('core.SystemMonitor')
        system_monitor = SystemMonitorService().update(system_monitor.id, response_time=300)
        assert system_monitor is not None, 'Should create a System Monitor object'
        assert system_monitor.response_time == 300, 'Response time is equals to 300c'


class TestRecipientService(object):
    """
    Tests for Recipient model Service
    """
    def test_get(self):
        """
        Test Recipient get service
        """
        mixer.blend('core.Recipient', first_name='Victor')
        recipient = RecipientService().get(first_name='Victor')
        assert recipient is not None, 'Should return a recipient object'
        assert recipient.first_name == 'Victor', 'First name is equals to Victor'

    def test_filter(self):
        """
        Test Recipient filter service
        """
        mixer.cycle(3).blend('core.Recipient')
        recipients = RecipientService().filter()
        assert len(recipients) == 3, 'Should return 3 Recipients'

    def test_create(self):
        """
        Test Recipient Create Service
        """
        state = mixer.blend('base.State')
        recipient = RecipientService().create(first_name='Victor', last_name='Joseph', state=state)
        assert recipient is not None, 'Should create a recipient object'
        assert recipient.last_name == 'Joseph', 'Last name is equals to Joseph'

    def test_update(self):
        """
        Test Recipient update Service
        """
        recipient = mixer.blend('core.Recipient')
        recipient = RecipientService().update(recipient.id, first_name='Victor')
        assert recipient is not None, 'Should create a recipient object'
        assert recipient.first_name == 'Victor', 'First name is equals to Victor'


class TestRecipientService(object):
    """
    Tests for Recipient model Service
    """
    def test_get(self):
        """
        Test Recipient get service
        """
        mixer.blend('core.Recipient', first_name='Victor')
        recipient = RecipientService().get(first_name='Victor')
        assert recipient is not None, 'Should return a recipient object'
        assert recipient.first_name == 'Victor', 'First name is equals to Victor'

    def test_filter(self):
        """
        Test Recipient filter service
        """
        mixer.cycle(3).blend('core.Recipient')
        recipients = RecipientService().filter()
        assert len(recipients) == 3, 'Should return 3 Recipients'

    def test_create(self):
        """
        Test Recipient Create Service
        """
        state = mixer.blend('base.State')
        recipient = RecipientService().create(first_name='Victor', last_name='Joseph', state=state)
        assert recipient is not None, 'Should create a recipient object'
        assert recipient.last_name == 'Joseph', 'Last name is equals to Joseph'

    def test_update(self):
        """
        Test Recipient update Service
        """
        recipient = mixer.blend('core.Recipient')
        recipient = RecipientService().update(recipient.id, first_name='Victor')
        assert recipient is not None, 'Should create a recipient object'
        assert recipient.first_name == 'Victor', 'First name is equals to Victor'


class TestSystemRecipientService(object):
    """
    Tests for SystemRecipient model Services
    """
    def test_get(self):
        """
        Test SystemRecipient get service
        """
        system = mixer.blend('core.System')
        mixer.blend('core.SystemRecipient', system=system)
        system_recipient = SystemRecipientService().get(system=system.id)
        assert system_recipient is not None, 'Should get a created  SystemRecipient object'

    def test_filter(self):
        """
        Test SystemRecipient filter service
        """
        mixer.cycle(3).blend('core.SystemRecipient')
        system_recipient = SystemRecipientService().filter()
        assert len(system_recipient) == 3, 'Should return 3 SystemRecipient objects'

    def test_create(self):
        """
        Test SystemRecipient create service
        """
        system = mixer.blend('core.System')
        state = mixer.blend('base.State')
        recipient = mixer.blend('core.Recipient')
        escalation_level = mixer.blend('core.EscalationLevel')
        system_recipient = SystemRecipientService().create(system=system, state=state, recipient=recipient,
                                                           escalation_level=escalation_level)
        assert system_recipient is not None, 'Should create a SystemMonitor Object'
        assert system_recipient.recipient == recipient, 'System Recipient is equals to the recipient created'

    def test_update(self):
        """
        Test SystemRecipient update service
        """
        system_recipient = mixer.blend('core.SystemRecipient')
        new_recipient = mixer.blend('core.Recipient')
        system_recipient = SystemRecipientService().update(system_recipient.id, recipient= new_recipient)
        assert system_recipient is not None, 'Should create a System Recipient object'
        assert system_recipient.recipient == new_recipient, 'System Recipient is changed to new_recipient'


class TestEventService(object):
    """
    Tests for Event model Services
    """
    def test_get(self):
        """
        Test Event get service
        """
        system = mixer.blend('core.System')
        interface = mixer.blend('core.Interface')
        event_type = mixer.blend('core.EventType')
        state = mixer.blend('base.State')
        mixer.blend('core.Event', system=system, interface=interface, event_type=event_type,
                    state=state, method='Some', response='response', code='234', response_time=111)
        event = EventService().get(system=system.id)
        assert event is not None, 'Should get a created Event object'

    def test_filter(self):
        """
        Test Event filter service
        """
        mixer.cycle(3).blend('core.Event')
        event = EventService().filter()
        assert len(event) == 3, 'Should return 3 SystemMonitor objects'

    def test_create(self):
        """
        Test Event create service
        """
        interface = mixer.blend('core.Interface')
        event_type = mixer.blend('core.EventType')
        system = mixer.blend('core.System')
        state = mixer.blend('base.State')
        event = EventService().create(system=system, interface=interface, state=state, event_type=event_type)
        assert event is not None, 'Should create an Event Object'
        assert event.code is not None, 'Event Created should have a code'

    def test_update(self):
        """
        Test Event update service
        """
        event = mixer.blend('core.Event')
        event = EventService().update(event.id, response='response2')
        assert event is not None, 'Should create a System Monitor object'
        assert event.response == 'response2', 'Response  is equals to response2'


class TestIncidentService(object):
    """
    Tests for Incident model Services
    """
    def test_get(self):
        """
        Test Incident get service
        """
        system = mixer.blend('core.System')
        incident_type = mixer.blend('core.IncidentType')
        state = mixer.blend('base.State')
        mixer.blend('core.Incident', system=system, incident_type=incident_type, state=state)
        incident = IncidentService().get(system=system.id)
        assert incident is not None, 'Should get a created an Incident object'

    def test_filter(self):
        """
        Test Incident filter service
        """
        mixer.cycle(3).blend('core.Incident')
        incident = IncidentService().filter()
        assert len(incident) == 3, 'Should return 3 Incident objects'

    def test_create(self):
        """
        Test Incident create service
        """
        incident_type = mixer.blend('core.IncidentType')
        priority_level = mixer.blend('core.PriorityLevel')
        system = mixer.blend('core.System')
        state = mixer.blend('base.State')
        incident = IncidentService().create(system=system, incident_type=incident_type, state=state, name='maintenance',
        description='some', priority_level=priority_level)
        assert incident is not None, 'Should create an Incident Object'
        assert incident.description is not None, 'Incident has a description'

    def test_update(self):
        """
        Test Incident update service
        """
        incident = mixer.blend('core.Incident')
        incident = IncidentService().update(incident.id, description='some')
        assert incident is not None, 'Should create an Incident object'
        assert incident.description == 'some', 'Incident description  is equals to some'


class TestIncidentEventService(object):
    """
    Tests for IncidentEvent model Services
    """
    def test_get(self):
        """
        Test SystemMonitor get service
        """
        incident = mixer.blend('core.Incident')
        event = mixer.blend('core.Event')
        priority_level = mixer.blend('core.PriorityLevel')
        state = mixer.blend('base.State')
        mixer.blend('core.IncidentEvent', incident=incident, event=event, state=state, priority_level=priority_level)
        incident_event = IncidentEventService().get(incident=incident.id)
        assert incident_event is not None, 'Should get a created IncidentEvent object'

    def test_filter(self):
        """
        Test SystemMonitor filter service
        """
        mixer.cycle(3).blend('core.IncidentEvent')
        incident_event = IncidentEventService().filter()
        assert len(incident_event) == 3, 'Should return 3 IncidentEvent objects'

    def test_create(self):
        """
        Test SystemMonitor create service
        """
        incident = mixer.blend('core.Incident')
        event = mixer.blend('core.Event')
        state = mixer.blend('base.State')
        log_type = mixer.blend('core.LogType')
        priority_level = mixer.blend('core.PriorityLevel')
        incident_event = IncidentEventService().create(incident=incident, event=event, state=state,
                                                       priority_level=priority_level, log_type=log_type)
        assert incident_event is not None, 'Should create an IncidentEvent Object'
        assert incident_event.state is not None, 'IncidentEvent state is not null'

    def test_update(self):
        """
        Test SystemMonitor update service
        """
        event = mixer.blend('core.Event')
        incident_event = mixer.blend('core.IncidentEvent')
        incident_event = IncidentEventService().update(incident_event.id, event=event)
        assert incident_event is not None, 'Should create an IncidentEvent object'
        assert incident_event.event == event, 'Event  is updated  to  the created event'


class TestIncidentLogService(object):
    """
    Tests for IncidentLog model Services
    """
    def test_get(self):
        """
        Test IncidentLog get service
        """
        incident = mixer.blend('core.Incident')
        user = mixer.blend(User)
        state = mixer.blend('base.State')
        mixer.blend('core.IncidentLog', incident=incident, user=user,state=state)
        incident_log = IncidentLogService().get(incident=incident.id)
        assert incident_log is not None, 'Should get a created IncidentLog object'
        return user

    def test_filter(self):
        """
        Test IncidentLog filter service
        """
        mixer.cycle(3).blend('core.IncidentLog')
        incident_log = IncidentLogService().filter()
        assert len(incident_log) == 3, 'Should return 3 IncidentLog objects'

    def test_create(self):
        """
        Test IncidentLog create service
        """
        incident = mixer.blend('core.Incident')
        user = mixer.blend(User)
        state = mixer.blend('base.State')
        incident_log = IncidentLogService().create(incident=incident, user=user, state=state, description='Incident1')
        assert incident_log is not None, 'Should create an IncidentLog Object'
        assert incident_log.description == 'Incident1', ' IncidentLog description is equals to Incident1'

    def test_update(self):
        """
        Test IncidentLog update service
        """
        incident_log = mixer.blend('core.IncidentLog')
        incident_log = IncidentLogService().update(incident_log.id, description='response2')
        assert incident_log is not None, 'Should create a System Monitor object'
        assert incident_log.description == 'response2', 'IncidentLog description has been updated to response2'


class TestEndpointService(object):
    """
    Tests for Endpoint model Services
    """
    def test_get(self):
        """
        Test Endpoint get service
        """
        system = mixer.blend('core.System')
        endpoint_type = mixer.blend('core.EndpointType')
        state = mixer.blend('base.State')
        mixer.blend('core.Endpoint', system=system, endpoint_type=endpoint_type, state=state)
        incident_log = EndpointService().get(system=system.id)
        assert incident_log is not None, 'Should get a created endpoint object'

    def test_filter(self):
        """
        Test Endpiont filter service
        """
        mixer.cycle(3).blend('core.Endpoint')
        endpoint = EndpointService().filter()
        assert len(endpoint) == 3, 'Should return 3 Endpoint objects'

    def test_create(self):
        """
        Test Endpoint create service
        """
        system = mixer.blend('core.system')
        endpoint_type = mixer.blend('core.EndpointType')
        state = mixer.blend('base.State')
        endpoint = EndpointService().create(system=system, endpoint_type=endpoint_type, state=state,
                                                   description='Incident1')
        assert endpoint is not None, 'Should create an Endpoint Object'
        assert endpoint.description == 'Incident1', ' Endpoint description is equals to Incident1'

    def test_update(self):
        """
        Test Endpoint update service
        """
        endpoint = mixer.blend('core.Endpoint')
        endpoint = EndpointService().update(endpoint.id, description='response2')
        assert endpoint is not None, 'Should create a System Monitor object'
        assert endpoint.description == 'response2', 'IncidentLog description has been updated to response2'


class PriorityLevelService(object):
    """
    Tests for PriorityLevel model Services
    """
    def test_get(self):
        """
        Test PriorityLevel get service
        """
        state = mixer.blend('base.State')
        mixer.blend('core.PriorityLevel', state=state)
        priority_level = PriorityLevelService().get(state=state.id)
        assert priority_level is not None, 'Should get a created PriorityLevel object'

    def test_filter(self):
        """
        Test PriorityLevel filter service
        """
        mixer.cycle(3).blend('core.PriorityLevel')
        incident_log = PriorityLevelService().filter()
        assert len(incident_log) == 3, 'Should return 3 PriorityLevel objects'

    def test_create(self):
        """
        Test PriorityLevel create service
        """
        state = mixer.blend('base.State')
        priority_level = PriorityLevelService().create(state=state, description='Incident1')
        assert priority_level is not None, 'Should create a PriorityLevel Object'
        assert priority_level.description == 'Incident1', ' PriorityLevel description is equals to Incident1'

    def test_update(self):
        """
        Test PriorityLevel update service
        """
        priority_level = mixer.blend('core.PriorityLevel')
        priority_level = PriorityLevelService().update(priority_level.id, description='response2')
        assert priority_level is not None, 'Should create a System Monitor object'
        assert priority_level.description == 'response2', 'IncidentLog description has been updated to response2'


class TestLogTypeService(object):
    """
    Tests for LogType model Services
    """
    def test_get(self):
        """
        Test LogType get service
        """
        state = mixer.blend('base.State')
        mixer.blend('core.LogType', state=state)
        log_type = LogTypeService().get(state=state.id)
        assert log_type is not None, 'Should get a created  LogType object'

    def test_filter(self):
        """
        Test LogType filter service
        """
        mixer.cycle(3).blend('core.LogType')
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
        log_type = mixer.blend('core.LogType')
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
        mixer.blend('core.EventType', state=state)
        event_type = EventTypeService().get(state=state.id)
        assert event_type is not None, 'Should get a created EventType object'

    def test_filter(self):
        """
        Test EventType filter service
        """
        mixer.cycle(3).blend('core.EventType')
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
        event_type = mixer.blend('core.EventType')
        event_type = EventTypeService().update(event_type.id, description='response2')
        assert event_type is not None, 'Should create an EventType object'
        assert event_type.description == 'response2', 'EventType description has been updated to response2'


class TestOccurrenceService(object):
    """
    Tests for occurrence model Services
    """
    def test_get(self):
        """
        Test Occurrence get service
        """
        state = mixer.blend('base.State')
        mixer.blend('core.Occurrence', state=state)
        occurrence = OccurrenceService().get(state=state.id)
        assert occurrence is not None, 'Should get a created occurrence object'

    def test_filter(self):
        """
        Test Occurrence filter service
        """
        mixer.cycle(3).blend('core.Occurrence')
        occurrence = OccurrenceService().filter()
        assert len(occurrence) == 3, 'Should return 3 Occurrence objects'

    def test_create(self):
        """
        Test Occurrence create service
        """
        state = mixer.blend('base.State')
        occurrence = EventTypeService().create( state=state, description='Incident1')
        assert occurrence is not None, 'Should create an Occurrence Object'
        assert occurrence.description == 'Incident1', ' Occurrence description is equals to Incident1'

    def test_update(self):
        """
        Test Occurrence update service
        """
        occurrence = mixer.blend('core.Occurrence')
        occurrence = OccurrenceService().update(occurrence.id, description='response2')
        assert occurrence is not None, 'Should create an Occurrence object'
        assert occurrence.description == 'response2', 'Occurrence description has been updated to response2'

