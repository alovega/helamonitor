# coding=utf-8
"""
Class for Systems Administration
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


class SystemAdministrator(object):
	"""
	Class for Systems Administration
	"""

	@staticmethod
	def create_system(name, description, admin_id = None, **kwargs):
		"""
		Creates an escalation rule for a selected system.
		@param name: Name of the system to be created
		@type name: str
		@param description: Details on the System
		@type description: str
		@param admin_id: Admin user of the system
		@type admin_id: str | None
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().create(
				name = name, description = description, state = StateService().get(name = 'Active'), admin = admin_id)

			if system:
				system = SystemService().filter(pk = system.id).values(
					'name', 'id', 'description', 'date_created', 'date_modified', 'version', status = F('state__name'),
					admin_id = F('admin')).first()
			return {"code": "800.200.001", 'data': system}
		except Exception as ex:
			lgr.exception("System creation exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def update_system(system_id, name = None, description = None, state = None, **kwargs):
		"""
		Updates a system.
		@param system_id: Id of the system
		@type system_id: str | None
		@param name: Name of the system
		@type name: str | None
		@param description: Details on the System
		@type description: str | None
		@param state: State of the System
		@type state: str | None
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system_id, state__name = 'Active')
			if not system:
				return {'code': '800.400.200'}
			name = name if name is not None else system.name
			description = description if description is not None else system.description
			updated_system = SystemService().update(pk = system.id, name = name, description = description)
			if updated_system:
				updated_system = SystemService().filter(pk = system.id).values(
					'name', 'id', 'description', 'date_created', 'date_modified', 'version', status = F('state__name'),
					admin_id = F('admin')).first()
				return {'code': '800.200.001', 'data': updated_system}
		except Exception as ex:
			lgr.exception("Escalation Rule Update exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def get_system(system_id, **kwargs):
		"""
		Retrieves a system.
		@param system_id: Id of the system to be retrieved
		@type system_id: str | None
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().filter(pk = system_id, state__name = 'Active').values(
					'name', 'id', 'description', 'date_created', 'date_modified', 'version', status = F('state__name'),
					admin_id = F('admin')).first()
			if system is None:
				return {"code": "800.400.002"}
			return {'code': '800.200.001', 'data': system}
		except Exception as ex:
			lgr.exception("Escalation Rule Update exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def get_systems():
		"""
		Retrieves all active Systems.
		@return: Response code dictionary to indicate if the systems were retrieved or not
		@rtype: dict
		"""
		try:
			systems = list(SystemService().filter(state__name = 'Active').values(
					'name', 'id', 'description', 'date_created', 'date_modified', 'version', status = F('state__name'),
					admin_id = F('admin')))
			if systems is None:
				return {"code": "800.400.002"}
			return {'code': '800.200.001', 'data': systems}
		except Exception as ex:
			lgr.exception("Escalation Rule Update exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def delete_system(system_id, **kwargs):
		"""
		Deletes a system.
		@param system_id: System to be deleted
		@type system_id: str
		@return: Response code dictionary to indicate if the system was deleted or not
		@rtype: dict
		"""
		try:
			system = SystemService().filter(pk = system_id).first()
			if system is None:
				return {"code": "800.400.002"}
			if system.delete():
				return {'code': '800.200.001', 'Message': 'System deleted successfully'}
		except Exception as ex:
			lgr.exception("Escalation Rule Update exception %s" % ex)
		return {"code": "800.400.001"}
