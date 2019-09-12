# coding=utf-8
"""
Class for logging and escalating reported events
"""
import logging
from datetime import timedelta

from django.utils import timezone
from core.backend.services import EventService, EscalationRuleService, SystemService, InterfaceService
from base.backend.services import EventTypeService, StateService
# from api.backend.processors.incident_log import IncidentLogger

lgr = logging.getLogger(__name__)


class EventLog(object):
	"""
	Class for processing events
	"""

	@staticmethod
	def log_event(
			event_type, system, interface = None, method = None, response = None, request = None, code = None,
			description = None, **kwargs):
		"""
		Logs an event reported from external systems or an health check
		@param event_type: Type of the event to be logged
		@type event_type: str
		@param system: The system where the event occurred
		@type system: str
		@param interface: Specific interface in a system where the event occurred
		@type interface: str | None
		@param method: Specific method within an interface where the event occurred
		@type method: str | None
		@param response: Response body, if any, of the reported event occurrence
		@type response: str | None
		@param request: Request body, if any, of the reported event occurrence
		@type request: str | None
		@param code: Response code of the event
		@type code: str | None
		@param description: Detailed information on the event occurrence
		@type description: str | None
		@param kwargs: Extra key=>value arguments to be passed for the event logging
		@return: The status of event creation in a response code dictionary:
		@rtype: dict
		"""
		try:
			system = SystemService().get(name = system, state__name = "Active")
			event_type = EventTypeService().get(name = event_type, state__name = "Active")
			if system is None or event_type is None:
				return {"code": "400.400.002"}
			event = EventService().create(
				event_type = event_type, system = system, method = method, response = response, request = request,
				code = code,
				interface = InterfaceService().get(name = interface, state__name = "Active", system = system),
				description = description, state = StateService().get(name = "Active")
			)
			if event is not None:
				escalation = EventLog().escalate_event(event)
				if escalation.get('code') != '800.200.001':
					lgr.error('%s event escalation Failed' % event_type)
				return {'code': '800.200.001'}
		except Exception as ex:
			lgr.exception('Event processor exception %s' % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def escalate_event(event):
		"""
		Checks registered escalation rules to determine if an event occurrence is to be escalated or not.
		@param event: Logged event to be escalated
		@type event: Event
		@return: The status of an event escalation in a response code dictionary
		@rtype: dict
		"""
		try:
			matched_rules = EscalationRuleService().filter(
				event_type = event.event_type, system = event.system).order_by("-nth_event")
			now = timezone.now()
			for matched_rule in matched_rules:
				escalated_events = EventService().filter(
					event_type = event.event_type, date_created__range = (now - matched_rule.duration, now)
				)
				if escalated_events.count() >= matched_rule.nth_event > 0:
					return IncidentLogger().log_incident(
						name = "%s event" % event.event_type.name, incident_type = "Realtime",
						system = event.system.name, state = "Investigating", escalated_events = escalated_events,
						escalation_level = matched_rule.escalation_level, event_type = event.event_type.name,
						description = "%s %s events occurred in %s between %s and %s" % (
							matched_rule.nth_event, event.event_type, matched_rule.system,
							now - matched_rule.duration, now)
					)
			return {"code": "800.200.001"}
		except Exception as ex:
			lgr.exception("Event Logger exception %s " % ex)
		return {"code": "800.400.001"}
