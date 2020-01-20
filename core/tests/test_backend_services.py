# -*- coding: utf-8 -*-
"""
This is the Core services tests module.
"""
import datetime
import pytest
from mixer.backend.django import mixer
from core.models import User

# noinspection SpellCheckingInspection
from core.backend.services import SystemService, InterfaceService, SystemCredentialService, \
    SystemRecipientService, SystemMonitorService, EventService, IncidentService,\
    IncidentEventService, IncidentLogService, EndpointService, EscalationRuleService


pytestmark = pytest.mark.django_db


class TestSystemService(object):
    """
    Test the System Model Services
    """

    def test_get(self):
        """
        Test System get service
        """
        mixer.blend('core.System', name = 'Helaplan')
        system = SystemService().get(name = 'Helaplan')
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
        system = SystemService().create(name = 'Helaplan', state = state, admin = admin)
        assert system is not None, 'Should have a System object'
        assert system.name == 'Helaplan', 'Created System name is equals to Helaplan'

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
        mixer.blend('core.Interface', name = "take_loan")
        interface = InterfaceService().get(name = "take_loan")
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
        mixer.blend('core.SystemMonitor', system = system)
        system_monitor = SystemMonitorService().get(system = system.id)
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
        system_monitor = SystemMonitorService().create(
            system = system, state = state, endpoint = endpoint, response_time = datetime.timedelta(milliseconds = 300))
        assert system_monitor is not None, 'Should create a SystemMonitor Object'
        assert system_monitor.response_time == datetime.timedelta(milliseconds = 300), 'Response time is equals to 300'

    def test_update(self):
        """
        Test SystemMonitor update service
        """
        system_monitor = mixer.blend('core.SystemMonitor')
        system_monitor = SystemMonitorService().update(
            system_monitor.id, response_time=datetime.timedelta(milliseconds =300)
        )
        assert system_monitor is not None, 'Should create a System Monitor object'
        assert system_monitor.response_time == datetime.timedelta(milliseconds = 300), 'Response time is equals to 300c'


class TestSystemRecipientService(object):
    """
    Tests for SystemRecipient model Services
    """
    def test_get(self):
        """
        Test SystemRecipient get service
        """
        system = mixer.blend('core.System')
        mixer.blend('core.SystemRecipient', system = system)
        system_recipient = SystemRecipientService().get(system = system.id)
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
        recipient = mixer.blend('core.User')
        escalation_level = mixer.blend('base.EscalationLevel')
        notification_type = mixer.blend('base.NotificationType')
        system_recipient = SystemRecipientService().create(
            system = system, state = state, recipient = recipient, escalation_level = escalation_level,
            notification_type = notification_type)
        assert system_recipient is not None, 'Should create a SystemMonitor Object'
        assert system_recipient.recipient == recipient, 'System Recipient is equals to the recipient created'

    def test_update(self):
        """
        Test SystemRecipient update service
        """
        system_recipient = mixer.blend('core.SystemRecipient')
        new_recipient = mixer.blend('core.User')
        system_recipient = SystemRecipientService().update(system_recipient.id, recipient = new_recipient)
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
        event_type = mixer.blend('base.EventType')
        state = mixer.blend('base.State')
        mixer.blend(
            'core.Event', system=system, interface=interface, event_type=event_type, state=state, method='Some',
            response='response', code='200'
        )
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
        event_type = mixer.blend('base.EventType')
        system = mixer.blend('core.System')
        state = mixer.blend('base.State')
        event = EventService().create(system=system, interface=interface, state=state, event_type=event_type)
        assert event is not None, 'Should create an Event Object'

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
        incident_type = mixer.blend('base.IncidentType')
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
        incident_type = mixer.blend('base.IncidentType')
        system = mixer.blend('core.System')
        state = mixer.blend('base.State')
        incident = IncidentService().create(
            system=system, incident_type=incident_type, state=state, name='maintenance', description='some',
            priority_level=1
        )
        assert incident is not None, 'Should create an Incident Object'
        assert incident.name == 'maintenance', 'Incident should have the same name'

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
        Test IncidentEvent get service
        """
        incident = mixer.blend('core.Incident')
        event = mixer.blend('core.Event')
        state = mixer.blend('base.State')
        mixer.blend('core.IncidentEvent', incident=incident, event=event, state=state)
        incident_event = IncidentEventService().get(incident=incident.id)
        assert incident_event is not None, 'Should get a created IncidentEvent object'

    def test_filter(self):
        """
        Test IncidentEvent filter service
        """
        mixer.cycle(3).blend('core.IncidentEvent')
        incident_event = IncidentEventService().filter()
        assert len(incident_event) == 3, 'Should return 3 IncidentEvent objects'

    def test_create(self):
        """
        Test IncidentEvent create service
        """
        incident = mixer.blend('core.Incident')
        event = mixer.blend('core.Event')
        state = mixer.blend('base.State')
        incident_event = IncidentEventService().create(
            incident=incident, event=event, state=state
        )
        assert incident_event is not None, 'Should create an IncidentEvent Object'
        assert incident_event.state is not None, 'IncidentEvent state is not null'

    def test_update(self):
        """
        Test IncidentEvent update service
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
        escalation_level = mixer.blend('base.EscalationLevel')
        mixer.blend(
            'core.IncidentLog', incident = incident, user = user, state = state, priority_level =
            incident.priority_level, escalation_level = escalation_level)
        incident_log = IncidentLogService().get(incident = incident.id)
        assert incident_log is not None, 'Should get a created IncidentLog object'

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
        escalation_level = mixer.blend('base.EscalationLevel')
        incident_log = IncidentLogService().create(
            incident = incident, user = user, state = state, description = 'Incident1', priority_level =
            incident.priority_level, escalation_level = escalation_level)
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
        endpoint_type = mixer.blend('base.EndpointType')
        state = mixer.blend('base.State')
        mixer.blend('core.Endpoint', system=system, endpoint_type=endpoint_type, state=state)
        incident_log = EndpointService().get(system=system.id)
        assert incident_log is not None, 'Should get a created endpoint object'

    def test_filter(self):
        """
        Test Endpoint filter service
        """
        mixer.cycle(3).blend('core.Endpoint')
        endpoint = EndpointService().filter()
        assert len(endpoint) == 3, 'Should return 3 Endpoint objects'

    def test_create(self):
        """
        Test Endpoint create service
        """
        system = mixer.blend('core.system')
        endpoint_type = mixer.blend('base.EndpointType')
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


class TestEscalationRuleService(object):
    """
    Tests for EscalationRule model Services
    """
    def test_get(self):
        """
        Test EscalationRule get service
        """
        system = mixer.blend('core.System')
        mixer.blend('core.EscalationRule', system = system, duration = datetime.timedelta(minutes = 60))
        escalation_rule = EscalationRuleService().get(system = system.id)
        assert escalation_rule is not None, 'Should get a created  EscalationRule object'

    def test_filter(self):
        """
        Test SystemRecipient filter service
        """
        mixer.cycle(3).blend('core.EscalationRule', duration=datetime.timedelta(minutes = 60))
        system_recipient = EscalationRuleService().filter()
        assert len(system_recipient) == 3, 'Should return 3 EscalationRule objects'

    def test_update(self):
        """
        Test EscalationRule create service
        """
        system = mixer.blend('core.System')
        escalation_rule = mixer.blend(
            'core.EscalationRule', duration = datetime.timedelta(minutes = 60))
        escalation_rule = EscalationRuleService().update(escalation_rule.id, system = system)
        assert escalation_rule is not None, 'Should create an EscalationRule Object'
        assert escalation_rule.system == system, 'Escalation Rule system is equals to system created'

    def test_create(self):
        """
        Test EscalationRule update service
        """
        system = mixer.blend('core.System')
        state = mixer.blend('base.State')
        event_type = mixer.blend('base.EventType')
        escalation_level = mixer.blend('base.EscalationLevel')
        escalation_rule = EscalationRuleService().create(
            system = system, state = state, event_type = event_type, escalation_level = escalation_level,
            duration = datetime.timedelta(minutes = 60), name = '10th event', nth_event = 10,
            description = 'Escalates to level High for every 10 events of type error recorded within 60 minutes'
        )
        assert escalation_rule is not None, 'Should create an Escalation Rule object'
        assert escalation_rule.system == system, ' Recipient is changed to new_recipient'
