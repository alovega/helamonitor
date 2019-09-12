# coding=utf-8
"""
Class for creating new incidents and logging incident updates
"""
import logging

from core.backend.services import NotificationService, SystemRecipientService
from base.backend.services import StateService

import datetime

lgr = logging.getLogger(__name__)


class NotificationLogger(object):

	@staticmethod
	def send_notification(message, message_type, recipient):
		"""
		Create and sends a notification
		@param message: a string of the content to be sent
		@type:str
		@param message_type: a notification_type object
		@type: Object
		@param recipient: a user object
		@type:Object
		@return: returns a dict of a code for success or failure
		@rtype: dict
		"""
		try:
			data = NotificationService().create(
					message = message,
					notification_type = message_type,
					recipient = recipient,
					state = StateService().get(name = 'Active')
				)
			if data:
				system = SystemRecipientService().get(recipient=data.recipient, state__name='Active')
				message1 = {
					"destination": data.recipient, "message_type": data.notification_type,
					"lang": None,
					"corporate_id": system.system.id, "message_code": 'HPS0006',
					"replace_tags": {
						"code": None, 'corporate':system.system.name,
						'date': datetime.date.today().strftime('%d/%m/%y'),
						'time': datetime.datetime.now().time().strftime('%I:%M%p')
						}
					}
				# to do a call to notification API check if it returns a code for success
				if message:
					print data.id
					NotificationService().update(data.id, state= StateService().get(name='Sent'))
					return {"code": "800.200.001"}
				else:
					NotificationService().update(data.id, state = StateService().get(name = 'Failed'))
					return {"code": "200.400.006"}
			return {"code": "200.400.005"}
		except Exception as e:
			lgr.exception("Notification logger exception %s" % e)



