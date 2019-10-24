# coding=utf-8
"""
Class for creating new incidents and logging incident updates
"""
import logging

from core.backend.services import NotificationService, SystemService
from base.backend.services import StateService, NotificationTypeService

import datetime

lgr = logging.getLogger(__name__)


class NotificationLogger(object):

	@staticmethod
	def send_notification(message, message_type, recipients, system_id):
		"""
		Create and sends a notification
		@param system_id: id of the system the notification is created from
		@type system_id:str
		@param message: a string of the content to be sent
		@type:str
		@param message_type: a string indicating the notification type
		@type: str
		@param recipients: a list containing either email or Phone_number dependent on message type
		@type:list
		@return: returns a dict of a code for success or failure
		@rtype: dict
		"""
		if not (recipients and message and message_type):
			return {"code": "800.400.002"}

		try:
			for recipient in recipients:
				data = NotificationService().create(
					message = message,
					notification_type = NotificationTypeService().get(name = message_type),
					recipient = recipient,
					system_id = SystemService().get(pk=system_id),
					state = StateService().get(name = 'Active')
				)

				if data is not None:
					message_data = {
						"destination": data.recipient, "message_type": data.notification_type.name,
						"lang": None,
						"corporate_id": None, "message_code": 'HPS0006',
						"replace_tags": {
							"code": None, 'corporate': None,
							'date': datetime.date.today().strftime('%d/%m/%y'),
							'time': datetime.datetime.now().time().strftime('%I:%M%p')
						}
					}
					# to do a call to notification API check if it returns a code for success
					if message_data:
						NotificationService().update(data.id, state = StateService().get(name = 'Sent'))
					else:
						data = NotificationService().update(data.id, state = StateService().get(name = 'Failed'))
						lgr.warn("Message sending failed: %s" % data)
				else:
					return {"code": "200.400.005"}
			return {"code": "800.200.001"}
		except Exception as e:
			lgr.exception("Notification logger exception %s" % e)
		return {"code": "800.400.001", "message": "error in sending notification interface"}

	@staticmethod
	def get_system_notification(system_id):
		"""

		@param system_id: the id of the system the notification are from
		@type:str
		@return:returns a dict of a code for success or failure and data containing systems notifications
		@rtype:dict
		"""
		try:
			data = {}
			if not system_id:
				return {"code": "800.400.002", "message":"Missing parameter system_id"}
			notifications = list(NotificationService().filter(system__id= system_id).values(
				'message', 'recipient', 'notification_type__name', 'date_created', 'state__name'))
			data.update(notifications=notifications)
			return {"code": "800.200.001", "data":data}

		except Exception as ex:
			lgr.exception("Notification logger exception %s" % ex)
		return {"code": "800.400.001", "message": "error in fetching systems notifications"}
