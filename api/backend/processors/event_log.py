# coding=utf-8
"""
Class for logging and escalating reported events
"""
import logging
from datetime import timedelta

from django.utils import timezone
from core.backend.services import EventService, EscalationRuleService, SystemService, InterfaceService, IncidentService
from base.backend.services import EventTypeService, StateService

lgr = logging.getLogger(__name__)


class EventLog(object):
	"""
	Class for processing events
	"""

	@staticmethod
	def log_event(event_type, system, **kwargs):
		"""
		Method that formats event data and logs the event
		@param event_type: type of the reported event
		@param system: the system which reported the event
		@param kwargs: extra fields in the event e.g. request, response and description
		@return: EventLog | None:
		@rtype: EventLog
		"""
		try:
			system = SystemService().get(name=system, state__name="Active")
			event_type = EventTypeService().get(name=event_type, state__name="Active")
			if system is None or event_type is None:
				return {"code": "200.400.001"}
			event = EventService().create(
				event_type=event_type, system=system, interface=InterfaceService().get(
					name=kwargs.get("interface", None), state__name="Active", system=system), state=StateService().get(
					name="Active"), method=kwargs.get('method', None), response=kwargs.get('response', None),
				request=kwargs.get('request', None), code=kwargs.get('code', None), description=kwargs.get(
					'description', None)
			)

			if event is not None:
				return EventLog().escalate_event(event)
			return {"code": "200.400.001"}
		except Exception as ex:
			lgr.exception('Event processor exception %s' % ex)
		return {"code": "200.400.001"}

	@staticmethod
	def escalate_event(event):
		"""
		Checks registered escalation rules to determine if an escalation is needed for an event.
		@param event: the logged event
		@return: incident | None: Returns a created incident based on the matched rules
		@rtype: Incident | None
		"""
		try:
			matched_rules = EscalationRuleService().filter(
				event_type=event.event_type, system=event.system).order_by("-nth_event")
			now = timezone.now()
			# Filter out escalation rules for the system the event is reported from
			for matched_rule in matched_rules:
				if matched_rule.duration > timedelta(seconds=1) and matched_rule.nth_event > 0:
					# Escalate if n events of the specified event type occur within the specified duration
					escalated_events = EventService().filter(
						event_type=event.event_type, date_created__range=(now - matched_rule.duration, now)
					).order_by("-date_created")

					if escalated_events.count() >= matched_rule.nth_event:
						incident = IncidentService().create(
							name="%s event" % event.event_type.name, incident_type="realtime",
							system=event.system.name, state="Investigating", priority_level=1,
							escalation_level=matched_rule.escalation_level, escalated_events=escalated_events,
							description= "%s %s events occurred in %s between %s and %s" % (
								matched_rule.nth_event, event.event_type, matched_rule.system,
								now - matched_rule.duration, now)
						)
						return incident
		except Exception as ex:
			lgr.exception("Event Logger exception %s " % ex)
		return {"code": "300.400.001"}
