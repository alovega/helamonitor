"""
Services for Core module
"""
from core.models import System, Interface, SystemCredential, Recipient, SystemRecipient, SystemMonitor, Event, \
    Incident, IncidentEvent, IncidentLog, Notification, Endpoint, EscalationRule

from base.backend.servicebase import ServiceBase


class SystemService(ServiceBase):
    """
    Service for SystemService CRUD
    """
    manager = System.objects


class InterfaceService(ServiceBase):
    """
    Service for Interface CRUD
    """
    manager = Interface.objects


class SystemCredentialService(ServiceBase):
    """
    Service for SystemCredential CRUD
    """
    manager = SystemCredential.objects


class SystemMonitorService(ServiceBase):
    """
    Service for SystemMonitor CRUD
    """
    manager = SystemMonitor.objects


class RecipientService(ServiceBase):
    """
    Service for Recipient CRUD
    """
    manager = Recipient.objects


class SystemRecipientService(ServiceBase):
    """
    Service for SystemRecipient CRUD
    """
    manager = SystemRecipient.objects


class EventService(ServiceBase):
    """
    Service for Event CRUD
    """
    manager = Event.objects


class IncidentService(ServiceBase):
    """
    Service for Incident CRUD
    """
    manager = Incident.objects


class IncidentEventService(ServiceBase):
    """
    Service for IncidentEvent CRUD
    """
    manager = IncidentEvent.objects


class IncidentLogService(ServiceBase):
    """
    Service for IncidentLog CRUD
    """
    manager = IncidentLog.objects


class NotificationService(ServiceBase):
    """
    Service for Notification CRUD
    """
    manager = Notification.objects


class EndpointService(ServiceBase):
    """
    service for Endpoint CRUD
    """
    manager = Endpoint.objects


class EscalationRuleService(ServiceBase):
    """
    Service For EscalationRule CRUD
    """
    manager = EscalationRule.objects
