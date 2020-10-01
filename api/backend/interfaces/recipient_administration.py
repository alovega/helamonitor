import logging
from django.db.models import F

from core.backend.services import SystemService, SystemRecipientService
from core.models import SystemRecipient, User
from base.backend.services import StateService, NotificationTypeService, EscalationLevelService

lgr = logging.getLogger(__name__)


class RecipientAdministrator(object):
	"""
	class for recipient Administration
	"""

	@staticmethod
	def update_system_recipient(recipient_id, escalations):
		"""
		@param recipient_id: The id of the recipient
		@type:str
		@param escalations:A list of dictionaries containing notification type id and escalation level_id
		@type:list
		@return:Response code dictionary to indicate if the recipient was updated or not
		@rtype:dict
		"""
		try:
			recipient = User.objects.get(id = recipient_id)
			if not (recipient and escalations):
				return {"code": "800.400.002", "message": "Error missing parameters"}
			for escalation in escalations:
				SystemRecipientService().update(
					pk = escalation.get('system_recipient_id'),
					notification_type = NotificationTypeService().get(id = escalation.get('notification_type_id')),
					state = StateService().get(id = escalation.get('state_id'))
				)
			return {"code": "800.200.001", "message": "Successfully updated system recipient"}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception:  %s" % ex)
		return {"code": "800.400.001", "message": "Error while updating recipient"}

	@staticmethod
	def get_system_recipient(user_id, system_id):
		"""
		@param system_id: the id of the system the recipient belongs to
		@type:str
		@param user_id: the id of the recipient
		@type: str
		@return:recipients:a dictionary containing a success code and a list of dictionaries containing  system
							recipient data
		@rtype:dict
		"""
		try:
			escalations_levels = []
			notification_types = []
			state = []
			system_recipient_id = []
			system = SystemService().get(id = system_id)
			recipient = User.objects.get(id = user_id)
			if not (system and recipient):
				return {"code": "800.400.002", "message": "missing parameters"}
			system_recipient = SystemRecipientService().filter(system = system, recipient = recipient).values(
				userName = F('recipient__username'), recipientId=F('recipient'),
				systemRecipientId = F('id')).first()
			recipients = list(SystemRecipientService().filter(system = system, recipient = recipient).values(
				'state', userName = F('recipient__username'), notificationType = F('notification_type'),
				systemRecipientId = F('id'), escalationLevel = F('escalation_level')
			))
			if system_recipient:
				for recipient in recipients:
					escalations_levels.append(recipient.get('escalationLevel'))
					notification_types.append(recipient.get('notificationType'))
					state.append(recipient.get('state'))
					system_recipient_id.append(recipient.get('systemRecipientId'))
				data = [{
					'escalation_level_id': escalations_levels[i], 'notification_type_id': notification_types[i],
					'state_id': state[i], 'system_recipient_id': system_recipient_id[i]}
					for i in range(len(escalations_levels))]
				system_recipient.update(escalationLevels = data)
				return {'code': '800.200.001', 'data': system_recipient}
			return {'code': '800.200.001', 'data': 'There is no such system recipient'}
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

	@staticmethod
	def create_system_recipient(system_id, user_id, escalations):
		"""
		@param system_id: The id of the system the recipient will belong to
		@type:str
		@param user_id: The id of the recipient
		@type:str
		@param escalations:A list of dictionaries containing notification type id and escalation level_id
		@type:list
		@return:a dictionary containing response code  and data indicating a success or failure in creation
		@rtype: dict
		"""

		try:
			system = SystemService().get(id = system_id)
			recipient = User.objects.get(id = user_id)
			if not (system and recipient and escalations):
				return {"code": "800.400.002", "message": "Invalid parameters given"}

			for escalation in escalations:
				if SystemRecipientService().filter(
						system = system, recipient = recipient,
						escalation_level = EscalationLevelService().get(id = escalation.get('EscalationLevel')),
				):
					return {
						"code": "800.400.001",
						"message": "system recipient already exist consider updating the recipient"
					}
				SystemRecipientService().create(
					system = system, recipient = recipient,
					escalation_level = EscalationLevelService().get(id = escalation.get('EscalationLevel')),
					notification_type = NotificationTypeService().get(id = escalation.get('NotificationType')),
					state = StateService().get(name = 'Active')
				)
			return {"code": "800.200.001", "message": " successfully created a system recipient"}

		except Exception as ex:
			lgr.exception("Recipient Administration Exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error while creating a system recipient"}

	@staticmethod
	def delete_system_recipient(system_recipient_id):
		"""
		@param system_recipient_id:id of the recipient belong you are fetching
		@type system_recipient_id: str
		@return:recipients:a dictionary containing a success code and a list of dictionaries containing  system
							recipient data
		@rtype:dict
		"""
		try:
			system_recipient = SystemRecipientService().get(id = system_recipient_id)
			if not system_recipient:
				return {"code": "800.400.002", "message": "invalid parameter"}
			system_recipient = SystemRecipient.objects.get(id = system_recipient_id)
			system_recipient.delete()
			return {'code': '800.200.001', 'message': 'successfully deleted the system recipient'}
		except Exception as ex:
			lgr.exception("Recipient Administration Exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error while deleting system recipient"}
