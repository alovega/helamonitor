"""
Class for logging incoming events from connected microservices
"""
import logging
from core.backend.services import EventService, EscalationRuleService, SystemService, InterfaceService
from base.backend.services import EventTypeService, StateService

lgr = logging.getLogger(__name__)


class EventProcessor(object):
    """
    Class for processing events
    """

    def __init__(self):
        super(EventProcessor, self).__init__()

    def log_event(self, **kwargs):
        if kwargs is not None:
            description = kwargs.get('description', None)
            method = kwargs.get('method', None)
            response = kwargs.get('response', None)
            request = kwargs.get('request', None)
            code = kwargs.get('code', None)
            state = kwargs.get('state', None)
            try:
                system = SystemService().get(name = kwargs.get('system'))
                interface = InterfaceService().get(name = kwargs.get('interface'))
                event_type = EventTypeService().get(name = kwargs.get('event_type'))
                state = StateService().get(name = kwargs.get('state'))
                event_data = {
                    "description": description, "method": method, "response": response, "code": code, "state": state,
                    "request": request, "system": system, "interface": interface, "event_type": event_type
                }
            except Exception as ex:
                lgr.exception('Event processor exception %s' % ex)

        if event_data is not None:
            try:
                event = EventService().create(**event_data)
                return self.escalate_event(event)
            except Exception as ex:
                lgr.exception("Event Processor exception %s" % ex)

    def escalate_event(self, event, **kwargs):
        if event is not None:
            event_type = event.event_type
            matched_rule = EscalationRuleService().filter(event_type = event_type).first()
            return matched_rule.nth_event
            if matched_rule:
                nth_event = matched_rule.nth_event
                duration = matched_rule.duration
                state = matched_rule.state
                escalation_level = matched_rule.escalation_level







