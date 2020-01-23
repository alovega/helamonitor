from datetime import timedelta
import logging
import pandas as pd

from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import F

from api.backend.utilities.common import build_search_query, paginate_data
from core.backend.services import SystemService, EndpointService, SystemRecipientService, EventService, \
	EscalationRuleService, IncidentService, IncidentLogService, IncidentEventService, NotificationService
from base.backend.services import IncidentTypeService, NotificationTypeService
from core.models import User

lgr = logging.getLogger(__name__)


class TableData(object):
	"""
	class for getting data for table elements
	"""

	@staticmethod
	def get_endpoints(parameters, system_id):
		"""
		@param parameters: a dictionary containing parameters used for querying the endpoint model
		@type: dict
		@param system_id: Id of a system the endpoints will be attached to
		@type: int
		@return:a dictionary containing response code and data to be used for data table
		@rtype: dict
		"""
		try:
			system = SystemService().get(id = system_id)
			if system is None or parameters is None:
				return {'code': '800.400.002', 'message': 'Invalid parameters'}
			row = EndpointService().filter(system = system)
			columns = ['description', 'name', 'url', 'state__name', 'endpoint_type__name']
			search_query = build_search_query(search_value = parameters.get('search_query'), columns = columns)
			if parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = row.order_by('-' + str(parameters.get('order_column')))
				else:
					row = row.order_by(str(parameters.get('order_column')))
			if parameters.get('search_query'):
				row = row.filter(search_query)
			row = list(row.values(
				endpointDescription = F('description'), dateCreated = F('date_created'),
				endpointName = F('name'),
				Url = F('url'), responseTime = F('optimal_response_time'), status = F('state__name'),
				Id = F('id'), type = F('endpoint_type__name')))
			table_data = paginate_data(
				data = row, page_size = parameters.get('page_size'), page_number = parameters.get('page_number')
			)
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
		@type: char
		@return:a dictionary containing response code and data to be used for data table
		@rtype: dict
		"""
		try:
			system = SystemService().get(id = system_id)
			if system is None or parameters is None:
				return {'code': '800.400.002', 'message': 'Invalid parameters'}
			row = SystemRecipientService().filter(system = system).filter(
				Q(recipient__is_active = True))
			columns = [
				'recipient', 'recipient__username', 'notification_type__name', 'escalation_level__name', 'state__name'
			]
			search_queries = build_search_query(search_value = parameters.get('search_query'), columns = columns)
			if parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = row.order_by('-' + str(parameters.get('order_column')))
				else:
					row = row.order_by(str(parameters.get('order_column')))
			elif parameters.get('search_query'):
				row = row.filter(search_queries)

			row = list(row.values(
				userName = F('recipient__username'), systemRecipientId = F('id'), status = F('state__name'),
				notificationType = F('notification_type__name'), dateCreated = F('date_created'),
				escalationLevel = F('escalation_level__name'), recipientId = F('recipient')))
			df = pd.DataFrame(row)
			data = [update_dict(k, g.to_dict(orient = 'list')) for k, g in df.groupby(df.userName)]
			table_data = paginate_data(
				data = data, page_size = parameters.get('page_size'), page_number = parameters.get('page_number')
			)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception("System Recipient exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error while system recipient getting table data"}

	@staticmethod
	def get_notifications(parameters, system_id, notification_type = None):
		"""
		@param notification_type: Notification Type which the notification belongs to
		@type: str
		@param parameters: a dictionary containing parameters used for fetching notification data
		@type: dict
		@param system_id: Id of a system the notifications will be attached to
		@type: char
		@return: a dictionary containing response code and data to be used for data table
		@rtype: dict
		"""
		try:
			system = SystemService().get(id = system_id)
			notification_type = NotificationTypeService().filter(name = notification_type).first()
			columns = ['message', 'recipient', 'state__name', 'notification_type__name']
			search = build_search_query(search_value = parameters.get('search_query'), columns = columns)
			if not system or not parameters or not notification_type:
				return {
					"code": "800.400.002", "message": "invalid required parameters"
				}
			row = NotificationService().filter(system = system).filter(notification_type = notification_type)
			if parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = row.order_by('-' + str(parameters.get('order_column')))
				else:
					row = row.order_by(str(parameters.get('order_column')))

			if parameters.get('search_query'):
				row = row.filter(search)

			row = list(row.values('message', 'recipient', dateCreated = F('date_created'), status = F('state__name'),
			                      Id = F('id'), type = F('notification_type__name')))
			table_data = paginate_data(
				data = row, page_size = parameters.get('page_size'), page_number = parameters.get('page_number')
			)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception("Recipient Table exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error while getting notifications table data"}

	@staticmethod
	def get_events(system, parameters):
		"""
		Server side implementation of events data table
		@param system: System the events have been reported from
		@type: str
		@param parameters: Parameters to be used in the server side data table
		@type: dict
		@return:a dictionary containing response code and the table data
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system)
			if not parameters and not system:
				return {'code': '800.400.002', 'message': 'Invalid parameters'}
			row = EventService().filter(system = system)
			columns = ['description', 'code', 'event_type__name', 'method', 'request']
			search_query = build_search_query(search_value = parameters.get('search_query'), columns=columns)
			if parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = row.order_by('-' + str(parameters.get('order_column')))
				else:
					row = row.order_by(str(parameters.get('order_column')))

			if parameters.get('search_query'):
				row = row.filter(search_query)

			row = list(row.values(
					'id', 'date_created', 'date_modified', 'method', 'description', 'code',
					state_name = F('state__name'), system_name = F('system__name'), event_type_name = F(
						'event_type__name')))
			table_data = paginate_data(
				data = row, page_size = parameters.get('page_size'), page_number = parameters.get('page_number')
			)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception('Get Events data exception: %s' % ex)
		return {'code': '800.400.001', 'message': 'Error while fetching system events'}

	@staticmethod
	def active_users(system, parameters):
		"""
		Server side implementation of users data table
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
			row = User.objects.filter(is_active = True)
			columns = ['username', 'first_name', 'last_name', 'email', 'phone_number']
			search_query = build_search_query(search_value = parameters.get('search_query'), columns = columns)
			if parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = row.order_by('-' + str(parameters.get('order_column')))
				else:
					row = row.order_by(str(parameters.get('order_column')))

			if parameters.get('search_query'):
				row = row.filter(search_query)

			row = list(row.values())

			table_data = paginate_data(
				data = row, page_size = parameters.get('page_size'), page_number = parameters.get('page_number')
			)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception('Get Users data exception: %s' % ex)
		return {'code': '800.400.001', 'message': 'Error while fetching system users'}

	@staticmethod
	def escalation_rules(system, parameters):
		"""
		Server side implementation of Escalation rules data table
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
			row = EscalationRuleService().filter(system = system)
			columns = ['description', 'name', 'system__name', 'event_type__name', 'escalation_level__name']
			search_query = build_search_query(search_value = parameters.get('search_query'), columns = columns)
			if parameters.get('order_column'):
				if parameters.get('order_dir') == 'desc':
					row = row.order_by('-' + str(parameters.get('order_column')))
				else:
					row = row.order_by(str(parameters.get('order_column')))

			if parameters.get('search_query'):
				row = row.filter(search_query)
			row = list(row.values(
					'id', 'name', 'description', 'duration', 'date_created', 'date_modified', 'nth_event',
					system_id = F('system'), escalation_level_name = F('escalation_level__name'), state_name = F(
						'state__name'), event_type_name = F('event_type__name')))

			table_data = paginate_data(
				data = row, page_size = parameters.get('page_size'), page_number = parameters.get('page_number')
			)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception('Get Users data exception: %s' % ex)
		return {'code': '800.400.001', 'message': 'Error while fetching escalation rules'}

	@staticmethod
	def incidents(system, parameters, incident_type = None, **kwargs):
		"""
		Server side implementation of incidents data table
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
					Q(description__icontains = parameters.get('search_query')) |
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
					Q(description__icontains = parameters.get('search_query')) |
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
				incident_updates = list(IncidentLogService().filter(incident__id = value.get('id')).values(
					'id', 'description', 'priority_level', 'date_created', 'date_modified', user_id = F('user__id'),
					username = F('user__username'), escalation_level_id = F('escalation_level__id'), state_name = F(
						'state__name'), state_id = F('state__id')).order_by('-date_created'))
				value.update(incident_updates = incident_updates)
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
		return {'code': '800.400.001', 'message': 'Error while fetching incidents %s'}

	@staticmethod
	def incident_events(incident, parameters, **kwargs):
		"""
		Server side implementation of incident-events data table
		@param incident: Incident whose events are to be retrieved
		@type: str
		@param parameters: Parameters to be used in the server side data table
		@type: dict
		@param kwargs: Extra key-value pairs to be passed
		@return:a dictionary containing response code and the table data
		@rtype: dict
		"""
		try:
			incident = IncidentService().filter(pk = incident).first()
			if not parameters and incident:
				return {'code': '800.400.002', 'message': 'Invalid parameters'}
			if parameters.get('search_query', '') and parameters.get('order_column', ''):
				row = IncidentEventService().filter(incident = incident, state__name = 'Active').filter(
					Q(description__icontains = parameters.get('search_query')) |
					Q(code__icontains = parameters.get('search_query')) |
					Q(event_type__name__icontains = parameters.get('search_query')) |
					Q(method__icontains = parameters.get('search_query')) |
					Q(request__icontains = parameters.get('search_query'))).values(
					incident_id = F('incident'), status = F('state__name'), event_id = F('event'))
				if parameters.get('order_dir', '') == 'desc':
					row = list(row.order_by('-%s' % parameters.get('order_column')))
				else:
					row = list(row.order_by(parameters.get('order_column')))
			elif parameters.get('order_column', ''):
				row = IncidentEventService().filter(incident = incident, state__name = 'Active').values(
					incident_id = F('incident'), status = F('state__name'), event_id = F('event'))
				if parameters.get('order_dir', '') == 'desc':
					row = list(row.order_by('-%s' % (parameters.get('order_column'))))
				else:
					row = list(row.order_by(parameters.get('order_column')))
			elif parameters.get('search_query', ''):
				row = IncidentEventService().filter(incident = incident, state__name = 'Active').filter(
					Q(description__icontains = parameters.get('search_query')) |
					Q(code__icontains = parameters.get('search_query')) |
					Q(event_type__name__icontains = parameters.get('search_query')) |
					Q(method__icontains = parameters.get('search_query')) |
					Q(request__icontains = parameters.get('search_query'))).values(
					incident_id = F('incident'), status = F('state__name'), event_id = F('event'))
			else:
				row = IncidentEventService().filter(incident = incident, state__name = 'Active').values(
					incident_id = F('incident'), status = F('state__name'), event_id = F('event'))

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
		return {'code': '800.400.001', 'message': 'Error while fetching incident events'}


def update_dict(user_name, d):
	d['userName'] = user_name
	return d

