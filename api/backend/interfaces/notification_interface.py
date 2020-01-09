# coding=utf-8
"""
Class for creating new incidents and logging incident updates
"""
import logging

from django.db.models import F
from datetime import timedelta, datetime
from django.utils import timezone

from api.backend.services import OauthService
from core.backend.services import NotificationService, SystemService, RecipientService
from base.backend.services import StateService, NotificationTypeService


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
		if not (recipients or message or message_type):
			return {"code": "800.400.002"}

		try:
			for recipient in recipients:
				data = NotificationService().create(
					message = message,
					notification_type = NotificationTypeService().get(name = message_type),
					recipient = recipient,
					system = SystemService().get(pk=system_id),
					state = StateService().get(name = 'Active')
				)

				if data is not None:
					message_data = {
						"destination": data.recipient, "message_type": data.notification_type.name,
						"lang": None,
						"corporate_id": None, "message_code": 'HPS0006',
						"replace_tags": {
							"code": None, 'corporate': None,
							'date': datetime.now().strftime('%d/%m/%y'),
							'time': datetime.now().time().strftime('%I:%M%p')
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
			return {"code": "800.200.001", "message": message}
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
			if not system_id:
				return {"code": "800.400.002", "message": "Missing parameter system_id"}
			notifications = list(NotificationService().filter(system__id= system_id).values(
				'message', 'recipient', type= F('notification_type__name'), dateCreated=F('date_created'),
				status = F('state__name')))
			return {"code": "800.200.001", "data": notifications}

		except Exception as ex:
			lgr.exception("Notification logger exception %s" % ex)
		return {"code": "800.400.001", "message": "error in fetching systems notifications"}

	@staticmethod
	def get_logged_in_user_recent_notifications(token):
		"""

		@param token: the given token of a logged in user
		@type: str
		@return: a dictionary containing response code and data
		@rtype:dict
		"""

		try:
			user = OauthService().filter(token = token).values(user=F('app_user__user')).first()
			user_id = user.get('user')
			recipient = RecipientService().filter(user__id = user_id).values(
				'phone_number', email=F('user__email')).first()
			now = timezone.now()
			recently = now - timedelta(hours = 6, minutes = 0)
			current_hour = timezone.now()
			notifications = list(NotificationService().filter(
				recipient = recipient['email'], date_created__lte=current_hour, date_created__gte=recently
			).values())
			sms_notification = list(NotificationService().filter(
				recipient = recipient['phone_number'], date_created__lte = current_hour,
				date_created__gte = recently).values()
			     )
			for sms in sms_notification:
				notifications.append(sms)
			return {"code": "800.200.001", "data": notifications}
		except Exception as ex:
			lgr.exception("Notification Logger exception: %s" % ex)
		return{"code": "800.400.001", "message": "error in fetching recent user notifications"}

	@staticmethod
	def get_logged_in_user_notifications(token):
		"""

		@param token: the given token of a logged in user
		@type: str
		@return: a dictionary containing response code and data
		@rtype:dict
		"""

		try:
			user = OauthService().filter(token = token).values(user=F('app_user__user')).first()
			user_id = user.get('user')
			recipient = RecipientService().filter(user__id = user_id).values(
				'phone_number', email = F('user__email')).first()
			notifications = list(NotificationService().filter(
				recipient = recipient['email']
			).values(
				'message', 'recipient', type= F('notification_type__name'), dateCreated=F('date_created'),
				status = F('state__name')))
			sms_notification = list(NotificationService().filter(
				recipient = recipient['phone_number']).values(
				'message', 'recipient', type= F('notification_type__name'
				                                ''), dateCreated=F('date_created'),
				status = F('state__name'))
			                        )
			for sms in sms_notification:
				notifications.append(sms)
			return {"code": "800.200.001", "data": notifications}
		except Exception as ex:
			lgr.exception("Notification Logger exception: %s" % ex)
		return {"code": "800.400.001", "message": "error in fetching recent user notifications"}
