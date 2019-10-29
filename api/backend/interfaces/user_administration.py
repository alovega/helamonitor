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
from api.backend.services import OauthService, AppUserService

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
	def delete_user(user_id, **kwargs):
		"""
		Deletes a user from a selected system.
		@param user_id: The id of the user to be deleted
		@type user_id: str
		@param kwargs: Extra key-value arguments to pass for user deletion
		@return: Response code dictionary to indicate if the user was deleted or not
		@rtype: dict
		"""
		try:
			user = User.objects.filter(pk = user_id).first()
			if user is None:
				return {"code": "800.400.002"}
			if user:
				if user.delete():
					return {'code': '800.200.001', 'Message': 'User deleted successfully'}
		except Exception as ex:
			lgr.exception("Delete user exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def get_logged_in_user_details(token, **kwargs):
		"""

		@param token: the generated token of the user
		@type:char
		@param kwargs: Extra key arguments passed to the method
		@return: Response code dictionary
		"""
		try:
			app_user = list(OauthService().filter(token = token).values('app_user'))
			user = list(AppUserService().filter(id = app_user[0].get('app_user')).values(userName = F(
				'user__username'), email = F('user__email'), superUser = F('user__is_superuser'), firstName = F(
				'user__first_name'), lastName = F('user__last_name'), log = F('user__logentry'),
				staff = F('user__is_staff'), phoneNumber = F('user__recipient__phone_number'), password = F(
					'user__password')))
			if user[0].get('superUser'):
				user.update(role = 'Admin')
			elif user[0].get('staff'):
				user[0].update(role = 'Staff')
			else:
				user[0].update(role = 'User')
			return {'code': '800.200.001', "data": user}
		except Exception as ex:
			lgr.exception("Logged in user exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def edit_logged_in_user_details(
			token, username = None, first_name = None, last_name = None, phone_number = None, email = None,
			password = None,
			**kwargs):
		"""
		@param password: password for user
		@type:str
		@param email: Email of the user
		@type:str
		@param phone_number: phone_number of the user
		@type:str
		@param last_name: Users last name
		@type: str
		@param first_name:
		@param username:
		@param token: the token of a logged in user
		@type:str
		@param kwargs: Extra key arguments passed to the method
		@return:Response code dictionary if the update was okay
		"""
		try:
			user_id = list(OauthService().filter(token = token).values('app_user__user__id'))
			user__id = user_id[0].get('app_user__user__id')
			user = User.objects.get(id = user__id)
			recipient = list(RecipientService().filter(user__id = user__id).values())
			if user:
				user.username = username if username else user.username
				user.email = email if email else user.email
				user.first_name = first_name if first_name else user.first_name
				user.last_name = last_name if last_name else user.last_name
				if password is not None:
					user.set_password(password)
				user.save()
				if recipient:
					recipient[0]['phone_number'] = phone_number if phone_number else recipient[0]['phone_number']
				updated_user = User.objects.filter(id = user__id).values()[0]
				return {'code': '800.200.001', "data": updated_user}
		except Exception as ex:
			lgr.exception("Logged in user exception %s" % ex)
		return {"code": "800.400.001 %s" % ex}
