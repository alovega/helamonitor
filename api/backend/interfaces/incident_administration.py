# coding=utf-8
"""
Class for incident Administration
"""
import logging

from api.backend.processors.incident_logger import IncidentLogger
from core.backend.services import IncidentService, IncidentLogService
from base.backend.services import LogTypeService, StateService, EscalationLevelService
from django.contrib.auth.models import User

lgr = logging.getLogger(__name__)


class IncidentAdministrator(object):
	"""
	Class for Incident Administration
	"""

	@staticmethod
	def create_incident(
			name, description, state, incident_type, priority_level, system, escalation_level, message, **kwargs):
		"""
		Calls the incident logger processor to create an incident
		@param name: The name of the incident
		@type: name: str
		@param description: Details on the incident
		@type description: str
		@param state: The resolution state of the incident at creation
		@type state: str
		@param incident_type: The type of the incident i.e realtime or scheduled
		@type incident_type: str
		@param system: The system affected by the incident
		@type system: str
		@param escalation_level: Level at which to send notifications on the incident to configured users
		@type escalation_level: str
		@param message: Message to be send when notifying users on the incident
		@type message: str
		@param priority_level: Level of importance assigned to the incident
		@type priority_level: str
		@param kwargs: Extra key-value arguments to be passed for incident creation
		@return: Response code and data to indicate if the incident was created or not
		@rtype: dict
		"""
		incident = IncidentLogger().log_incident(
			name = name, description = description, state = state, incident_type = incident_type, system = system,
			escalation_level = escalation_level, message = message, priority_level = priority_level,
		)
		if incident.get('code') != '800.200.001':
			return {'code': incident.get('code'), 'data': 'Incident creation failed'}
		return {'code': '800.200.001', 'data': 'Incident created successfully'}

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
				description = description, incident = incident, user = User.objects.get(username = user),
				log_type = log_type, priority_level = priority_level, state = StateService().get(name = state)
			)
			if incident_log:
				notification = IncidentLogger().send_notification(
					incident = incident.name, escalation_level = escalation_level.name,
					message = description, asignee = incident_log.user
				)
				if notification.get('code') != '800.200.001':
					lgr.error('Notification on incident %s update failed' % incident)
				return {'code': '800.200.001', 'data': 'Incident updated successfully'}
		except Exception as ex:
			lgr.exception("Incident Administration exception %s" % ex)
		return {'code': '800.200.001', 'data': 'Failed to update the incident'}
