# coding=utf-8
"""
Class for creating new incidents and logging incident updates
"""
import logging

from core.backend.services import SystemRecipientService, NotificationService
from base.backend.services import StateService, NotificationTypeService

import datetime

lgr = logging.getLogger(__name__)


class NotificationLogger(object):

	@staticmethod
	def send_notification(message, message_type, recipients):
		try:
			data = NotificationService().create(
					message = notification.get('message'),
					notification_type = notification.get('notification_type'),
					recipient = notification.get('recipient'), incident = notification.get('incident'),
					system = notification.get('system'), state = notification.get('state'),
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

		except Exception as e:
			lgr.exception("Notification logger exception %s" % e)



