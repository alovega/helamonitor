# coding=utf-8
"""
Class for creating new incidents and logging incident updates
"""
import logging

from core.backend.services import SystemService, IncidentService, IncidentEventService, IncidentLogService
from base.backend.services import IncidentTypeService, StateService, EventTypeService, EscalationLevelService, \
	LogTypeService

lgr = logging.getLogger(__name__)


class IncidentLogger(object):
	"""
	Class for logging incidents
	"""

	@staticmethod
	def create_incident(
			incident_type, system, escalation_level, name, description, event_type = None,
			escalated_events = None, priority_level = None, message = None, **kwargs):
		"""
		Creates a realtime incident based on escalated events or scheduled incident based on user reports
		@param incident_type: Type of the incident to be created
		@type incident_type: str
		@param system: The system which the incident will be associated with
		@type system: str
		@param name: Title of the incident
		@type name: str
		@param description: Details on the incident
		@type description: str
		@param event_type: Type of the event(s) that triggered creation of the incident, if its event driven.
		@type event_type: str | None
		@param escalated_events: One or more events in the escalation if the incident is event driven.
		@type escalated_events: list | None
		@param priority_level: The level of importance to be assigned to the incident.
		@type priority_level: str | None
		@param message: The message to be sent out during notification after incident creation.
		@type message: str | None
		@param escalation_level: Level at which an escalation is configured with a set of recipients
		@type escalation_level: str
		@param duration: The duration to check for an unresolved incident caused by the same event type occurrence.
		@type duration: timedelta | None
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Status of the incident creation in a response code dictionary
		@rtype: dict
		"""
		try:
			system = SystemService().get(name = system, state__name = "Active")
			incident_type = IncidentTypeService().get(name = incident_type, state__name = "Active")
			escalation_level = EscalationLevelService().get(
				name = escalation_level, state__name = "Active", system = system)
			if system is None or incident_type is None or escalation_level is None:
				return {"code": "800.400.002"}

			if incident_type.name == "Realtime" and escalated_events is not None and event_type is not None:
				incident = IncidentService().filter(event_type__name = event_type).exclude(
					state__name = 'Resolved').order_by('-date_created').first()
				if incident:
					incident_log = IncidentLogService().create(
						description = "Priority level increased to %s" % incident.priority_level + 1,
						priority_level = int(priority_level) + 1, incident = incident,
						log_type = LogTypeService().get(name = "PriorityUpdate"), state = incident.state
					)
					if incident_log is not None:
						pass
						# TODO add send_notification call
						return {'code': '800.200.001'}
					return {'code': '800.400.001'}
				else:
					priority_level = EventTypeService().get(name = event_type).priority_level()
			else:
				priority_level = int(priority_level)

			incident = IncidentService().create(
				name = name, description = description, state = StateService().get(name = "Active"),
				incident_type = incident_type, system = system, event_type = EventTypeService().get(
					name = 'event_type'),
				priority_level = priority_level
			)
			if incident is not None:
				if escalated_events is not None:
					for event in escalated_events:
						IncidentEventService().create(
							event = event, incident = incident, state = StateService().get(name = "Active")
						)
					# TODO add send_notification call
				return {'code': '800.200.001'}
		except Exception as ex:
			lgr.exception("Incident Logger exception %s" % ex)
		return {"code": "800.400.001"}
