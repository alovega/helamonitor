# coding=utf-8
"""
Class for creating new incidents and logging incident updates
"""
import logging

from core.backend.services import NotificationService, SystemRecipientService
from base.backend.services import StateService, NotificationTypeService

import datetime

lgr = logging.getLogger(__name__)


class NotificationLogger(object):

	@staticmethod
	def send_notification(message, message_type, recipients):
		"""
		Create and sends a notification
		@param message: a string of the content to be sent
		@type:str
		@param message_type: a notification_type object
		@type: str
		@param recipients: a list of recipients
		@type:list
		@return: returns a dict of a code for success or failure
		@rtype: dict
		"""
		try:
			for recipient in recipients:
				data = NotificationService().create(
					message = message,
					notification_type = NotificationTypeService().get(name = message_type),
					recipient = recipient,
					state = StateService().get(name = 'Active')
				)
				if data:
					if str(message_type) == 'Email':
						system = SystemRecipientService().get(recipient__email = data.recipient, state__name = 'Active')
					else:
						system = SystemRecipientService().get(
							recipient__phone_number = data.recipient.phone_number, state__name = 'Active'
						)
					message = {
						"destination": data.recipient, "message_type": data.notification_type.name,
						"lang": None,
						"corporate_id": system.system.id, "message_code": 'HPS0006',
						"replace_tags": {
							"code": None, 'corporate': system.system.name,
							'date': datetime.date.today().strftime('%d/%m/%y'),
							'time': datetime.datetime.now().time().strftime('%I:%M%p')
						}
					}
					# to do a call to notification API check if it returns a code for success
					if message:
						print NotificationService().update(data.id, state = StateService().get(name = 'Sent'))
					else:
						print NotificationService().update(data.id, state = StateService().get(name = 'Failed'))
						lgr.warn("Message sending failed %s" % message)
				return {"code": "200.400.005"}
			return {"code": "800.200.001"}
		except Exception as e:
			lgr.exception("Notification logger exception %s" % e)
