# coding=utf-8
"""
Class for creating new incidents and logging incident updates
"""
import logging

from django.db.models import F
from datetime import timedelta, datetime
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import F

from api.backend.services import OauthService
from api.backend.utilities.common import build_search_query, paginate_data
from core.backend.services import NotificationService, SystemService
from base.backend.services import StateService, NotificationTypeService
from core.models import User

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
			recipient = User.objects.filter(id = user_id).values(
				'phone_number', 'email').first()
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
	def get_logged_in_user_notifications(token, parameters):
		"""

		@param token: the given token of a logged in user
		@type: str
		@param parameters:  a dictionary containing parameters used for fetching notification data
		@type: dict
		@return: a dictionary containing response code and data
		@rtype:dict
		"""

		try:
			user = OauthService().filter(token = token).values(user=F('app_user__user')).first()
			user_id = user.get('user')
			recipient = User.objects.filter(id = user_id).values(
				'phone_number', 'email').first()
			if not parameters or not token or not user:
				return {
					"code": "800.400.002", "message": "invalid required parameters"
				}
			row = NotificationService().filter(
				Q(recipient = recipient['email']) | Q(recipient = recipient['phone_number'])
			)
			columns = ['message', 'recipient', 'state__name', 'notification_type__name']
			search_query = build_search_query(search_value = parameters.get('search_query'), columns = columns)
			if parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = row.order_by('-' + str(parameters.get('order_column')))
				else:
					row = row.order_by(str(parameters.get('order_column')))
			if parameters.get('search_query'):
				row = row.filter(search_query)
			row = list(row.values(
					'message', 'recipient', dateCreated = F('date_created'), status = F('state__name'),
					Id = F('id'), type = F('notification_type__name')))
			table_data = paginate_data(
				data = row, page_size = parameters.get('page_size'), page_number = parameters.get('page_number')
			)
			return {'code': '800.200.001', 'data': table_data, 'recipient':recipient}
		except Exception as ex:
			lgr.exception("Notification Logger exception: %s" % ex)
		return {"code": "800.400.001", "message": "error in fetching recent user notifications"}
