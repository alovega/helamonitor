# coding=utf-8
"""
Class for creating new incidents and logging incident updates
"""
import logging

from core.backend.services import SystemService, IncidentService, IncidentEventService, SystemRecipientService, \
	NotificationService
from base.backend.services import IncidentTypeService, StateService, EventTypeService, EscalationLevelService, \
	NotificationTypeService

import datetime

lgr = logging.getLogger(__name__)


class IncidentLogger(object):
	"""
	Class for logging incidents
	"""

	@staticmethod
	def create_incident(
			incident_type, system, escalation_level, name = '', description = '', event_type = None,
			escalated_events = None, priority_level = '', message = '', **kwargs):
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
		@param priority_level: The priority level to be assigned to the incident.
		@type priority_level: str | None
		@param escalation_level: Level at which an escalation is configured with a set of recipients
		@type escalation_level: str
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
					incident.priority_level += 1
					return {'code': '800.200.001'}
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
				notification = IncidentLogger.send_notification(
					incident, escalation_level = escalation_level, message = "message")
				if notification.get('code') != '800.200.001':
					lgr.error("Notification sending failed")
				return {'code': '800.200.001'}
		except Exception as ex:
			lgr.exception("Incident Logger exception %s" % ex)
		return {"code": "200.400.002"}

	@staticmethod
	def notification(incident, message, escalation_level = None, assignee = None):

		notifications_data = []
		try:
			if escalation_level is not None:
				recipients = SystemRecipientService().filter(
					status__name = 'Active', escalation_level = escalation_level, system = incident.system
				)
				for recipient in recipients:
					if recipient.phone_number and recipient.email:
						notification_data1 = {
							"message": message, "notification_type": NotificationTypeService().get('SMS'),
							"recipient": recipient, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notification_data2 = {
							"message": message, "notification_type": NotificationTypeService().get('Email'),
							"recipient": recipient, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.extend((notification_data1, notification_data2))
					elif recipient.phone_number is not None:
						notification_data = {
							"message": message, "notification_type": NotificationTypeService().get('SMS'),
							"recipient": recipient, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.append(notification_data)
					else:
						notification_data = {
							"message": message, "notification_type": NotificationTypeService().get('Email'),
							"recipient": recipient, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.append(notification_data)
				else:

					if assignee.phone_number and assignee.email:
						notification_data1 = {
							"message": message, "notification_type": NotificationTypeService().get('email'),
							"recipient": assignee, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notification_data2 = {
							"message": message, "notification_type": NotificationTypeService().get('SMS'),
							"recipient": assignee, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.extend((notification_data1, notification_data2))
					elif assignee.phone_number:
						notification_data = {
							"message": message, "notification_type": NotificationTypeService().get('SMS'),
							"recipient": assignee, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.append(notification_data)
					else:
						data = {
							"message": message, "notification_type": NotificationTypeService().get('SMS'),
							"recipient": assignee, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.append(data)
					return {"code": "200.400.005"}
				return {"code": "800.200.001", "data": notifications_data}
		except Exception as e:
			lgr.exception("Notification logger exception %s" % e)
