# coding=utf-8
"""
Class for creating new incidents and logging incident updates
"""
import logging

from core.backend.services import SystemService, IncidentService
from base.backend.services import IncidentTypeService, StateService, EventTypeService
lgr = logging.getLogger(__name__)


class IncidentLogger(object):
	"""
	Class for logging incidents
	"""
	@staticmethod
	def create_incident(incident_type, system, name='', description='', event_type='', escalated_events=None,
						priority_level='', escalation_level='', **kwargs):
		"""
		Creates an incident from the escalated events
		@param incident_type: Type of the incident to be created
		@type incident_type: str
		@param system: System where the incident is to be reported
		@type system: str
		@param name: Title of the incident
		@type name: str
		@param description: Details on the incident
		@type description: str
		@param event_type: Type of the event that triggered the creation of the incident
		@type event_type: str
		@param escalated_events: One or more events that satisfied an escalation rule.
		@type escalated_events: list
		@param priority_level: The priority level to be assigned to the incident.
		@type priority_level: str
		@param escalation_level: Configuration for the recipients of a notification after incident creation
		@type escalation_level: str
		@param kwargs:
		@return:
		"""
		try:
			system = SystemService().get(name=system, state__name = "Active")
			incident_type = IncidentTypeService().get(name=incident_type, state__name="Active")
			if system is None or incident_type is None:
				return {"code": "800.400.002"}

			open_incident = IncidentService().filter(event_type__name=event_type).exclude(
				state__name='Resolved').order_by('-date_created').first()
			if open_incident:
				open_incident.priority_level += 1
				notification = IncidentLogger.send_notification(
					open_incident, escalation_level=escalation_level, message="message")
			else:
				incident = IncidentService().create(
					name = name, description = description, state = StateService().get(name = "Active"),
					incident_type = incident_type, system = system,
					priority_level = EventTypeService().get(name = event_type).priority_level()
				)
				if incident is not None:
					notification = IncidentLogger.send_notification(incident, escalation_level)
			if notification.get('code') != '800.200.001':
				lgr.warning('Error during notification')
			return {"code": "200.400.002"}
		except Exception as ex:
			lgr.exception("Incident Logger exception %s" % ex)
		return {"code": "200.400.002"}

	def log_incident(self):
		pass

	@staticmethod
	def send_notification(incident, escalation_level, message):
		return {'code': '800.200.001'}
