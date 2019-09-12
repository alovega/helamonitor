# coding=utf-8
"""
Class for incident Administration
"""
import logging

from core.backend.services import IncidentService, IncidentLogService, IncidentEventService, SystemService, \
	SystemRecipientService, RecipientService
from base.backend.services import LogTypeService, StateService, EscalationLevelService, EventTypeService, \
	IncidentTypeService, NotificationTypeService
from django.contrib.auth.models import User

lgr = logging.getLogger(__name__)


class IncidentAdministrator(object):
	"""
	Class for Incident Administration
	"""

	@staticmethod
	def log_incident(
			incident_type, system, escalation_level, name, description, event_type = None,
			escalated_events = None, priority_level = None, message = None, duration = None, **kwargs):
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
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().get(name = system, state__name = "Active")
			incident_type = IncidentTypeService().get(name = incident_type, state__name = "Active")
			escalation_level = EscalationLevelService().get(
				name = escalation_level, state__name = "Active")
			if system is None or incident_type is None or escalation_level is None:
				return {"code": "800.400.002"}

			if incident_type.name == "Realtime" and event_type is not None:
				incident = IncidentService().filter(event_type__name = event_type, system = system).exclude(
					state__name = 'Resolved').order_by('-date_created').first()
				if incident:
					priority_level = incident.priority_level + 1
					return IncidentAdministrator().update_incident(
						incident = incident.name, escalation_level = escalation_level.name, log_type = "PriorityUpdate",
						state = incident.state.name, priority_level = str(priority_level),
						description = "Priority level of %s incident changed to %s" % (incident.name, priority_level)
					)
				else:
					priority_level = EventTypeService().get(name = event_type).priority_level()
			else:
				priority_level = int(priority_level)

			incident = IncidentService().create(
				name = name, description = description, state = StateService().get(name = "Active"),
				incident_type = incident_type, system = system, event_type = EventTypeService().get(
					name = event_type), priority_level = priority_level
			)
			if incident is not None:
				if escalated_events is not None:
					for event in escalated_events:
						incident_event = IncidentEventService().create(
							event = event, incident = incident, state = StateService().get(name = "Active")
						)
						if not incident_event:
							lgr.error("Error creating incident-events")
				system_recipients = SystemRecipientService().filter(
					escalation_level = escalation_level, system = system)
				return {'code': '800.200.001'}
		except Exception as ex:
			lgr.exception("Incident Logger exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def update_incident(
			incident, log_type, escalation_level, state, description = None, user = None, priority_level = None):
		"""
		Logs incident updates e.g changes in resolution state or priority level of an incident
		@param incident: The incident to be updated
		@type incident: str
		@param log_type: The type of update to be done on the incident
		@type log_type: str
		@param escalation_level: Level at which to send notifications to configured users
		@type escalation_level: str
		@param state: New resolution state of the incident
		@type state: str
		@param description: Detailed information on the incident update
		@type description: str | None
		@param user: User assigned to the incident
		@type user: str | None
		@param priority_level: New priority level of the incident
		@type priority_level: str | None
		@return: Response code in a dictionary to indicate if the incident was updated or not
		@rtype: dict
		"""
		try:
			incident = IncidentService().get(name = incident, state__name = 'Active')
			log_type = LogTypeService().get(name = log_type, state__name = 'Active')
			escalation_level = EscalationLevelService().get(name = escalation_level, state__name = "Active")
			state = StateService().get(name = state)
			if incident is None or log_type is None or escalation_level is None or state is None:
				return {'code': '800.400.002'}
			if priority_level is not None:
				priority_level = int(priority_level)
			else:
				priority_level = incident.priority_level
			incident_log = IncidentLogService().create(
				description = description, incident = incident, user = User.objects.filter(username = user).first(),
				log_type = log_type, priority_level = priority_level, state = StateService().get(name = state)
			)
			if incident_log:
				system_recipients = SystemRecipientService().filter(
					escalation_level = escalation_level, system = incident.system).values('recipient')
				recipients = RecipientService().filter(id__in = system_recipients)
				email_list = [recipient["email"] for recipient in recipients.values("email")]
				phone_numbers = [recipient["phone_number"] for recipient in recipients.values("phone_number")]
				notification = NotificationLogger().send_notification(
					message = incident.description, recipients = email_list, message_type = "Email"
				)
				return {'code': '800.200.001'}
		except Exception as ex:
			lgr.exception("Incident Administration exception %s" % ex)
		return {'code': '800.400.001'}
