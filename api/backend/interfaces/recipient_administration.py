import logging

from django.contrib.auth.models import User
from django.db.models import F

from core.backend.services import SystemService, RecipientService, SystemRecipientService
from base.backend.services import StateService, EscalationLevelService, NotificationTypeService

lgr = logging.getLogger(__name__)


class RecipientAdministrator(object):
	"""
	class for recipient Administration
	"""

	@staticmethod
	def create_recipient(first_name, last_name, email, phone_number, user_id, state_id, system_id,
	                     escalation_level_id, notification_type_id):
		"""
		@param first_name: first name of the recipient to be created
		@type first_name:str
		@param last_name:last name of the recipient to be created
		@type last_name:str
		@param email: email of the recipient to be created
		@type email:str
		@param phone_number:phone number of the recipient to be created
		@type phone_number:str
		@param user_id: id of the user the recipient belongs to
		@type user_id:str
		@param state_id: id of the initial state the recipient will have
		@type state_id:str
		@param system_id:id of the system the recipient will belong to
		@type system_id:str
		@param escalation_level_id:id of the escalation level the recipient will be tied to
		@type escalation_level_id:str
		@param notification_type_id:id of notification_type the recipient will be tied to
		@type notification_type_id: str
		@return:Response code dictionary to indicate if the recipient was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().get(id = system_id)
			state = StateService().get(id = state_id)
			escalation_level = EscalationLevelService().get(id = escalation_level_id)
			user = User.objects.get(id = int(user_id))
			notification_type = NotificationTypeService().get(id = notification_type_id)

			if not (system and state and escalation_level and user and notification_type and first_name and last_name
			        and email and phone_number):
				return {"code": "800.400.002", "message": "invalid required parameters"}
			# check if a recipient with the details given exist
			exist = RecipientService().filter(user = user)
			if exist:
				system_recipient = RecipientAdministrator.create_system_recipient(system = system, state = state,
				                                                                  escalation_level = escalation_level,
				                                                                  recipient = exist)
				if system_recipient.get("code") == "200.400.009":
					return {"code": "200.400.008", "message": "Recipient already exist consider updating the recipient"}
				return {"code": "800.200.001", "message": "system recipient successfully created"}
			recipient = RecipientService().create(
				first_name = first_name, last_name = last_name, email = email, user = user, phone_number = phone_number,
				notification_type = notification_type, state = state
			)
			if recipient:
				system_recipient = RecipientAdministrator.create_system_recipient(
					recipient = recipient, system = system, state = state, escalation_level = escalation_level
				)
				if system_recipient.get("code") != '800.200.001':
					return {"code": "800.400.002", "message": "Error while creating system recipient"}
				return {"code": "800.200.001", "message": "recipient successfully created"}

		except Exception as ex:
			lgr.exception("Recipient Administration Exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error while creating a recipient"}

	@staticmethod
	def create_system_recipient(escalation_level, system, recipient, state):
		"""

		@param escalation_level: an escalation level object
		@type escalation_level:object
		@param system: a system object
		@type system:object
		@param recipient: a recipient object
		@type recipient:object
		@param state: a state object
		@type state:object
		@return: Response code dictionary to indicate if the endpoint was created or not
		@rtype:dict
		"""
		try:
			system_recipient = SystemRecipientService().filter(system = system, escalation_level = escalation_level,
			                                                   recipient = recipient)
			if system_recipient:
				return {"code": "200.400.009", "message": "System recipient already exist"}
			SystemRecipientService().create(system = system, recipient = recipient, escalation_level = escalation_level,
			                                state = state)
			return {"code": "800.200.001", "message": "successfully created system_recipient"}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception %s" % ex)

	@staticmethod
	def update_recipient(recipient_id, system_recipient_id, notification_type_id, state_id, first_name, last_name,
	                     email, phone_number):
		"""
		@param system_recipient_id:  id of the system_recipient
		@type system_recipient_id:str
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
			updated_system_recipient = SystemRecipientService().get(id = system_recipient_id)
			notification_type = NotificationTypeService().get(id = notification_type_id)
			state = StateService().get(id = state_id)
			if not (state and updated_recipient and updated_system_recipient and first_name and last_name and
			        email and phone_number and notification_type):
				return {"code": "800.400.002", "message": "missing parameters"}
			recipient = RecipientService().update(pk = recipient_id, first_name = first_name, last_name = last_name,
			                                      email = email,
			                                      notification_type = notification_type, phone_number = phone_number)
			if recipient:
				system_recipient = RecipientAdministrator.update_system_recipient(
					system_recipient_id = system_recipient_id, state = state)
				if system_recipient.get('code') == '800.200.001':
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
	def get_system_recipients(system_id, escalation_level_id):
		"""
		@param system_id:id of the system the recipients belong to
		@type system_id: str
		@param escalation_level_id: id of the escalation level the recipient belong to
		@type escalation_level_id:str
		@return:recipients:a dictionary containing a success code and a list of dictionaries containing  system
							recipients data
		@rtype:dict
		"""

		try:
			recipients = {}
			system = SystemService().get(id = system_id)
			escalation_level = EscalationLevelService().get(id = escalation_level_id)
			if not (system and escalation_level):
				return {"code": "800.400.002", "message": "It seems there is no existing system"}
			system_recipients = list(SystemRecipientService().filter(system = system,
			                                                         escalation_level = escalation_level).values(
				'id', 'escalation_level__name', 'state__name', first_name = F(
					'recipient__first_name'),
				last_name = F('recipient__last_name'), phone_number = F('recipient__phone_number'),
				email = F('recipient__email'), recipient_id = F('recipient__id'),
				notification_type = F('recipient__notification_type__name')
			).order_by('-date_created'))
			recipients.update(recipients = system_recipients)
			return {'code': '800.200.001', 'data': recipients}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception:  %s" % ex)
		return {"code": "800.400.001", "message": "Error while fetching recipients"}

	@staticmethod
	def get_system_recipient(system_id, recipient_id, escalation_level_id):
		"""
		@param system_id: id of the system the recipient belongs to
		@type system_id: str
		@param recipient_id:id of the recipient belong you are fetching
		@type recipient_id: str
		@param escalation_level_id: id of the escalation level the recipient belong to
		@type escalation_level_id:str
		@return:recipients:a dictionary containing a success code and a list of dictionaries containing  system
							recipient data
		@rtype:dict
		"""

		try:
			data = {}
			system = SystemService().get(id = system_id)
			recipient = RecipientService().get(id = recipient_id)
			escalation_level = EscalationLevelService().get(id = escalation_level_id)
			if not (system and recipient and escalation_level):
				return {"code": "800.400.002", "message": "It seems there is no such recipient"}
			system_recipient = list(SystemRecipientService().filter(recipient = recipient, system = system,
			                                                        escalation_level = escalation_level).values(
				'id', 'escalation_level__name', 'state__name', first_name = F(
					'recipient__first_name'),
				last_name = F('recipient__last_name'), phone_number = F('recipient__phone_number'),
				email = F('recipient__email'), recipient_id = F('recipient__id'),
				notification_type = F('recipient__notification_type__name')
			))
			data.update(recipient = system_recipient)
			return {'code': '800.200.001', 'data': data}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception:  %s" % ex)
		return {"code": "800.400.001", "message": "Error while fetching recipient"}
