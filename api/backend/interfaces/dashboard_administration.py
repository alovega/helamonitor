# coding=utf-8
"""
Class for dashboard data
"""
import logging
import dateutil.parser
from core.models import User
from django.db.models import F, Q

from api.backend.interfaces.notification_interface import NotificationLogger
from core.backend.services import IncidentService, IncidentLogService, IncidentEventService, SystemService, \
	SystemRecipientService, RecipientService, EndpointService
from base.backend.services import StateService, EscalationLevelService, EventTypeService, IncidentTypeService

lgr = logging.getLogger(__name__)


class DashboardAdministration(object):
	"""
	Class for dashboard Administration
	"""
	@staticmethod
	def get_current_status(system, **kwargs):
		"""
		Retrieves current system status and current incidents if any
		@param system: system whose status is being retrieved
		@type system: str
		@param kwargs: extra key-value args to be passed
		@return: a dictionary with any current incidents, statuses of registered endpoints and the response code
		"""
		try:
			system = SystemService().get(pk = system, state__name = 'Active')
			if system is None:
				return {'code': '800.400.002', 'sys': str(system)}
			current_incidents = list(IncidentService().filter(
				system = system).exclude(Q(state__name = 'Resolved') | Q(state__name = 'Completed')).values(
				'id', 'name', 'description', 'scheduled_for', 'scheduled_until', 'priority_level', 'event_type__name',
				'system__name', 'state__name', 'date_created').order_by('-date_created'))
			status_data = {'incidents': current_incidents, 'current_state': {}}
			endpoints = [str(endpoint) for endpoint in list(
				EndpointService().filter(system = system).values_list('state__name', flat = True))]
			if endpoints is not None:
				for endpoint in endpoints:
					if 'Major Outage' in endpoints and all(status == 'Major Outage' for status in endpoints):
						status_data.update(
							current_state = {'state': 'status-critical', 'description': 'There is a Major Outage'})
						break
					elif 'Major Outage' in endpoints:
						status_data.update(
							current_state = {'state': 'status-major', 'description': 'There is a Partial System Outage'})
						break
					elif 'Minor Outage' in endpoints:
						status_data.update(
							current_state = {'state': 'status-minor', 'description': 'There is a Minor Service Outage'})
						break
					elif 'Degraded Performance' in endpoints:
						status_data.update(
							current_state = {'state': 'status-minor', 'description': 'Partially Degraded Service'})
						break
					elif 'Under Maintenance' in endpoints:
						status_data.update(current_state = {
							'state': 'status-maintenance', 'description': 'A Service is undergoing maintenance'})
						break
					else:
						status_data.update(current_state = {
							'state': 'status-operational', 'description': 'All systems are operational'})
						break
			# status_data.update(
				# current_state = {'state': 'status-operational', 'description': 'All systems are operational'})
			return {'code': '800.200.001', 'data': status_data}
		except Exception as ex:
			lgr.exception('Get current system status exception %s' % ex)
		return {'code': '800.400.001'}
