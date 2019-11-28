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
	def get_endpoints(parameters):
		"""
		@param parameters: a dictionary containing parameters used for fetching endpoint data
		@type: dict
		@return:a dictionary containing response code and data to be used for data table
		@rtype: dict
		"""
		try:
			if not parameters:
				return {
					"code": "800.400.002 %s" % parameters, "message": "invalid required parameters"
				}
			system = SystemService().get(id = parameters.get('systemId'))
			if parameters.get('searchQuery') and parameters.get('orderColumn'):
				if parameters.get('orderDir') == 'desc':
					row = list(EndpointService().filter(
						Q(system__id__icontains = parameters.get('systemId')) |
						Q(description__icontains = parameters.get('searchQuery')) |
						Q(name__icontains = parameters.get('searchQuery')) |
						Q(url__icontains = parameters.get('searchQuery')) |
						Q(state__name__icontains = parameters.get('searchQuery')) |
						Q(endpoint_type__name__icontains = parameters.get('searchQuery'))
					).filter(system = system).values(
						endpointDescription = F('description'), dateCreated = F('date_created'),
						endpointName = F('name'),
						Url = F('url'), responseTime = F('optimal_response_time'), status = F('state__name'),
						Id = F('id'), type = F('endpoint_type__name')).order_by(
						'-' + str(parameters.get('orderColumn'))))
				else:
					row = list(EndpointService().filter(
						Q(description__icontains = parameters.get('searchQuery')) |
						Q(name__icontains = parameters.get('searchQuery')) |
						Q(url__icontains = parameters.get('searchQuery')) |
						Q(state__name__icontains = parameters.get('searchQuery')) |
						Q(endpoint_type__name__icontains = parameters.get('searchQuery'))
					).filter(system = system).values(
						endpointDescription = F('description'), dateCreated = F('date_created'),
						endpointName = F('name'),
						Url = F('url'), responseTime = F('optimal_response_time'), status = F('state__name'),
						Id = F('id'), type = F('endpoint_type__name')).order_by(
						str(parameters.get('orderColumn'))))

			elif parameters.get('orderColumn'):
				if parameters.get('orderDir') == 'desc':
					row = list(EndpointService().filter(system = system).values(
						endpointDescription = F('description'), dateCreated = F('date_created'),
						endpointName = F('name'),
						Url = F('url'), responseTime = F('optimal_response_time'), status = F('state__name'),
						Id = F('id'), type = F('endpoint_type__name')).order_by(
						'-' + str(parameters.get('orderColumn'))))
				else:
					row = list(EndpointService().filter(system = system).values(
						endpointDescription = F('description'), dateCreated = F('date_created'),
						endpointName = F('name'),
						Url = F('url'), responseTime = F('optimal_response_time'), status = F('state__name'),
						Id = F('id'), type = F('endpoint_type__name')).order_by(
						str(parameters.get('orderColumn'))))

			elif parameters.get('searchQuery'):
				row = list(EndpointService().filter(
					Q(description__icontains = parameters.get('searchQuery')) |
					Q(name__icontains = parameters.get('searchQuery')) |
					Q(url__icontains = parameters.get('searchQuery')) |
					Q(state__name__icontains = parameters.get('searchQuery')) |
					Q(endpoint_type__name__icontains = parameters.get('searchQuery'))
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
			paginator = Paginator(row, parameters.get('pageSize'))
			table_data = {"row": paginator.page(parameters.get('pageNumber')).object_list}
			item_range = [table_data.get('row')[0].get('item_index'), table_data.get('row')[-1].get('item_index')]
			item_description = str(item_range[0]) + ' to ' + str(item_range[1]) + ' of ' + str(
				paginator.count) + ' ' + 'items'
			table_data.update(size = paginator.num_pages, totalElements = paginator.count,
			                  totalPages = paginator.num_pages, range = item_description)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception("Endpoint Administration exception: %s" % ex)
		return {"code": "800.400.001 %s" % ex, "message": "Error while getting table data"}

	@staticmethod
	def get_system_recipients(parameters):
		"""
		@param parameters: a dictionary containing parameters used for fetching endpoint data
		@type: dict
		@return:a dictionary containing response code and data to be used for data table
		@rtype: dict
		"""
		try:
			if not parameters:
				return {
					"code": "800.400.002 %s" % parameters, "message": "invalid required parameters"
				}
			system = SystemService().get(id = parameters.get('systemId'))
			if parameters.get('searchQuery') and parameters.get('orderColumn'):
				if parameters.get('orderDir') == 'desc':
					row = list(SystemRecipientService().filter(
						Q(recipient__user__username__icontains = parameters.get('searchQuery')) |
						Q(notification_type__name__icontains = parameters.get('searchQuery')) |
						Q(escalation_level__name__icontains = parameters.get('searchQuery')) |
						Q(state__name__icontains = parameters.get('searchQuery'))
					).filter(system = system).values(
						userName = F('recipient__user__username'), systemRecipientId = F('id'),
						status = F('state__name'), notificationType = F('notification_type__name'),
						dateCreated = F('date_created'), escalationLevel = F('escalation_level__name')).order_by(
						'-' + str(parameters.get('orderColumn'))))
				else:
					row = list(SystemRecipientService().filter(
						Q(recipient__user__username__icontains = parameters.get('searchQuery')) |
						Q(notification_type__name__icontains = parameters.get('searchQuery')) |
						Q(escalation_level__name__icontains = parameters.get('searchQuery')) |
						Q(state__name__icontains = parameters.get('searchQuery'))
					).filter(system = system).values(
						userName = F('recipient__user__username'), systemRecipientId = F('id'),
						status = F('state__name'),
						notificationType = F('notification_type__name'), dateCreated = F('date_created'),
						escalationLevel = F('escalation_level__name')).order_by(
						str(parameters.get('orderColumn'))))
			elif parameters.get('orderColumn'):
				if parameters.get('orderDir') == 'desc':
					row = list(SystemRecipientService().filter(system = system).values(
						userName = F('recipient__user__username'), systemRecipientId = F('id'),
						status = F('state__name'), notificationType = F('notification_type__name'),
						dateCreated = F('date_created'), escalationLevel = F('escalation_level__name')).order_by(
						'-' + str(parameters.get('orderColumn'))))
				else:
					row = list(SystemRecipientService().filter(system = system).values(
						userName = F('recipient__user__username'), systemRecipientId = F('id'),
						status = F('state__name'),
						notificationType = F('notification_type__name'), dateCreated = F('date_created'),
						escalationLevel = F('escalation_level__name')).order_by(
						str(parameters.get('orderColumn'))))
			elif parameters.get('searchQuery'):
				row = list(SystemRecipientService().filter(
					Q(recipient__user__username__icontains = parameters.get('searchQuery')) |
					Q(notification_type__name__icontains = parameters.get('searchQuery')) |
					Q(escalation_level__name__icontains = parameters.get('searchQuery')) |
					Q(state__name__icontains = parameters.get('searchQuery'))
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
			paginator = Paginator(row, parameters.get('pageSize'))
			table_data = {"row": paginator.page(parameters.get('pageNumber')).object_list}
			item_range = [table_data.get('row')[0].get('item_index'), table_data.get('row')[-1].get('item_index')]
			item_description = str(item_range[0]) + ' to ' + str(item_range[1]) + ' of ' + str(
				paginator.count) + ' ' + 'items'
			table_data.update(size = paginator.num_pages, totalElements = paginator.count,
			                  totalPages = paginator.num_pages, range = item_description)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception("Endpoint Administration exception: %s" % ex)
		return {"code": "800.400.001 %s" % ex, "message": "Error while getting table data"}

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
					"code": "800.400.002 %s" % parameters, "message": "invalid required parameters"
				}
			if parameters.get('searchQuery') and parameters.get('orderColumn'):
				if parameters.get('orderDir') == 'desc':
					row = list(RecipientService().filter(
						Q(user__username__icontains = parameters.get('searchQuery')) |
						Q(phone_number__icontains = parameters.get('searchQuery')) |
						Q(state__name__icontains = parameters.get('searchQuery'))
					).values(
						userName = F('user__username'), phoneNumber = F('phone_number'), status = F('state__name'),
						dateCreated = F('date_created'), recipientId = F('id')
					).order_by(
						'-' + str(parameters.get('orderColumn'))))
				else:
					row = list(RecipientService().filter(
						Q(user__username__icontains = parameters.get('searchQuery')) |
						Q(phone_number__icontains = parameters.get('searchQuery')) |
						Q(state__name__icontains = parameters.get('searchQuery'))
					).values(
						userName = F('user__username'), phoneNumber = F('phone_number'), status = F('state__name'),
						dateCreated = F('date_created'), recipientId = F('id')
					).order_by(
						str(parameters.get('orderColumn'))))

			elif parameters.get('orderColumn'):
				if parameters.get('orderDir') == 'desc':
					row = list(RecipientService().filter().values(
						userName = F('user__username'), phoneNumber = F('phone_number'), status = F('state__name'),
						dateCreated = F('date_created'), recipientId = F('id')
					).order_by(
						'-' + str(parameters.get('orderColumn'))))
				else:
					row = list(RecipientService().filter().values(
						userName = F('user__username'), phoneNumber = F('phone_number'), status = F('state__name'),
						dateCreated = F('date_created'), recipientId = F('id')
					).order_by(
						str(parameters.get('orderColumn'))))
			elif parameters.get('searchQuery'):
				row = list(RecipientService().filter(
					Q(user__username__icontains = parameters.get('searchQuery')) |
					Q(phone_number__icontains = parameters.get('searchQuery')) |
					Q(state__name__icontains = parameters.get('searchQuery'))
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
			paginator = Paginator(row, parameters.get('pageSize'))
			table_data = {"row": paginator.page(parameters.get('pageNumber')).object_list}
			item_range = [table_data.get('row')[0].get('item_index'), table_data.get('row')[-1].get('item_index')]
			item_description = str(item_range[0]) + ' to ' + str(item_range[1]) + ' of ' + str(paginator.count) + ' ' + 'items'
			table_data.update(size = paginator.num_pages, totalElements = paginator.count,
			                  totalPages = paginator.num_pages, range = item_description)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception("Endpoint Administration exception: %s" % ex)
		return {"code": "800.400.001 %s" % ex, "message": "Error while getting table data"}
