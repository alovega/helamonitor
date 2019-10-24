# coding=utf-8
"""
Class for User Administration
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


class UserAdministrator(object):
	"""
	Class for User Administration
	"""

	@staticmethod
	def create_user(username, password, email, first_name, last_name, **kwargs):
		"""
		Creates a user.
		@param username: Username of the user to be created
		@type username: str
		@param email: Email of the user to be created
		@type email: str
		@param password: Password of the user to be created
		@type password: str
		@param first_name: First name of the user
		@type first_name: str
		@param last_name: Last name of the user
		@type last_name: str
		@param kwargs: Extra key-value arguments to pass for user creation
		@return: Response code dictionary to indicate if the user was created or not
		@rtype: dict
		"""
		try:
			user = User.objects.create_user(username, email, password, first_name = first_name, last_name = last_name)
			if user:
				user = User.objects.filter(id = user.id).values()[0]
				return {'code': '800.200.001', 'data': user}
		except Exception as ex:
			lgr.exception("Escalation Rule Creation exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def update_user(
			user_id, username = None, password = None, email = None, first_name = None, last_name = None, **kwargs):
		"""
		Updates a user.
		@param user_id: Id of the user to be updated
		@type user_id: str
		@param username: Username of the user to be created
		@type username: str | None
		@param email: Email of the user to be created
		@type email: str | None
		@param password: Password of the user to be created
		@type password: str | None
		@param first_name: First name of the user
		@type first_name: str | None
		@param last_name: Last name of the user
		@type last_name: str | None
		@param kwargs: Extra key-value arguments to pass for user creation
		@return: Response code dictionary to indicate if the user was created or not
		@rtype: dict
		"""
		try:
			user = User.objects.get(id = user_id)
			if user:
				user.username = username if username else user.username
				user.email = email if email else user.email
				user.first_name = first_name if first_name else user.first_name
				user.last_name = last_name if last_name else user.last_name
				if password is not None:
					user.set_password(password)
				user = User.objects.filter(id = user.id).values()[0]
				return {'code': '800.200.001', 'data': user}
		except Exception as ex:
			lgr.exception("User Update exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def get_user(user_id, **kwargs):
		"""
		Retrieves a user.
		@param user_id: The id of the user to be retrieved
		@type user_id: str
		@param kwargs: Extra key-value arguments to pass for user retrieval
		@return: Response code dictionary to indicate if the user was retrieved or not
		@rtype: dict
		"""
		try:
			user = User.objects.filter(id = user_id).values()[0]
			if not user:
				return {"code": "800.400.002"}
			return {'code': '800.200.001', 'data': user}
		except Exception as ex:
			lgr.exception("Get User exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def get_users(**kwargs):
		"""
		Retrieves all users.
		@param kwargs: Extra key-value arguments to pass for user retrieval
		@return: Response code dictionary to indicate if all users were retrieved or not
		@rtype: dict
		"""
		try:
			users = list(User.objects.filter().values().order_by('-date_joined'))
			if users:
				return {'code': '800.200.001', 'data': users}
		except Exception as ex:
			lgr.exception("Get Users exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def delete_user(rule_id, system_id, **kwargs):
		"""
		Deletes an escalation rule for a selected system.
		@param rule_id: The id of the rule to be deleted
		@type rule_id: str
		@param system_id: System where the escalation rule is defined in
		@type system_id: str
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().filter(pk = system_id, state__name = 'Active').first()
			if system is None:
				return {"code": "800.400.002"}
			escalation_rule = EscalationRuleService().filter(pk = rule_id, system = system).first()
			if escalation_rule:
				if escalation_rule.delete():
					return {'code': '800.200.001', 'Message': 'Rule deleted successfully'}
		except Exception as ex:
			lgr.exception("Escalation Rule Update exception %s" % ex)
		return {"code": "800.400.001"}
