"""
Class for logging incoming events from connected microservices
"""
import logging
from core.backend.services import EventService, EscalationRuleService

lgr = logging.getLogger(__name__)


class EventLogger(object):
    """
    Class for logging events
    """
    event = None

    def __init__(self, **kwargs):
        super(EventLogger, self).__init__()
        try:
            if self.event is None:
                self.event = EventService().create(**kwargs)  # Create event Object
        except Exception as ex:
            lgr.exception('Event Log exception %s' % ex)







