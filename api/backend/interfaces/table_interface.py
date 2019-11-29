import datetime
import logging
from django.core.paginator import Paginator
from django.db.models import Q

from django.db.models import F

from core.backend.services import SystemService, EndpointService, SystemRecipientService, RecipientService

lgr = logging.getLogger(__name__)


class TableData(object):
	"""
	class for getting data for table elements
	"""

	@staticmethod
	def get_endpoints(parameters, system_id):
		"""
		@param parameters: a dictionary containing parameters used for fetching endpoint data
		@type: dict
		@param system_id: Id of a system the endpoints will be attached to
		@type: int
		@return:a dictionary containing response code and data to be used for data table
		@rtype: dict
		"""
		try:
			if not parameters:
				return {
					"code": "800.400.002 %s" % parameters, "message": "invalid required parameters"
				}
			system = SystemService().get(id = system_id)
			if parameters.get('search_query') and parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = list(EndpointService().filter(
						Q(system__id__icontains = system_id) |
						Q(description__icontains = parameters.get('search_query')) |
						Q(name__icontains = parameters.get('search_query')) |
						Q(url__icontains = parameters.get('search_query')) |
						Q(state__name__icontains = parameters.get('search_query')) |
						Q(endpoint_type__name__icontains = parameters.get('search_query'))
					).filter(system = system).values(
						endpointDescription = F('description'), dateCreated = F('date_created'),
						endpointName = F('name'),
						Url = F('url'), responseTime = F('optimal_response_time'), status = F('state__name'),
						Id = F('id'), type = F('endpoint_type__name')).order_by(
						'-' + str(parameters.get('order_column'))))
				else:
					row = list(EndpointService().filter(
						Q(description__icontains = parameters.get('search_query')) |
						Q(name__icontains = parameters.get('search_query')) |
						Q(url__icontains = parameters.get('search_query')) |
						Q(state__name__icontains = parameters.get('search_query')) |
						Q(endpoint_type__name__icontains = parameters.get('search_query'))
					).filter(system = system).values(
						endpointDescription = F('description'), dateCreated = F('date_created'),
						endpointName = F('name'),
						Url = F('url'), responseTime = F('optimal_response_time'), status = F('state__name'),
						Id = F('id'), type = F('endpoint_type__name')).order_by(
						str(parameters.get('order_column'))))

			elif parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = list(EndpointService().filter(system = system).values(
						endpointDescription = F('description'), dateCreated = F('date_created'),
						endpointName = F('name'),
						Url = F('url'), responseTime = F('optimal_response_time'), status = F('state__name'),
						Id = F('id'), type = F('endpoint_type__name')).order_by(
						'-' + str(parameters.get('order_column'))))
				else:
					row = list(EndpointService().filter(system = system).values(
						endpointDescription = F('description'), dateCreated = F('date_created'),
						endpointName = F('name'),
						Url = F('url'), responseTime = F('optimal_response_time'), status = F('state__name'),
						Id = F('id'), type = F('endpoint_type__name')).order_by(
						str(parameters.get('order_column'))))

			elif parameters.get('search_query'):
				row = list(EndpointService().filter(
					Q(description__icontains = parameters.get('search_query')) |
					Q(name__icontains = parameters.get('search_query')) |
					Q(url__icontains = parameters.get('search_query')) |
					Q(state__name__icontains = parameters.get('search_query')) |
					Q(endpoint_type__name__icontains = parameters.get('search_query'))
				).filter(system = system).values(
					endpointDescription = F('description'), dateCreated = F('date_created'),
					endpointName = F('name'),
					Url = F('url'), responseTime = F('optimal_response_time'), status = F('state__name'),
					Id = F('id'), type = F('endpoint_type__name')))
			else:
				row = list(EndpointService().filter(system = system).values(
					endpointDescription = F('description'), dateCreated = F('date_created'),
					endpointName = F('name'),
					Url = F('url'), responseTime = F('optimal_response_time'), status = F('state__name'),
					Id = F('id'), type = F('endpoint_type__name')))
			for index, value in enumerate(row):
				time = datetime.timedelta.total_seconds(value.get('responseTime'))
				del value["responseTime"]
				value.update(responseTime = time, item_index = index + 1)
			paginator = Paginator(row, parameters.get('page_size'))
			table_data = {"row": paginator.page(parameters.get('page_number')).object_list}
			item_range = [table_data.get('row')[0].get('item_index'), table_data.get('row')[-1].get('item_index')]
			item_description = 'Showing ' + str(item_range[0]) + ' to ' + str(item_range[1]) + ' of ' + \
			                   str(paginator.count) + ' ' + 'items'
			table_data.update(size = paginator.num_pages, totalElements = paginator.count,
			                  totalPages = paginator.num_pages, range = item_description)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception("Endpoint Table Data exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error while endpoint getting table data"}

	@staticmethod
	def get_system_recipients(parameters, system_id):
		"""
		@param parameters: a dictionary containing parameters used for fetching endpoint data
		@type: dict
		@param system_id: Id of a system the endpoints will be attached to
		@type: int
		@return:a dictionary containing response code and data to be used for data table
		@rtype: dict
		"""
		try:
			if not parameters:
				return {
					"code": "800.400.002 %s %s" % (parameters, system_id), "message": "invalid required parameters"
				}
			system = SystemService().get(id = system_id)
			if parameters.get('search_query') and parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = list(SystemRecipientService().filter(
						Q(recipient__user__username__icontains = parameters.get('search_query')) |
						Q(notification_type__name__icontains = parameters.get('search_query')) |
						Q(escalation_level__name__icontains = parameters.get('search_query')) |
						Q(state__name__icontains = parameters.get('search_query'))
					).filter(system = system).values(
						userName = F('recipient__user__username'), systemRecipientId = F('id'),
						status = F('state__name'), notificationType = F('notification_type__name'),
						dateCreated = F('date_created'), escalationLevel = F('escalation_level__name')).order_by(
						'-' + str(parameters.get('order_column'))))
				else:
					row = list(SystemRecipientService().filter(
						Q(recipient__user__username__icontains = parameters.get('search_query')) |
						Q(notification_type__name__icontains = parameters.get('search_query')) |
						Q(escalation_level__name__icontains = parameters.get('search_query')) |
						Q(state__name__icontains = parameters.get('search_query'))
					).filter(system = system).values(
						userName = F('recipient__user__username'), systemRecipientId = F('id'),
						status = F('state__name'),
						notificationType = F('notification_type__name'), dateCreated = F('date_created'),
						escalationLevel = F('escalation_level__name')).order_by(
						str(parameters.get('order_column'))))
			elif parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = list(SystemRecipientService().filter(system = system).values(
						userName = F('recipient__user__username'), systemRecipientId = F('id'),
						status = F('state__name'), notificationType = F('notification_type__name'),
						dateCreated = F('date_created'), escalationLevel = F('escalation_level__name')).order_by(
						'-' + str(parameters.get('order_column'))))
				else:
					row = list(SystemRecipientService().filter(system = system).values(
						userName = F('recipient__user__username'), systemRecipientId = F('id'),
						status = F('state__name'),
						notificationType = F('notification_type__name'), dateCreated = F('date_created'),
						escalationLevel = F('escalation_level__name')).order_by(
						str(parameters.get('order_column'))))
			elif parameters.get('search_query'):
				row = list(SystemRecipientService().filter(
					Q(recipient__user__username__icontains = parameters.get('search_query')) |
					Q(notification_type__name__icontains = parameters.get('search_query')) |
					Q(escalation_level__name__icontains = parameters.get('search_query')) |
					Q(state__name__icontains = parameters.get('search_query'))
				).filter(system = system).values(
					userName = F('recipient__user__username'), systemRecipientId = F('id'), status = F('state__name'),
					notificationType = F('notification_type__name'), dateCreated = F('date_created'),
					escalationLevel = F('escalation_level__name')))
			else:
				row = list(SystemRecipientService().filter(system = system).values(
					userName = F('recipient__user__username'), systemRecipientId = F('id'), status = F('state__name'),
					notificationType = F('notification_type__name'), dateCreated = F('date_created'),
					escalationLevel = F('escalation_level__name')))
			for index, value in enumerate(row):
				value.update(item_index = index + 1)
			paginator = Paginator(row, parameters.get('page_size'))
			table_data = {"row": paginator.page(parameters.get('page_number')).object_list}
			item_range = [table_data.get('row')[0].get('item_index'), table_data.get('row')[-1].get('item_index')]
			item_description = 'Showing ' + str(item_range[0]) + ' to ' + str(item_range[1]) + ' of ' + \
			                   str(paginator.count) + ' ' + 'items'
			table_data.update(size = paginator.num_pages, totalElements = paginator.count,
			                  totalPages = paginator.num_pages, range = item_description)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception("System Recipient exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error while system recipient getting table data"}

	@staticmethod
	def get_recipients(parameters):
		"""
		@param parameters: a dictionary containing parameters used for fetching endpoint data
		@type: dict
		@return:a dictionary containing response code and data to be used for data table
		@rtype: dict
		"""
		try:
			if not parameters:
				return {
					"code": "800.400.002", "message": "invalid required parameters"
				}
			if parameters.get('search_query') and parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = list(RecipientService().filter(
						Q(user__username__icontains = parameters.get('search_query')) |
						Q(phone_number__icontains = parameters.get('search_query')) |
						Q(state__name__icontains = parameters.get('search_query'))
					).values(
						userName = F('user__username'), phoneNumber = F('phone_number'), status = F('state__name'),
						dateCreated = F('date_created'), recipientId = F('id')
					).order_by(
						'-' + str(parameters.get('order_column'))))
				else:
					row = list(RecipientService().filter(
						Q(user__username__icontains = parameters.get('search_query')) |
						Q(phone_number__icontains = parameters.get('search_query')) |
						Q(state__name__icontains = parameters.get('search_query'))
					).values(
						userName = F('user__username'), phoneNumber = F('phone_number'), status = F('state__name'),
						dateCreated = F('date_created'), recipientId = F('id')
					).order_by(
						str(parameters.get('order_column'))))

			elif parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = list(RecipientService().filter().values(
						userName = F('user__username'), phoneNumber = F('phone_number'), status = F('state__name'),
						dateCreated = F('date_created'), recipientId = F('id')
					).order_by(
						'-' + str(parameters.get('order_column'))))
				else:
					row = list(RecipientService().filter().values(
						userName = F('user__username'), phoneNumber = F('phone_number'), status = F('state__name'),
						dateCreated = F('date_created'), recipientId = F('id')
					).order_by(
						str(parameters.get('order_column'))))
			elif parameters.get('search_query'):
				row = list(RecipientService().filter(
					Q(user__username__icontains = parameters.get('search_query')) |
					Q(phone_number__icontains = parameters.get('search_query')) |
					Q(state__name__icontains = parameters.get('search_query'))
				).values(
					userName = F('user__username'), phoneNumber = F('phone_number'), status = F('state__name'),
					dateCreated = F('date_created'), recipientId = F('id')
				))
			else:
				row = list(RecipientService().filter().values(
					userName = F('user__username'), phoneNumber = F('phone_number'), status = F('state__name'),
					dateCreated = F('date_created'), recipientId = F('id')
				))
			for index, value in enumerate(row):
				value.update(item_index = index + 1)
			paginator = Paginator(row, parameters.get('page_size'))
			table_data = {"row": paginator.page(parameters.get('page_number')).object_list}
			item_range = [table_data.get('row')[0].get('item_index'), table_data.get('row')[-1].get('item_index')]
			item_description = 'Showing ' + str(item_range[0]) + ' to ' + str(item_range[1]) + ' of ' + \
			                   str(paginator.count) + ' ' + 'items'
			table_data.update(size = paginator.num_pages, totalElements = paginator.count,
			                  totalPages = paginator.num_pages, range = item_description)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception("Recipient Table exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error while getting recipient table data"}
