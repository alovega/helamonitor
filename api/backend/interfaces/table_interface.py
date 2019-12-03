from datetime import timedelta
import logging

from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import F

from core.backend.services import SystemService, EndpointService, SystemRecipientService, RecipientService, \
	EventService, EscalationRuleService, IncidentService
from base.backend.services import IncidentTypeService
from core.models import User

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
				time = timedelta.total_seconds(value.get('responseTime'))
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

	@staticmethod
	def get_events(system, parameters):
		"""
		@param system: System the events have been reported from
		@type: str
		@param parameters: Parameters to be used in the server side data table
		@type: dict
		@return:a dictionary containing response code and the table data
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system)
			if not parameters and system:
				return {'code': '800.400.002', 'message': 'Invalid parameters'}
			if parameters.get('search_query', '') and parameters.get('order_column', ''):
				row = EventService().filter(system = system).filter(
					Q(description__icontains = parameters.get('search_query')) |
					Q(code__icontains = parameters.get('search_query')) |
					Q(event_type__name__icontains = parameters.get('search_query')) |
					Q(method__icontains = parameters.get('search_query')) |
					Q(request__icontains = parameters.get('search_query'))
				).values(
					'id', 'date_created', 'date_modified', 'method', 'description', 'code',
					state_name = F('state__name'), system_name = F('system__name'), event_type_name = F(
						'event_type__name'))
				if parameters.get('order_dir', '') == 'desc':
					row = list(row.order_by('-%s' % parameters.get('order_column')))
				else:
					row = list(row.order_by(parameters.get('order_column')))
			elif parameters.get('order_column', ''):
				row = EventService().filter(system = system).values(
					'id', 'date_created', 'date_modified', 'method', 'description', 'code',
					state_name = F('state__name'), system_name = F('system__name'), event_type_name = F(
						'event_type__name'))
				if parameters.get('order_dir', '') == 'desc':
					row = list(row.order_by('-%s' % (parameters.get('order_column'))))
				else:
					row = list(row.order_by(parameters.get('order_column')))
			elif parameters.get('search_query', ''):
				row = list(EventService().filter(system = system).filter(
					Q(description__icontains = parameters.get('search_query')) |
					Q(code__icontains = parameters.get('search_query')) |
					Q(event_type__name__icontains = parameters.get('search_query')) |
					Q(method__icontains = parameters.get('search_query')) |
					Q(request__icontains = parameters.get('search_query'))
				).values(
					'id', 'date_created', 'date_modified', 'method', 'description', 'code',
					state_name = F('state__name'), system_name = F('system__name'), event_type_name = F(
						'event_type__name')))
			else:
				row = list(EventService().filter(system = system).values(
					'id', 'date_created', 'date_modified', 'method', 'description', 'code',
					state_name = F('state__name'), system_name = F('system__name'), event_type_name = F(
						'event_type__name')))

			for index, value in enumerate(row):
				value.update(item_index = index + 1)
			paginator = Paginator(row, parameters.get('page_size', ''))
			table_data = {"row": paginator.page(parameters.get('page_number', '')).object_list}
			item_range = [table_data.get('row')[0].get('item_index'), table_data.get('row')[-1].get('item_index')]
			item_description = 'Showing %s to %s of %s items' % (
				str(item_range[0]), str(item_range[1]), str(paginator.count))
			table_data.update(
				size = paginator.num_pages, totalElements = paginator.count, totalPages = paginator.num_pages,
				range = item_description)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception('Get Events data exception: %s' % ex)
		return {'code': '800.400.001', 'message': 'Error while fetching system events'}

	@staticmethod
	def active_users(system, parameters):
		"""
		@param system: System the users where the users are registered in
		@type: str
		@param parameters: Parameters to be used in the server side data table
		@type: dict
		@return:a dictionary containing response code and the table data
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system)
			if not parameters and system:
				return {'code': '800.400.002', 'message': 'Invalid parameters'}
			if parameters.get('search_query', '') and parameters.get('order_column', ''):
				row = User.objects.filter(is_active = True).filter(
					Q(username__icontains = parameters.get('search_query')) |
					Q(first_name__icontains = parameters.get('search_query')) |
					Q(last_name__icontains = parameters.get('search_query')) |
					Q(email__icontains = parameters.get('search_query')) |
					Q(phone_number__icontains = parameters.get('search_query'))
				).values()
				if parameters.get('order_dir', '') == 'desc':
					row = list(row.order_by('-%s' % parameters.get('order_column')))
				else:
					row = list(row.order_by(parameters.get('order_column')))
			elif parameters.get('order_column', ''):
				row = User.objects.filter(is_active = True).filter().values()
				if parameters.get('order_dir', '') == 'desc':
					row = list(row.order_by('-%s' % (parameters.get('order_column'))))
				else:
					row = list(row.order_by(parameters.get('order_column')))
			elif parameters.get('search_query', ''):
				row = User.objects.filter(is_active = True).filter(
					Q(username__icontains = parameters.get('search_query')) |
					Q(first_name__icontains = parameters.get('search_query')) |
					Q(last_name__icontains = parameters.get('search_query')) |
					Q(email__icontains = parameters.get('search_query')) |
					Q(phone_number__icontains = parameters.get('search_query'))
				).values()
			else:
				row = User.objects.filter(is_active = True).filter().values()

			for index, value in enumerate(row):
				value.update(item_index = index + 1)
			paginator = Paginator(row, parameters.get('page_size', ''))
			table_data = {'row': paginator.page(parameters.get('page_number', '')).object_list}
			if table_data.get('row'):
				item_range = [table_data.get('row')[0].get('item_index'), table_data.get('row')[-1].get('item_index')]
			else:
				item_range = [0, 0]
			item_description = 'Showing %s to %s of %s items' % (
				str(item_range[0]), str(item_range[1]), str(paginator.count))
			table_data.update(
					size = paginator.num_pages, totalElements = paginator.count, totalPages = paginator.num_pages,
					range = item_description)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception('Get Users data exception: %s' % ex)
		return {'code': '800.400.001', 'message': 'Error while fetching system users'}

	@staticmethod
	def escalation_rules(system, parameters):
		"""
		@param system: System the escalation rules are defined in
		@type: str
		@param parameters: Parameters to be used in the server side data table
		@type: dict
		@return:a dictionary containing response code and the table data
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system)
			if not parameters and system:
				return {'code': '800.400.002', 'message': 'Invalid parameters'}
			if parameters.get('search_query', '') and parameters.get('order_column', ''):
				row = EscalationRuleService().filter(system = system).filter(
					Q(description__icontains = parameters.get('search_query')) |
					Q(name__icontains = parameters.get('search_query')) |
					Q(system__name__icontains = parameters.get('search_query')) |
					Q(event_type__name__icontains = parameters.get('search_query')) |
					Q(escalation_level__name__icontains = parameters.get('search_query'))).values(
					'id', 'name', 'description', 'duration', 'date_created', 'date_modified', 'nth_event',
					system_id = F('system'), escalation_level_name = F('escalation_level__name'), state_name = F(
						'state__name'), event_type_name = F('event_type__name'))
				if parameters.get('order_dir', '') == 'desc':
					row = list(row.order_by('-%s' % parameters.get('order_column')))
				else:
					row = list(row.order_by(parameters.get('order_column')))
			elif parameters.get('order_column', ''):
				row = EscalationRuleService().filter(system = system).values(
					'id', 'name', 'description', 'duration', 'date_created', 'date_modified', 'nth_event',
					system_id = F('system'), escalation_level_name = F('escalation_level__name'), state_name = F(
						'state__name'), event_type_name = F('event_type__name'))
				if parameters.get('order_dir', '') == 'desc':
					row = list(row.order_by('-%s' % (parameters.get('order_column'))))
				else:
					row = list(row.order_by(parameters.get('order_column')))
			elif parameters.get('search_query', ''):
				row = EscalationRuleService().filter(system = system).filter(
					Q(description__icontains = parameters.get('search_query')) |
					Q(name__icontains = parameters.get('search_query')) |
					Q(system__name__icontains = parameters.get('search_query')) |
					Q(event_type__name__icontains = parameters.get('search_query')) |
					Q(escalation_level__name__icontains = parameters.get('search_query'))).values(
					'id', 'name', 'description', 'duration', 'date_created', 'date_modified', 'nth_event',
					system_id = F('system'), escalation_level_name = F('escalation_level__name'), state_name = F(
						'state__name'), event_type_name = F('event_type__name'))
			else:
				row = EscalationRuleService().filter(system = system).values(
					'id', 'name', 'description', 'duration', 'date_created', 'date_modified', 'nth_event',
					system_id = F('system'), escalation_level_name = F('escalation_level__name'), state_name = F(
						'state__name'), event_type_name = F('event_type__name'))

			for index, value in enumerate(row):
				value.update(duration = timedelta.total_seconds(value.get('duration')))
				value.update(item_index = index + 1)
			paginator = Paginator(row, parameters.get('page_size', ''))
			table_data = {'row': paginator.page(parameters.get('page_number', '')).object_list}
			if table_data.get('row'):
				item_range = [table_data.get('row')[0].get('item_index'), table_data.get('row')[-1].get('item_index')]
			else:
				item_range = [0, 0]
			item_description = 'Showing %s to %s of %s items' % (
				str(item_range[0]), str(item_range[1]), str(paginator.count))
			table_data.update(
					size = paginator.num_pages, totalElements = paginator.count, totalPages = paginator.num_pages,
					range = item_description)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception('Get Users data exception: %s' % ex)
		return {'code': '800.400.001', 'message': 'Error while fetching escalation rules'}

	@staticmethod
	def incidents(system, parameters, incident_type = None, **kwargs):
		"""
		@param system: System the incidents were created in
		@type: str
		@param incident_type: Type of the incident
		@type: str | None
		@param parameters: Parameters to be used in the server side data table
		@type: dict
		@param kwargs: Extra key-value pairs to be passed
		@return:a dictionary containing response code and the table data
		@rtype: dict
		"""
		try:
			system = SystemService().filter(pk = system).first()
			incident_type = IncidentTypeService().filter(name = incident_type).first()
			if not parameters and system:
				return {'code': '800.400.002', 'message': 'Invalid parameters'}
			states = kwargs.get('states', None)
			row = IncidentService().filter(state__name__in = states) if states is not None else \
				IncidentService().filter()
			row = row.filter(incident_type = incident_type) if incident_type else row
			if parameters.get('search_query', '') and parameters.get('order_column', ''):
				row = row.filter(system = system).filter(
					Q(name__icontains = parameters.get('search_query')) |
					Q(decription__icontains = parameters.get('search_query')) |
					Q(system__name__icontains = parameters.get('search_query')) |
					Q(event_type__name__icontains = parameters.get('search_query')) |
					Q(incident_type__name__icontains = parameters.get('search_query'))).values(
					'id', 'name', 'description', 'priority_level', 'date_created', 'date_modified',
					'scheduled_for', 'scheduled_until', system_id = F('system__id'), incident_type_name = F(
						'incident_type__name'), state_id = F('state__id'), state_name = F('state__name'),
					system_name = F('system__name'), event_type_id = F('event_type__id'))
				if parameters.get('order_dir', '') == 'desc':
					row = list(row.order_by('-%s' % parameters.get('order_column')))
				else:
					row = list(row.order_by(parameters.get('order_column')))
			elif parameters.get('order_column', ''):
				row = row.filter(system = system).values(
					'id', 'name', 'description', 'priority_level', 'date_created', 'date_modified',
					'scheduled_for', 'scheduled_until', system_id = F('system__id'), incident_type_name = F(
						'incident_type__name'), state_id = F('state__id'), state_name = F('state__name'),
					system_name = F('system__name'), event_type_id = F('event_type__id'))
				if parameters.get('order_dir', '') == 'desc':
					row = list(row.order_by('-%s' % (parameters.get('order_column'))))
				else:
					row = list(row.order_by(parameters.get('order_column')))
			elif parameters.get('search_query', ''):
				row = row.filter(system = system).filter(
					Q(name__icontains = parameters.get('search_query')) |
					Q(decription__icontains = parameters.get('search_query')) |
					Q(system__name__icontains = parameters.get('search_query')) |
					Q(event_type__name__icontains = parameters.get('search_query')) |
					Q(incident_type__name__icontains = parameters.get('search_query'))).values(
					'id', 'name', 'description', 'priority_level', 'date_created', 'date_modified',
					'scheduled_for', 'scheduled_until', system_id = F('system__id'), incident_type_name = F(
						'incident_type__name'), state_id = F('state__id'), state_name = F('state__name'),
					system_name = F('system__name'), event_type_id = F('event_type__id'))
			else:
				row = row.filter(system = system).values(
					'id', 'name', 'description', 'priority_level', 'date_created', 'date_modified',
					'scheduled_for', 'scheduled_until', system_id = F('system__id'), incident_type_name = F(
						'incident_type__name'), state_id = F('state__id'), state_name = F('state__name'),
					system_name = F('system__name'), event_type_id = F('event_type__id'))

			for index, value in enumerate(row):
				value.update(item_index = index + 1)
			paginator = Paginator(row, parameters.get('page_size', ''))
			table_data = {'row': paginator.page(parameters.get('page_number', '')).object_list}
			if table_data.get('row'):
				item_range = [table_data.get('row')[0].get('item_index'), table_data.get('row')[-1].get('item_index')]
			else:
				item_range = [0, 0]
			item_description = 'Showing %s to %s of %s items' % (
				str(item_range[0]), str(item_range[1]), str(paginator.count))
			table_data.update(
					size = paginator.num_pages, totalElements = paginator.count, totalPages = paginator.num_pages,
					range = item_description)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception('Get Users data exception: %s' % ex)
		return {'code': '800.400.001', 'message': 'Error while fetching incidents %s'%str(ex)}
