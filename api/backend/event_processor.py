"""
Class for logging incoming events from connected micro-services
"""
import logging
from datetime import timedelta
from django.utils import timezone
from core.backend.services import EventService, EscalationRuleService, SystemService, InterfaceService
from base.backend.services import EventTypeService, StateService
from base.backend.utilities import format_duration

lgr = logging.getLogger(__name__)


class EventProcessor(object):
    """
    Class for processing events
    """

    def __init__(self):
        super(EventProcessor, self).__init__()

    def log_event(self, event_type, system, interface, description, state, **kwargs):
        """
        Method that formats event data and logs the event
        :param event_type:
        :param system:
        :param interface:
        :param description:
        :param state:
        :param kwargs:
        :return: event:
        """
        event_data = {}
        try:
            system = SystemService().get(name=system)
            interface = InterfaceService().get(name=interface)
            event_type = EventTypeService().get(name=event_type)
            state = StateService().get(name=state)
            if kwargs is not None:
                method = kwargs.get('method', None)
                response = kwargs.get('response', None)
                request = kwargs.get('request', None)
                code = kwargs.get('code', None)
                event_data.update({
                    "method": method, "response": response, "code": code, "state": state, "request": request,
                })
            event_data.update({
                "description": description, "system": system, "interface": interface, "event_type": event_type
            })
        except Exception as ex:
            lgr.exception('Event processor exception %s' % ex)

        if event_data is not None:
            try:
                event = EventService().create(**event_data)
                return self.escalate_event(event)
            except Exception as ex:
                lgr.exception("Event Processor exception %s" % ex)

    @staticmethod
    def escalate_event(event):
        """
        Method that processes an event and checks the existing escalation rules to determine if an escalation is needed.
        :param event:
        :return: incident_data: Data needed for creating an incident based on the escalation_rules and event(s)
        :rtype: dict
        """
        if event is not None:
            event_type = event.event_type
            system = event.system
            matched_rules = EscalationRuleService().filter(event_type=event_type, system=system)  # Filter out
            # satisfied rules for the system the event originates from
            incident_data = {
                "name": "%s event" % event_type.name, "incident_type": "realtime", "system": event.system.name,
                "state": "Investigating", "priority_level": 1
            }   # Data to be used during incident creation and escalating to configured users
            for matched_rule in matched_rules:
                nth_event = matched_rule.nth_event
                duration = matched_rule.duration
                escalation_level = matched_rule.escalation_level

                if duration > timedelta(seconds=1) and nth_event > 0:
                    # Duration set at a minimum of a second and number of events is greater than zero.
                    now = timezone.now()
                    start = now-duration
                    if nth_event == 1:
                        # Escalates each event occurrence within the specified duration
                        event = EventService().filter(event_type=event_type, date_created__range=(start, now)).order_by(
                            "-date_created").first()
                        if event:
                            incident_data.update(escalation_level = escalation_level,
                                                 description = "%s event occurred on %s in %s" % (
                                                     event_type, now, system), events = event)
                            return incident_data
                    else:
                        # Escalate if n events of the specified event type occur within the specified duration
                        try:
                            events = EventService().filter(event_type=event_type, date_created__range=(start, now))
                            if events.count() == nth_event:
                                # Rule match found. Update incident_data with an appropriate description and the events
                                incident_data.update(escalation_level=escalation_level,
                                                     description="%s %s events occurred in %s between %s and %s" % (
                                                         nth_event, event_type, system, start, now), events=events)
                                return incident_data
                        except Exception as ex:
                            lgr.exception("Event Processor exception %s " % ex)
