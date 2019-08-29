from base.models import State, Occurrence, EndpointType, LogType, PriorityLevel, EventType, IncidentType,\
                        NotificationType,EscalationLevel

from servicebase import ServiceBase


class StateService(ServiceBase):
    """
    Service for State CRUD
    """
    manager = State.objects


class OccurrenceService(ServiceBase):
    """
    service for Occurrence CRUD
    """
    manager = Occurrence.objects


class EndpointTypeService(ServiceBase):
    """
    service for EndpointType CRUD
    """
    manager = EndpointType.objects


class LogTypeService(ServiceBase):
    """
    service for LogType CRUD
    """
    manager = LogType.objects


class PriorityLevelService(ServiceBase):
    """
    service for PriorityLevel CRUD
    """
    manager = PriorityLevel.objects


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