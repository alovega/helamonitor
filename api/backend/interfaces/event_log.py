# coding=utf-8
"""
Class for logging and escalating reported events
"""
import logging
from datetime import timedelta, datetime
from django.db.models import F
from django.utils import timezone

from core.backend.services import EventService, EscalationRuleService, SystemService, InterfaceService
from base.backend.services import EventTypeService, StateService
from api.backend.interfaces.incident_administration import IncidentAdministrator

lgr = logging.getLogger(__name__)


class EventLog(object):
	"""
	Class for logging and escalating reported events by checking against registered escalation rules
	"""

	@staticmethod
	def log_event(
			event_type, system, interface = None, method = None, response = None, request = None, code = None,
			description = None, stack_trace = None, **kwargs):
		"""
		Logs an event that being reported from an external system or an health check
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
		@param stack_trace: Stack trace from the on the event occurrence
		@type stack_trace: str | None
		@param kwargs: Extra key=>value arguments to be passed for the event logging
		@return: Response code in a dictionary indicating if the event is created successfully or not
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system, state__name = "Active")
			event_type = EventTypeService().get(name = event_type, state__name = "Active")
			if system is None or event_type is None:
				return {"code": "800.400.002"}
			event = EventService().create(
				event_type = event_type, system = system, method = method, response = response, request = request,
				code = code, description = description, state = StateService().get(name = "Active"),
				interface = InterfaceService().get(name = interface, state__name = "Active", system = system),
				stack_trace = stack_trace
			)
			if event is not None:
				escalation = EventLog.escalate_event(event)
				if escalation.get('code') != '800.200.001':
					lgr.error('%s event escalation Failed' % event_type)
				created_event = EventService().filter(id = event.id).values(
					'id', 'event_type', 'state__id', 'system__id', 'method', 'response', 'request', 'code',
					'description', 'interface__id', 'stack_trace'
				).first()
				return {'code': '800.200.001', 'data': created_event}
		except Exception as ex:
			lgr.exception('Event processor exception %s' % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def escalate_event(event):
		"""
		Checks registered escalation rules to determine if an event occurrence is to be escalated or not.
		@param event: A logged event to be checked for escalation
		@type event: Event
		@return: Response code in a dictionary indicating if the event is created successfully or not
		@rtype: dict
		"""
		try:
			matched_rules = EscalationRuleService().filter(
				event_type = event.event_type, system = event.system).order_by("-nth_event")
			now = timezone.now()
			for matched_rule in matched_rules:
				escalated_events = EventService().filter(
					event_type = event.event_type, date_created__range = (
						now - timedelta(seconds = matched_rule.duration), now))
				if escalated_events.count() >= matched_rule.nth_event > 0:
					return IncidentAdministrator.log_incident(
						name = matched_rule.name, incident_type = "Realtime",
						system = event.system.id, state = "Investigating", escalated_events = escalated_events,
						escalation_level = matched_rule.escalation_level.id, event_type = event.event_type.name,
						description = matched_rule.description, priority_level =
						event.event_type.priority_level()
					)
			return {"code": "800.200.001"}
		except Exception as ex:
			lgr.exception("Event Logger exception %s " % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def get_event(event_id, system_id):
		"""
		Retrieves an event logged for a certain system
		@param: event_id: Id of the event
		@type event_id: str
		@param: system_id: Id of the system
		@type system_id: str
		@return: Response code indicating status and logged event
		"""
		try:
			system = SystemService().get(pk = system_id, state__name = 'Active')
			event = EventService().filter(pk = event_id, system = system, state__name = 'Active').values(
				'id', 'date_created', 'interface', 'method', 'request', 'response', 'stack_trace', 'description',
				'code', status = F('state__name'), system_name = F('system__name'), eventtype = F('event_type__name')
			).first()
			if system is None or event is None:
				return {'code': '800.400.200', 'event': str(event_id)}
			return {'code': '800.200.001', 'data': event}
		except Exception as ex:
			lgr.exception("Get event Exception %s" % ex)
		return {'code': '800.400.001'}

	@staticmethod
	def get_events(system_id):
		"""
		Retrieves events logged for a certain system
		@param: system_id: Id of the system
		@type system_id: str
		@return: Response code indicating status and logged events
		"""
		try:
			system = SystemService().get(pk = system_id, state__name = 'Active')
			if not system:
				return {'code': '800.400.200'}
			events = list(EventService().filter(system = system, state__name = 'Active').values(
				'id', 'date_created', 'interface', 'method', 'request', 'response', 'stack_trace', 'description',
				'code',
				status = F('state__name'), system_name = F('system__name'), eventtype = F('event_type__name')
			).order_by('-date_created'))
			return {'code': '800.200.001', 'data': events}
		except Exception as ex:
			lgr.exception("Get events Exception %s" % ex)
		return {'code': '800.400.001'}
