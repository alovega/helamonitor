# coding=utf-8
"""
Class for User Administration
"""
import calendar
from datetime import timedelta
from django.utils import timezone
from django.db import IntegrityError

import logging
import dateutil.parser
from core.models import User
from django.db.models import F, Q
from api.models import token_expiry
from api.backend.interfaces.notification_interface import NotificationLogger
from core.backend.services import RecipientService, EscalationRuleService
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
			if User.objects.filter(username = username).exists():
				return {"code": "800.400.001", 'message': 'Username already in use'}
			if User.objects.filter(email = email).exists():
				return {"code": "800.400.001", 'message': 'Email already in use'}
			user = User.objects.create_user(username, email, password, first_name = first_name, last_name = last_name)
			user = User.objects.filter(id = user.id).values().first()
			if user:
				return {'code': '800.200.001', 'data': user}
		except Exception as ex:
			lgr.exception("UserCreation exception %s" % ex)
		return {"code": "800.400.001", 'message': 'User could not be created'}

	@staticmethod
	def update_user(
			user_id, username = None, email = None, first_name = None, last_name = None, **kwargs):
		"""
		Updates a user.
		@param user_id: Id of the user to be updated
		@type user_id: str
		@param username: Username of the user to be created
		@type username: str | None
		@param email: Email of the user to be created
		@type email: str | None
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
				user.save()
				user = User.objects.filter(id = user.id).values().first()
				if user:
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
			user = User.objects.filter(id = user_id).values().first()
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
		@type token:char
		@param kwargs: Extra key arguments passed to the method
		@return: Response code dictionary
		"""
		try:
			app_user = OauthService().filter(token = token).values('app_user').first()
			user = AppUserService().filter(id = app_user.get('app_user')).values(userName = F(
				'user__username'), email = F('user__email'), superUser = F('user__is_superuser'), firstName = F(
				'user__first_name'), lastName = F('user__last_name'), log = F('user__logentry'),
				staff = F('user__is_staff'), phoneNumber = F('user__recipient__phone_number'), password = F(
					'user__password')).first()
			if user.get('superUser'):
				user.update(role = 'Admin')
			elif user.get('staff'):
				user.update(role = 'Staff')
			else:
				user.update(role = 'User')
			return {'code': '800.200.001', "data": user}
		except Exception as ex:
			lgr.exception("Logged in user exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def edit_logged_in_user_details(
			token, username = None, first_name = None, last_name = None, phone_number = None, email = None,
			**kwargs):
		"""
		@param email: Email of the user
		@type token: str
		@param phone_number: phone_number of the user
		@type phone_number: str
		@param last_name: Users last name
		@type last_name: str
		@param first_name:
		@param username:
		@param token: the token of a logged in user
		@type:str
		@param kwargs: Extra key arguments passed to the method
		@return:Response code dictionary indicating if the update was okay
		"""
		try:
			user_id = OauthService().filter(token = token).values(userId=F('app_user__user__id')).first()
			user = User.objects.get(id = user_id.get('userId'))
			recipient = RecipientService().get(user__id = user_id.get('userId'))
			if user:
				user.username = username if username else user.username
				user.email = email if email else user.email
				user.first_name = first_name if first_name else user.first_name
				user.last_name = last_name if last_name else user.last_name
				user.save()
				if recipient:
					if phone_number:
						RecipientService().update(pk=recipient.id, phone_number=phone_number)
				updated_user = User.objects.filter(id = user_id.get('userId')).values().first()
				return {'code': '800.200.001', "data": updated_user}
		except Exception as ex:
			lgr.exception("Logged in user exception: %s" % ex)
		return {"code": "800.400.001", "message": "Logged in user update fail"}

	@staticmethod
	def edit_logged_in_user_password(token, current_password=None, new_password=None, **kwargs):
		"""
		@param token: the token of the logged in user
		@type: str
		@param current_password: password of the logged in user
		@type:str
		@param new_password:new password of the logged in user
		@type:str
		@return:Response code dictionary indicating if the password update was okay
		"""
		try:
			user_id = OauthService().filter(token = token).values('app_user__user__id').first()
			user = User.objects.get(id = user_id.get("app_user__user__id"))
			if user:
				if not user.check_password(current_password):
					return{"code": "800.400.001", "message": "Current password given is invalid"}
				user.set_password(new_password)
				user.save()
				return {"code": "800.200.001", "message": "Password successfully updated"}
		except Exception as ex:
			lgr.exception("Logged in user exception: %s" % ex)
		return {"code": "800.400.001", "message": "logged in user password update fail"}

	@staticmethod
	def verify_token(token, **kwargs):
		"""
		Verifies the access token granted to a user
		@param token: The authorization token
		@type token: str
		@param kwargs: Extra key-value arguments that can be passed into the method
		@return: A response code indicating status and the access token
		"""
		try:
			oauth = OauthService().filter(
				token = token, expires_at__gte = timezone.now(), state__name = 'Active').first()
			if oauth is None:
				return {'code': '800.400.002'}
			if OauthService().update(pk = oauth.id, expires_at = token_expiry()) is not None:
				updated_oauth = OauthService().filter(pk = oauth.id).first()
				return {'code': '800.200.001', 'data': {
					'token': str(updated_oauth.token), 'expires_at': calendar.timegm(
						updated_oauth.expires_at.timetuple())}}
		except Exception as ex:
			lgr.exception('Verify Token Exception %s' % ex)
		return {'code': '800.400.001'}
