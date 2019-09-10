# coding=utf-8
"""
Class for logging and escalating reported events
"""
import logging
from datetime import timedelta

from django.utils import timezone
from core.backend.services import EventService, EscalationRuleService, SystemService, InterfaceService
from base.backend.services import EventTypeService, StateService
from api.backend.processors.incident_log import IncidentLogger


lgr = logging.getLogger(__name__)


class EventLog(object):
	"""
	Class for processing events
	"""

	@staticmethod
	def log_event(event_type, system, interface=None, method='', response='', request='',
															code='', description='', **kwargs):
		"""
		Method that creates an event
		@param event_type: type of the reported event
		@type event_type: str
		@param system: the system reporting the event
		@type system: str
		@param interface: the interface where the event occurred in
		@type interface: str
		@param method: Specific method within the interface where the event occurred
		@type method: str
		@param response: response body from the event
		@type response: str
		@param request: request body of the event
		@type request: str
		@param code: response code of the event
		@type code: str
		@param description: Detailed information on the event
		@type description: str
		@param kwargs: extra fields in the event
		@return: response code:
		@rtype: dict
		"""
		try:
			system = SystemService().get(name=system, state__name="Active")
			event_type = EventTypeService().get(name=event_type, state__name="Active")
			if system is None or event_type is None:
				return {"code": "400.400.002"}
			event = EventService().create(
				event_type=event_type, system=system, method=method, response=response, request=request, code=code,
				interface=InterfaceService().get(name=interface, state__name="Active", system=system),
				description=description, state=StateService().get(name="Active"),
			)
			if event is not None:
				escalation = EventLog().escalate_event(event)
				if escalation.get('code') == '800.200.001':
					lgr.warning('%s event escalation Failed' % event_type)
				return {'code': '800.200.001'}
		except Exception as ex:
			lgr.exception('Event processor exception %s' % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def escalate_event(event):
		"""
		Checks registered escalation rules to determine if an escalation is needed for an event.
		@param event: the logged event
		@type event: Event
		@return: response code
		@rtype: dict
		"""
		try:
			matched_rules = EscalationRuleService().filter(
				event_type=event.event_type, system=event.system).order_by("-nth_event")
			now = timezone.now()
			for matched_rule in matched_rules:
				if matched_rule.duration > timedelta(seconds=1) and matched_rule.nth_event > 0:
					escalated_events = EventService().filter(
						event_type=event.event_type, date_created__range=(now - matched_rule.duration, now)
					)
					if escalated_events.count() >= matched_rule.nth_event:
						incident = IncidentLogger().log_incident(
							name = "%s event" % event.event_type.name, incident_type = "Realtime",
							system = event.system.name, state = "Investigating", escalated_events = escalated_events,
							escalation_level = matched_rule.escalation_level, event_type=event.event_type.name,
							description = "%s %s events occurred in %s between %s and %s" % (
								matched_rule.nth_event, event.event_type, matched_rule.system,
								now - matched_rule.duration, now)
						)
						if incident.get('code') != '800.200.001':
							lgr.warning('Incident creation for %s event failed' % event.event_type.name)
						return {'code': '800.200.001'}
			return {"code": "800.200.001"}
		except Exception as ex:
			lgr.exception("Event Logger exception %s " % ex)
		return {"code": "800.400.001"}
