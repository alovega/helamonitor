# coding=utf-8
"""
Class for Escalation Rules Administration
"""
from datetime import timedelta
import logging
import dateutil.parser
from django.contrib.auth.models import User
from django.db.models import F, Q

from api.backend.interfaces.notification_interface import NotificationLogger
from core.backend.services import IncidentLogService, IncidentEventService, SystemService, \
	SystemRecipientService, RecipientService, EscalationRuleService
from base.backend.services import StateService, EscalationLevelService, EventTypeService, IncidentTypeService

lgr = logging.getLogger(__name__)


class EscalationRuleAdministrator(object):
	"""
	Class for Escalation Rules Administration
	"""

	@staticmethod
	def create_rule(name, description, system, nth_event, state, escalation_level, duration, **kwargs):
		"""
		Creates an escalation rule for a selected system.
		@param name: Name of the escalation rule to be created
		@type name: str
		@param system: The system which the escalation rule will be applied in
		@type system: str
		@param description: Details on the Escalation Rule
		@type description: str
		@param nth_event: Number of event of a certain type that need to be logged to raise an escalation
		@type nth_event: str
		@param duration:Time period within which certain events muct occur to trigger an escalation.
		@type duration: str
		@param state: State of the incident. Defaults to Active
		@type state: str
		@param escalation_level: Level at which an escalation is configured with a set of recipients
		@type escalation_level: str
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().get(name = system, state__name = "Active")
			state = StateService().get(name = state)
			escalation_level = EscalationLevelService().get(name = escalation_level, state__name = "Active")

			if system is None or state is None or escalation_level is None:
				return {"code": "800.400.002"}
			escalation_rule = EscalationRuleService().create(
				name = name, description = description, system = system, nth_event = int(nth_event),
				duration = timedelta(seconds = int(duration)), state = state, escalation_level = escalation_level
			)

			if escalation_rule is not None:
				rule = EscalationRuleService().filter(pk = escalation_rule.id, system = system).values(
					'name', 'description', 'duration', 'date_created', 'date_modified',
					'nth_event', 'escalation_level', eventtype = F('event_type__name'), status = F('state__name'),
					system_name = F('system__name')
				).first()
				return {'code': '800.200.001', 'data': rule}
		except Exception as ex:
			lgr.exception("Escalation Rule Creation exception %s" % ex)
		return {"code": "800.400.001", 'error': ex}
	#
	# @staticmethod
	# def update_rule(incident_id, name, escalation_level, state, description, user = None, priority_level = None):
	# 	"""
	# 	Logs incident updates e.g changes in resolution state or priority level of an incident
	# 	@param incident_id: The id of the incident to be updated
	# 	@type incident_id: str
	# 	@param name: The name of the incident to be updated
	# 	@type name: str
	# 	@param escalation_level: Level at which to send notifications to configured users
	# 	@type escalation_level: str
	# 	@param state: New resolution state of the incident
	# 	@type state: str
	# 	@param description: Detailed information on the incident update
	# 	@type description: str
	# 	@param user: User assigned to the incident
	# 	@type user: str | None
	# 	@param priority_level: New priority level of the incident
	# 	@type priority_level: str | None
	# 	@return: Response code in a dictionary to indicate if the incident was updated or not
	# 	@rtype: dict
	# 	"""
	# 	try:
	# 		state = StateService().get(name = state)
	# 		incident = IncidentService().get(pk = incident_id)
	# 		escalation_level = EscalationLevelService().get(name = escalation_level, state__name = "Active")
	# 		if incident is None or escalation_level is None or state is None:
	# 			return {'code': '800.400.002'}
	# 		priority_level = int(priority_level) if priority_level is not None else incident.priority_level
	# 		incident_log = IncidentLogService().create(
	# 			description = description, incident = incident, user = User.objects.filter(username = user).first(),
	# 			priority_level = priority_level, state = StateService().get(name = state)
	# 		)
	# 		updated_incident = IncidentService().update(
	# 			pk = incident.id, priority_level = priority_level, state = StateService().get(name = state),
	# 			name = name
	# 		)
	# 		if incident_log and updated_incident:
	# 			system_recipients = SystemRecipientService().filter(
	# 				escalation_level = escalation_level, system = incident.system).values('recipient')
	# 			recipients = RecipientService().filter(id__in = system_recipients, state__name = 'Active')
	# 			notification = NotificationLogger().send_notification(
	# 				message = incident_log.description, message_type = "Email",
	# 				recipients = [recipient["email"] for recipient in recipients.values("email")]
	# 			)
	# 			if notification.get('code') != '800.200.001':
	# 				lgr.warning("Notification sending failed")
	# 			return {'code': '800.200.001'}
	# 	except Exception as ex:
	# 		lgr.exception("Incident Administration exception %s" % ex)
	# 	return {'code': '800.400.001'}
	#
	# @staticmethod
	# def get_rule(system, incident_id):
	# 	"""
	# 	Retrieves a single incident within a system
	# 	@param system: System where the incident is created in
	# 	@type system: str
	# 	@param incident_id: Id of the incident to be retrieved
	# 	@type incident_id: str
	# 	@return: incident | response code to indicate errors retrieving the incident
	# 	@rtype: dict
	# 	"""
	# 	try:
	# 		system = SystemService().get(name = system, state__name = 'Active')
	# 		incident = IncidentService().filter(pk = incident_id, system = system).values(
	# 			'name', 'description', 'system_id', 'priority_level', 'date_created', 'date_modified',
	# 			'scheduled_for', 'scheduled_until', type = F('incident_type__name'), eventtype = F('event_type__name'),
	# 			incident_id = F('id'), status = F('state__name'), affected_system = F('system__name'),
	# 		).first()
	# 		if system is None or incident is None:
	# 			return {'code': '800.400.002'}
	# 		incident_updates = list(IncidentLogService().filter(incident__id = incident_id).values(
	# 			'description', 'priority_level', 'date_created', 'date_modified', user_name = F('user'),
	# 			status = F('state__name')
	# 		).order_by('-date_created'))
	# 		incident.update(incident_updates = incident_updates)
	# 		return {'code': '800.200.001', 'data': incident}
	# 	except Exception as ex:
	# 		lgr.exception("Incident Administration Exception: %s" % ex)
	# 	return {'code': '800.400.001'}
	#
	# @staticmethod
	# def get_rules(system, start_date, end_date):
	# 	"""
	# 	Retrieves a incidents within the specified start and end date range within a system
	# 	@param system: System where the incident is created in
	# 	@type system: str
	# 	@param start_date: Start date limit applied
	# 	@type start_date: str
	# 	@param end_date: End date limit to be applied
	# 	@type end_date: str
	# 	@return: incidents | response code to indicate errors retrieving the incident
	# 	@rtype: dict
	# 	"""
	# 	try:
	# 		system = SystemService().get(name = system, state__name = 'Active')
	# 		start_date = dateutil.parser.parse(start_date)
	# 		end_date = dateutil.parser.parse(end_date)
	# 		if not system:
	# 			return {'code': '800.400.002'}
	# 		incidents = list(IncidentService().filter(
	# 			system = system, date_created__gte = start_date, date_created__lte = end_date
	# 		).values(
	# 			'name', 'description', 'system_id', 'priority_level', 'date_created', 'date_modified',
	# 			'scheduled_for', 'scheduled_until', type = F('incident_type__name'), eventtype = F('event_type__name'),
	# 			incident_id = F('id'), status = F('state__name'), affected_system = F('system__name')
	# 		).order_by('-date_created'))
	# 		for incident in incidents:
	# 			incident_updates = list(IncidentLogService().filter(incident__id = incident.get('incident_id')).values(
	# 				'description', 'priority_level', 'date_created', 'date_modified', user_name = F('user'),
	# 				status = F('state__name')
	# 			).order_by('-date_created'))
	# 			incident.update(incident_updates = incident_updates)
	#
	# 		return {'code': '800.200.001', 'data': incidents}
	#
	# 	except Exception as ex:
	# 		lgr.exception("Get incidents exception %s" % ex)
	# 	return {'code': '800.400.001', 'error': ex}
