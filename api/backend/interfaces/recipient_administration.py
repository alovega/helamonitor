import logging

from django.contrib.auth.models import User
from django.db.models import F

from core.backend.services import SystemService, RecipientService, SystemRecipientService
from core.models import Recipient
from base.backend.services import StateService, EscalationLevelService, NotificationTypeService

lgr = logging.getLogger(__name__)


class RecipientAdministrator(object):
	"""
	class for recipient Administration
	"""

	@staticmethod
	def get_recipients():
		"""
		@return: response code dictionary for success or failure and a dictionary containing list of recipients
		@rtype: dict
		"""
		try:
			recipients = list(RecipientService().filter().values(
				userName=F('user__username'), phoneNumber=F('phone_number'), status=F('state__name'),
				dateCreated=F('date_created'), recipientId= F('id')))
			return {'code': '800.200.001', 'data': recipients}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception: %s" % ex)
		return {'code': '800.400.001', 'message': 'Error while getting system recipients'}

	@staticmethod
	def get_recipient(recipient_id):
		"""
		@param recipient_id: Id of the recipient that you want to fetch
		@type:str
		@return: a response code dictionary indicating success or failure and a dictionary of fetched recipient
		@rtype: dict
		"""
		try:
			recipient = list(RecipientService().filter(id = recipient_id).values(
				userName = F('user__username'), phoneNumber = F('phone_number'), status = F('state__name'),
				dateCreated= F('date_created'), recipientId = F('id')))
			return {'code': '800.200.001', 'data': recipient}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception: %s" % ex)
		return {'code': '800.400.001 %s' %ex, 'message': 'Error while getting recipient'}

	@staticmethod
	def create_recipient(user_id, phone_number, state_id):
		"""

		@param user_id: the id of the user the recipient is tied to
		@type: str
		@param phone_number: phone number of the recipient
		@type: str
		@param state_id: the id of the state the recipient will have
		@type: str
		@return: a response code dictionary indicating success or failure and a dictionary of created  recipient
		@rtype:dict
		"""
		try:
			if not (user_id and phone_number and state_id):
				return {"code": "800.400.002", "message": "invalid required "
				                                                                            "parameters"}
			if RecipientService().filter(user__id = user_id):
				return {"code": "800.400.001", "message": "user already tied to a recipient"}
			RecipientService().create(
				user=User.objects.get(id=user_id), phone_number=phone_number, state=StateService().get(id=state_id))
			return {"code": "800.200.001", "message": "successfully created a recipient"}
		except Exception as ex:
			lgr.exception('Recipient Administration Exception: %s' % ex)
		return {"code": "800.400.001", "message": "Error while creating recipient"}

	@staticmethod
	def update_recipient(recipient_id, phone_number, state_id):
		"""

		@param recipient_id:Id of the recipient you want to update
		@type:str
		@param phone_number: phone number of the recipient
		@type:str
		@param state_id:id of the state
		@type: str
		@return:a response code dictionary indicating success or failure and a dictionary of created  recipient
		@rtype:dict
		"""
		try:
			if not (recipient_id and phone_number and state_id):
				return {"code": "800.400.002", "message": "invalid required parameters"}
			RecipientService().update(pk = recipient_id, phone_number=phone_number, state=StateService().get(
										id=state_id))
			return {"code": "800.200.001", "message": "successfully updated the recipient"}
		except Exception as ex:
			lgr.exception('Recipient Administration Exception: %s' % ex)
		return {"code": "800.400.001", "message": "Error while updating recipient"}

	@staticmethod
	def update_system_recipient(recipient_id, notification_type_id, state_id, first_name, last_name, email,
	                           phone_number):
		"""
		@param recipient_id:id of the recipient that is going to be edited
		@type recipient_id: str
		@param notification_type_id:id of the notification_type the recipient will be tied to
		@type notification_type_id:str
		@param state_id:id of the state the updated recipient will have
		@type state_id:str
		@param first_name:first name of the recipient to be updated
		@type first_name:str
		@param last_name:last name of the recipient to be updated
		@type last_name:str
		@param email:email of the recipient to be updated
		@type email:str
		@param phone_number: phone number of the recipient to be updated
		@type phone_number:str
		@return:Response code dictionary to indicate if the recipient was updated or not
		@rtype:dict
		"""
		try:
			updated_recipient = RecipientService().get(id = recipient_id)
			notification_type = NotificationTypeService().get(id = notification_type_id)
			state = StateService().get(id = state_id)
			if not (state and updated_recipient and notification_type):
				return {"code": "800.400.002", "message": "missing parameters"}
			recipient = RecipientService().update(pk = recipient_id, first_name = first_name, last_name = last_name,
			                                      email = email,
			                                      notification_type = notification_type, phone_number = phone_number)
			if recipient:
				return {"code": "800.200.001", "message": "successfully updated system recipient"}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception:  %s" % ex)
		return {"code": "800.400.001", "message": "Error while updating recipient"}

	@staticmethod
	def update_system_recipient(system_recipient_id, state):
		"""
		@param system_recipient_id:id of the system recipient to be updated
		@type system_recipient_id:str
		@param state: state object
		@type state: object
		@return: Response code dictionary to indicate if the system_recipient was updated or not
		@rtype:dict
		"""
		try:
			SystemRecipientService().update(pk = system_recipient_id, state = state)
			return {"code": "800.200.001", "message": "successfully updated system recipient"}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error while updating System recipient"}

	@staticmethod
	def get_system_recipients(system_id):
		"""
		@param system_id:id of the system the recipients belong to
		@type system_id: str
		@return:recipients:a dictionary containing a success code and a list of dictionaries containing  system
							recipients data
		@rtype:dict
		"""

		try:
			data = {}
			system = SystemService().get(id = system_id)
			if not system:
				return {"code": "800.400.002", "message": "It seems there is no existing system"}
			recipients = list(RecipientService().filter().values(
				userName = F('user__username'), recipientId = F('id'), status=F('state__name')))
			for recipient in recipients:
				system_recipients = list(SystemRecipientService().filter(
					system = system, recipient__id = recipient.get('recipientId')).values(
					escalationLevels = F('escalation_level__name'), status = F('state__name'), Id=F('id'),
				).order_by('-date_created'))
				recipient.update(system_recipients = system_recipients)
			recipients = [recipient for recipient in recipients if recipient.get('system_recipients')]
			data.update(recipients = recipients)
			return {'code': '800.200.001', 'data': recipients}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception:  %s" % ex)
		return {"code": "800.400.001 %s" % ex, "message": "Error while fetching recipients"}

	@staticmethod
	def get_system_recipient(recipient_id):
		"""
		@param recipient_id:id of the recipient belong you are fetching
		@type recipient_id: str
		@return:recipients:a dictionary containing a success code and a list of dictionaries containing  system
							recipient data
		@rtype:dict
		"""

		try:
			data = {}
			recipient = list(RecipientService().filter(id = recipient_id).values(
				'state__name', 'first_name', 'last_name', 'phone_number',
				'email', 'notification_type__name', recipient_id = F('id'),
			))
			if recipient:
				data.update(recipient = recipient)
				return {'code': '800.200.001', 'data': data}
			return {'code': '800.400.001', 'message': 'No such recipient with the given id'}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception:  %s" % ex)
		return {"code": "800.400.001", "message": "Error while fetching recipient"}

	@staticmethod
	def delete_recipient(recipient_id):
		"""
		@param recipient_id:id of the recipient belong you are fetching
		@type recipient_id: str
		@return:recipients:a dictionary containing a success code and a list of dictionaries containing  system
							recipient data
		@rtype:dict
		"""
		try:
			if not recipient_id:
				return {"code": "800.400.002", "message": "invalid parameter"}
			recipient = Recipient.objects.get(id = recipient_id)
			recipient.delete()
			return {'code': '800.200.001', 'message': 'successfully deleted the recipient'}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error while deleting recipient"}
