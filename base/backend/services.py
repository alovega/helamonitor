from base.models import State, EndpointType, EventType, IncidentType, NotificationType, EscalationLevel

from servicebase import ServiceBase


class StateService(ServiceBase):
    """
    Service for State CRUD
    """
    manager = State.objects


class EndpointTypeService(ServiceBase):
    """
    service for EndpointType CRUD
    """
    manager = EndpointType.objects


class EventTypeService(ServiceBase):
    """
    service for EventType CRUD
    """
    manager = EventType.objects


class IncidentTypeService(ServiceBase):
    """
    Service for IncidentType CRUD
    """
    manager = IncidentType.objects


class NotificationTypeService(ServiceBase):
    """
    Service for NotificationType CRUD
    """
    manager = NotificationType.objects


class EscalationLevelService(ServiceBase):
    """
    Service for EscalationLevel CRUD
    """
    manager = EscalationLevel.objects
