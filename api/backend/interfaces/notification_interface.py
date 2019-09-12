# coding=utf-8
"""
Class for creating new incidents and logging incident updates
"""
import logging

from core.backend.services import NotificationService
from base.backend.services import StateService

import datetime

lgr = logging.getLogger(__name__)


class NotificationLogger(object):

	@staticmethod
	def send_notification(message, message_type, recipient):
		try:
			data = NotificationService().create(
					message = message,
					notification_type = message_type,
					recipient = recipient,
					state = StateService().get('Active')
				)
			if data:
					message1 = {
						"destination": data.recipient, "message_type": data.notification_type,
						"lang": None,
						"corporate_id": data.system__id, "message_code": 'HPS0006',
						"replace_tags": {
							"code": None, 'corporate':
								data.system, 'date': datetime.date.today().strftime('%d/%m/%y'),
							'time': datetime.datetime.now().time().strftime('%I:%M%p')
						}
					}
					# to do a call to notification API check if returns a code for success
					if message:
						NotificationService().update(id=data.id, state=StateService().get(name='Sent'))
						return {"code": "800.200.001"}
					else:
						NotificationService().update(id = data.id, state = StateService().get(name = 'Failed'))
						return {"code": "200.400.006"}
			return {"code": "200.400.005"}
		except Exception as e:
			lgr.exception("Notification logger exception %s" % e)



