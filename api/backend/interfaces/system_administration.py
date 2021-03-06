# coding=utf-8
"""
Class for Systems Administration
"""
from datetime import timedelta
import logging
import dateutil.parser
from core.models import User
from django.db.models import F, Q

from api.backend.interfaces.notification_interface import NotificationLogger
from core.backend.services import IncidentLogService, IncidentEventService, SystemService, \
	SystemRecipientService,  EscalationRuleService
from base.backend.services import StateService, EscalationLevelService, EventTypeService, IncidentTypeService

lgr = logging.getLogger(__name__)


class SystemAdministrator(object):
	"""
	Class for Systems Administration
	"""

	@staticmethod
	def create_system(name, description, admin_id = None, version = None, **kwargs):
		"""
		Creates an escalation rule for a selected system.
		@param name: Name of the system to be created
		@type name: str
		@param description: Details on the System
		@type description: str
		@param admin_id: Admin user of the system
		@type admin_id: str | None
		@param version: Version of the system
		@type version: str | None
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			if SystemService().get(name = name):
				return {'code': '800.400.100', 'message': 'System name already in use'}
			admin = User.objects.get(pk = admin_id)
			system = SystemService().create(
				name = name, description = description, state = StateService().get(name = 'Active'), admin = admin)
			if system:
				system = SystemService().filter(pk = system.id).values(
					'name', 'id', 'description', 'date_created', 'date_modified', 'version', state_id = F('state'),
					admin_id = F('admin')).first()
				return {"code": "800.200.001", 'data': system}
		except Exception as ex:
			lgr.exception("System creation exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def update_system(system, name = None, description = None, admin_id = None, version = None, **kwargs):
		"""
		Updates a system.
		@param system: Id of the system
		@type system: str | None
		@param name: Name of the system
		@type name: str | None
		@param description: Details on the System
		@type description: str | None
		@param version: Current version of the System
		@type version: str | None
		@param admin_id: The admin of the system
		@type admin_id: str | None
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system, state__name = 'Active')
			if not system:
				return {'code': '800.400.200'}
			if SystemService().get(name = name) and name != system.name:
				return {'code': '800.400.100', 'message': 'System name already in use'}
			name = name if name is not None else system.name
			description = description if description is not None else system.description
			admin_id = admin_id if admin_id is not None else system.admin_id
			version = version if version is not None else system.version
			admin = User.objects.get(id = admin_id)
			updated_system = SystemService().update(
				pk = system.id, name = name, description = description, admin = admin, version = version)
			if updated_system:
				updated_system = SystemService().filter(pk = system.id).values(
					'id', 'name', 'description', 'date_created', 'date_modified', 'version', status = F('state'),
					admin_id = F('admin')).first()
				return {'code': '800.200.001', 'data': updated_system, 'name': name}
		except Exception as ex:
			lgr.exception("System Update exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def get_system(system, name=None, **kwargs):
		"""
		Retrieves a system.
		@param name: Name of the system to be retrieved
		@type name: str | None
		@param system: Id of the system to be retrieved
		@type system: str | None
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			if name:

				system = SystemService().filter(name=name, state__name='Active').values().first()
			elif system:
				system = SystemService().filter(pk=system, state__name='Active').values(
					'id', 'name', 'description', 'date_created', 'date_modified', 'version', state_id = F('state'),
					admin_id=F('admin')).first()
			if system is None:
				return {"code": "800.400.002"}
			return {'code': '800.200.001', 'data': system}
		except Exception as ex:
			lgr.exception("Get system exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def get_systems(**kwargs):
		"""
		Retrieves all active Systems.
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the systems were retrieved or not
		@rtype: dict
		"""
		try:
			systems = list(SystemService().filter(state__name = 'Active').values(
					'id', 'name', 'description', 'date_created', 'date_modified', 'version', state_id = F('state'),
					admin_id = F('admin')))
			if systems is None:
				return {"code": "800.400.002"}
			return {'code': '800.200.001', 'data': systems}
		except Exception as ex:
			lgr.exception("Get systems exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def delete_system(system, **kwargs):
		"""
		Deletes a system.
		@param system: System to be deleted
		@type system: str
		@return: Response code dictionary to indicate if the system was deleted or not
		@rtype: dict
		"""
		try:
			system = SystemService().filter(pk = system).first()
			if system is None:
				return {"code": "800.400.002"}
			if system.delete():
				return {'code': '800.200.001', 'Message': 'System deleted successfully'}
		except Exception as ex:
			lgr.exception("Delete system exception %s" % ex)
		return {"code": "800.400.001"}
