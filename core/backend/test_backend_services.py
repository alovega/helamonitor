# -*- coding: utf-8 -*-
"""
This is the Core services tests module.
"""
import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User

# noinspection SpellCheckingInspection
from core.backend.services import StateService, NotificationTypeService, EscalationLevelService, IncidentTypeService, \
    SystemService, InterfaceService, SystemCredentialService, RecipientService, SystemRecipientService, \
    SystemMonitorService, EventService, IncidentService, IncidentEventService, IncidentLogService, NotificationService

pytestmark = pytest.mark.django_db


class TestStateService(object):
    """
	Test the State Model Services
	"""

    def test_get(self):
        """
		Test State get service
		"""
        mixer.blend('core.State', name="Active")
        state = StateService().get(name="Active")
        assert state is not None, 'Should have an State object'

    def test_filter(self):
        """
		Test State filter service
		"""
        mixer.cycle(3).blend('core.State')
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
        state = mixer.blend('core.State')
        state = StateService().update(state.id, name = "Active")
        assert state.name == "Active", 'Should have the same name'


class TestNotificationTypeService(object):
    """
	Test the NotificationType Model Services
	"""

    def test_get(self):
        """
		Test NotificationType get service
		"""
        state = mixer.blend('core.State')
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
        state = mixer.blend('core.State')
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
        state = mixer.blend('core.State')
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
        state = mixer.blend('core.State')
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
        state = mixer.blend('core.State')
        incident_type = IncidentTypeService().create(name = "scheduled", state=state)
        assert incident_type is not None, 'Should have a Incident Type object'
        assert incident_type.name == "scheduled", "Created Incident Type name is equals to Active"

    def test_update(self):
        """
		Test Incident Type update service
		"""
        state = mixer.blend('core.State')
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
        state = mixer.blend('core.State')
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
        state = mixer.blend('core.State')
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
        state = mixer.blend('core.State')
        system = mixer.blend('core.System')
        system_credential = SystemCredentialService().create(username='credential', state=state, system=system)
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
        state = mixer.blend('core.State')
        system_monitor = SystemMonitorService().create(system=system, state=state, response_time=300)
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
        state = mixer.blend('core.State')
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

