import logging

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

		@param first_name:
		@type first_name:str
		@param last_name:
		@type last_name:str
		@param email:
		@type email:str
		@param phone_number:
		@type phone_number:str
		@param user_id:
		@type user_id:str
		@param state_id:
		@type state_id:str
		@param system_id:
		@type system_id:str
		@param escalation_level_id:
		@type escalation_level_id:str
		@param notification_type_id:
		@type notification_type_id: str
		@return:
		@rtype: dict
		"""
		pass

	@staticmethod
	def update_recipient(recipient_id, notification_type_id, escalation_level_id, state_id, first_name, last_name,
	                     email, phone_number):
		"""

		@param recipient_id:
		@type recipient_id: str
		@param notification_type_id:
		@type notification_type_id:str
		@param escalation_level_id:
		@type escalation_level_id:str
		@param state_id:
		@type state_id:str
		@param first_name:
		@type first_name:str
		@param last_name:
		@type last_name:str
		@param email:
		@type email:str
		@param phone_number:
		@type phone_number:str
		@return:
		@rtype:dict
		"""

		pass

	@staticmethod
	def get_system_recipients(system_id):
		"""

		@param system_id:
		@type system_id: str
		@return:
		@rtype:dict
		"""
