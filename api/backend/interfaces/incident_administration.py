# coding=utf-8
"""
Class for incident Administration
"""
import logging
import dateutil.parser
from datetime import datetime
from dateutil.relativedelta import relativedelta
from core.models import User
from django.db.models import F, Q

from api.backend.interfaces.notification_interface import NotificationLogger
from core.backend.services import IncidentService, IncidentLogService, IncidentEventService, SystemService, \
	SystemRecipientService, RecipientService
from base.backend.services import StateService, EscalationLevelService, EventTypeService, IncidentTypeService

lgr = logging.getLogger(__name__)


class IncidentAdministrator(object):
	"""
	Class for Incident Administration
	"""

	@staticmethod
	def log_incident(
			incident_type, system, escalation_level, name, description, priority_level, event_type = None,
			state = "Investigating", escalated_events = None, scheduled_for = None, scheduled_until = None, **kwargs):
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
		@param state: Initial resolution state of the incident. Defaults to Investigating if left blank
		@type state: str
		@param priority_level: The level of importance to be assigned to the incident.
		@type priority_level: str
		@param escalation_level: Level at which an escalation is configured with a set of recipients
		@type escalation_level: str
		@param scheduled_for: Time the scheduled maintenance should begin if the incident is scheduled
		@type scheduled_for: str | None
		@param scheduled_until: Time the scheduled maintenance should end if the incident is scheduled
		@type scheduled_until: str | None
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system, state__name = "Active")
			incident_type = IncidentTypeService().get(name = incident_type, state__name = "Active")
			state = state if incident_type.name == 'Realtime' else "Scheduled"
			escalation_level = EscalationLevelService().get(
				pk = escalation_level, state__name = "Active")
			if system is None or incident_type is None or escalation_level is None:
				return {"code": "800.400.002"}
			if incident_type.name == "Realtime" and event_type is not None:
				incident = IncidentService().filter(event_type__name = event_type, system = system).exclude(
					Q(state__name = 'Resolved'), Q(state__name = 'Completed')).order_by('-date_created').first()
				if incident and int(priority_level) < 5:
					priority_level = incident.priority_level + 1
					return IncidentAdministrator().update_incident(
						incident_id = incident.id, escalation_level = escalation_level.name, name = incident.name,
						state = incident.state.id, priority_level = str(priority_level),
						description = "Priority level of %s incident changed to %s" % (incident.name, priority_level)
					)
			if incident_type.name == 'Scheduled':
				scheduled_for = dateutil.parser.parse(scheduled_for)
				scheduled_until = dateutil.parser.parse(scheduled_until)
			incident = IncidentService().create(
				name = name, description = description, state = StateService().get(name = state), system = system,
				incident_type = incident_type, scheduled_for = scheduled_for, scheduled_until = scheduled_until,
				event_type = EventTypeService().get(name = event_type), priority_level = int(priority_level)
			)
			incident_log = IncidentLogService().create(
				description = description, incident = incident, priority_level = priority_level,
				state = StateService().get(name = state), escalation_level = escalation_level
			)
			if incident is not None and incident_log is not None:
				if escalated_events:
					for event in escalated_events:
						incident_event = IncidentEventService().create(
							event = event, incident = incident, state = StateService().get(name = "Active")
						)
						if not incident_event:
							lgr.error("Error creating incident-events")
				system_recipients = SystemRecipientService().filter(
					escalation_level = escalation_level, system = incident.system, state__name = 'Active')
				recipients = RecipientService().filter(id__in = system_recipients, state__name = 'Active')
				sms_notification = NotificationLogger().send_notification(
					message = incident.description, message_type = "Sms", system_id = incident.system,
					recipients = [str(recipient["phone_number"]) for recipient in recipients.values("phone_number")]
				)
				email_notification = NotificationLogger().send_notification(
					message = incident.description, message_type = "Email", system_id = incident.system,
					recipients = [str(recipient['user__email']) for recipient in recipients.values('user__email')]
				)
				if sms_notification.get('code') != '800.200.001' or email_notification.get('code') != '800.200.001':
					lgr.warning("Notification sending failed")
				return {'code': '800.200.001'}
		except Exception as ex:
			lgr.exception("Incident Logger exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def update_incident(incident_id, name, escalation_level, state, description, user = None, priority_level = None):
		"""
		Logs incident updates e.g changes in resolution state or priority level of an incident
		@param incident_id: The id of the incident to be updated
		@type incident_id: str
		@param name: The name of the incident to be updated
		@type name: str
		@param escalation_level: Level at which to send notifications to configured users
		@type escalation_level: str
		@param state: New resolution state of the incident
		@type state: str
		@param description: Detailed information on the incident update
		@type description: str
		@param user: User assigned to the incident
		@type user: str | None
		@param priority_level: New priority level of the incident
		@type priority_level: str | None
		@return: Response code in a dictionary to indicate if the incident was updated or not
		@rtype: dict
		"""
		try:
			state = StateService().get(pk = state)
			incident = IncidentService().get(pk = incident_id)
			escalation_level = EscalationLevelService().get(pk = escalation_level, state__name = "Active")
			user = User.objects.filter(id = user).first() if user else None
			if incident is None or escalation_level is None or state is None:
				return {'code': '800.400.002'}
			priority_level = int(priority_level) if priority_level is not None else incident.priority_level
			incident_log = IncidentLogService().create(
				description = description, incident = incident, user = user,
				priority_level = priority_level, state = state, escalation_level = escalation_level
			)
			if state.name == 'Completed' or state.name == 'Resolved':
				IncidentService().update(
					pk = incident.id, priority_level = priority_level, state = state, name = name
				)
			else:
				IncidentService().update(pk = incident.id, priority_level = priority_level)
			if incident_log:
				system_recipients = SystemRecipientService().filter(
					escalation_level = escalation_level, system = incident.system).values('recipient')
				recipients = RecipientService().filter(id__in = system_recipients, state__name = 'Active')
				sms_notification = NotificationLogger().send_notification(
					message = incident_log.description, message_type = "Sms", system_id = incident.system,
					recipients = [str(recipient["phone_number"]) for recipient in recipients.values("phone_number")]
				)
				email_notification = NotificationLogger().send_notification(
					message = incident_log.description, message_type = "Email", system_id = incident.system,
					recipients = [str(recipient['user__email']) for recipient in recipients.values('user__email')]
				)
				if sms_notification.get('code') != '800.200.001' or email_notification.get('code') != '800.200.001':
					lgr.warning("Notification sending failed")
				return {'code': '800.200.001'}
		except Exception as ex:
			lgr.exception("Incident Administration exception %s" % ex)
		return {'code': '800.400.001'}

	@staticmethod
	def get_incident(system, incident_id):
		"""
		Retrieves a single incident within a system
		@param system: System where the incident is created in
		@type system: str
		@param incident_id: Id of the incident to be retrieved
		@type incident_id: str
		@return: incident | response code to indicate errors retrieving the incident
		@rtype: dict
		"""
		try:
			system = SystemService().get(name = system, state__name = 'Active')
			incident = IncidentService().filter(pk = incident_id, system = system).values(
				'name', 'state', 'description', 'system_id', 'priority_level', 'date_created', 'date_modified',
				'scheduled_for', 'scheduled_until', type = F('incident_type__name'), eventtype = F('event_type__name'),
				incident_id = F('id'), status = F('state__name'), affected_system = F('system__name'),
			).first()
			if system is None or incident is None:
				return {'code': '800.400.002'}
			incident_updates = list(IncidentLogService().filter(incident__id = incident_id).values(
				'description', 'priority_level', 'date_created', 'escalation_level',
				'date_modified', user_name = F('user__username'), status = F('state__name')
			).order_by('-date_created'))
			incident.update(incident_updates = incident_updates)
			return {'code': '800.200.001', 'data': incident}
		except Exception as ex:
			lgr.exception("Incident Administration Exception: %s" % ex)
		return {'code': '800.400.001'}

	@staticmethod
	def get_incidents(system, **kwargs):
		"""
		Retrieves a incidents within the specified start and end date range within a system
		@param system: System where the incident is created in
		@type system: str
		@param kwargs: Extra key, value arguments to be passed
		@return: incidents | response code to indicate errors retrieving the incident
		@rtype: dict
		"""
		try:
			system = SystemService().get(name = system, state__name = 'Active')
			if not system:
				return {'code': '800.400.002'}

			incidents = list(IncidentService().filter(system = system).values(
				'name', 'state', 'description', 'system_id', 'priority_level', 'date_created', 'date_modified',
				'scheduled_for', 'scheduled_until', type = F('incident_type__name'), eventtype = F('event_type__name'),
				incident_id = F('id'), status = F('state__name'), affected_system = F('system__name')
			).order_by('-date_created'))
			for incident in incidents:
				incident_updates = list(IncidentLogService().filter(incident__id = incident.get('incident_id')).values(
					'description', 'priority_level', 'date_created', 'escalation_level', 'date_modified',
					status = F('state__name'), user_name = F('user__username')).order_by('-date_created'))
				incident.update(incident_updates = incident_updates)

			return {'code': '800.200.001', 'data': incidents}

		except Exception as ex:
			lgr.exception("Get incidents exception %s" % ex)
		return {'code': '800.400.001'}

	@staticmethod
	def delete_incident(incident_id, system_id, **kwargs):
		"""
		Deletes an incident for a selected system.
		@param incident_id: The id of the incident to be deleted
		@type incident_id: str
		@param system_id: System where the incident is defined in
		@type system_id: str
		@param kwargs: Extra key-value arguments to pass for incident deleting
		@return: Response code dictionary to indicate if the incident was deleted or not
		@rtype: dict
		"""
		try:
			system = SystemService().filter(pk = system_id, state__name = 'Active').first()
			if system is None:
				return {"code": "800.400.002"}
			incident = IncidentService().filter(pk = incident_id, system = system).first()
			if incident:
				if incident.delete():
					return {'code': '800.200.001', 'Message': 'Incident deleted successfully'}
		except Exception as ex:
			lgr.exception("Incident Delete exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def get_incident_events(incident_id, system_id, **kwargs):
		"""
		Retrieves the events that have caused the incident in a selected system.
		@param incident_id: The id of the incident
		@type incident_id: str
		@param system_id: System where the incident is created in
		@type system_id: str
		@param kwargs: Extra key-value arguments to pass for incident_event retrieval
		@return: Response code dictionary to indicate if the incident_events were retrieved or not
		@rtype: dict
		"""
		from api.backend.interfaces.event_log import EventLog
		try:
			system = SystemService().filter(pk = system_id, state__name = 'Active').first()
			incident = IncidentService().filter(pk = incident_id, system = system).first()

			if system is None or incident is None:
				return {"code": "800.400.002"}
			incident_events = list(IncidentEventService().filter(incident = incident, state__name = 'Active').values(
				incident_id = F('incident'), status = F('state__name'), event_id = F('event')
			).order_by('-date_created'))
			for incident_event in incident_events:
				event = EventLog.get_event(incident_event.get('event_id'), system.id)
				if event.get('code') != '800.200.001':
					lgr.error('Event get Failed')
				incident_event.update(incident_event = event.get('data'))
			return {'code': '800.200.001', 'data': incident_events}
		except Exception as ex:
			lgr.exception("Get Incident Event exception %s" % ex)
		return {"code": "800.400.001"}
