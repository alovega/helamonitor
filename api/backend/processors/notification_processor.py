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
	def send_notification(incident, message, escalation_level = None, assignee = None):

		notifications_data = []
		try:
			if escalation_level is not None:
				recipients = SystemRecipientService().filter(
					status__name = 'Active', escalation_level = escalation_level, system = incident.system
				)
				for recipient in recipients:
					if recipient.phone_number and recipient.email:
						notification_data1 = {
							"message": message, "notification_type": NotificationTypeService().get('SMS'),
							"recipient": recipient, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notification_data2 = {
							"message": message, "notification_type": NotificationTypeService().get('Email'),
							"recipient": recipient, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.extend((notification_data1, notification_data2))
					elif recipient.phone_number is not None:
						notification_data = {
							"message": message, "notification_type": NotificationTypeService().get('SMS'),
							"recipient": recipient, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.append(notification_data)
					else:
						notification_data = {
							"message": message, "notification_type": NotificationTypeService().get('Email'),
							"recipient": recipient, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.append(notification_data)
				else:

					if assignee.phone_number and assignee.email:
						notification_data1 = {
							"message": message, "notification_type": NotificationTypeService().get('email'),
							"recipient": assignee, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notification_data2 = {
							"message": message, "notification_type": NotificationTypeService().get('SMS'),
							"recipient": assignee, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.extend((notification_data1, notification_data2))
					elif assignee.phone_number:
						notification_data = {
							"message": message, "notification_type": NotificationTypeService().get('SMS'),
							"recipient": assignee, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.append(notification_data)
					else:
						data = {
							"message": message, "notification_type": NotificationTypeService().get('SMS'),
							"recipient": assignee, "incident": incident, "system": incident.system,
							"state": StateService().get(name = 'Active')
						}
						notifications_data.append(data)
				for notification in notifications_data:

					data = NotificationService().create(
						message = notification.get('message'),
						notification_type = notification.get('notification_type'),
						recipient = notification.get('recipient'), incident = notification.get('incident'),
						system = notification.get('system'), state = notification.get('state'),
					)

					if message:
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
					return {"code": "200.400.005"}
				return {"code": "800.200.001"}

		except Exception as e:
			lgr.exception("Notification logger exception %s" % e)



