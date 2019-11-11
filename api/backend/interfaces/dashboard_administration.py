# coding=utf-8
"""
Class for dashboard data
"""
import logging
import calendar
import dateutil.parser
from datetime import datetime, timedelta
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
				'system__name', 'state__name').order_by('-date_created'))
			status_data = {'incidents': current_incidents, 'current_state': {}}
			endpoints = [str(endpoint) for endpoint in list(
				EndpointService().filter(system = system).values_list('state__name', flat = True))]
			status_data.update(current_state = {
				'state': 'status-operational', 'description': 'All systems are operational'
			})
			if endpoints is not None:
				for endpoint in endpoints:
					if 'Major Outage' in endpoints and all(status == 'Major Outage' for status in endpoints):
						status_data.update(
							current_state = {
								'state': 'status-critical', 'description': 'There is a Major System Outage'})
						break
					elif 'Major Outage' in endpoints:
						status_data.update(
							current_state = {'state': 'status-major', 'description': 'There is a Partial System Outage'})
						break
					elif 'Minor Outage' in endpoints:
						status_data.update(
							current_state = {'state': 'status-minor', 'description': 'There is a Minor System Outage'})
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
							'state': 'status-operational', 'description': 'All Systems Operational'})
						break
			# status_data.update(
				# current_state = {'state': 'status-operational', 'description': 'All systems are operational'})
			return {'code': '800.200.001', 'data': status_data}
		except Exception as ex:
			lgr.exception('Get current system status exception %s' % ex)
		return {'code': '800.400.001'}

	@staticmethod
	def past_incidents(system, date_from = None, date_to = None):
		"""
		Retrieves historical incidents within a specified start and end date range within a system
		@param system: System where the incident is created in
		@type system: str
		@param date_from: Start date limit applied
		@type date_from: str | None
		@param date_to: End date limit to be applied
		@type date_to: str | None
		@return: incidents | response code to indicate errors retrieving the incident
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system, state__name = 'Active')
			if not system:
				return {'code': '800.400.002'}
			if date_from and date_to:
				date_from = dateutil.parser.parse(date_from)
				date_to = dateutil.parser.parse(date_to)
			else:
				date_from = datetime.combine(datetime.now(), datetime.min.time())
				date_to = date_from - timedelta(days = 15)
			# return {'code': '800.200.001', 'data': date_to}
			data = []
			for date in (date_from - timedelta(n) for n in range((date_from - date_to).days)):
				incidents = list(IncidentService().filter(
					system = system, date_created__gte = date, date_created__lt = date + timedelta(1)).values(
					'name', 'description', 'system_id', 'priority_level', 'date_created', 'date_modified',
					'scheduled_for', 'scheduled_until', type = F('incident_type__name'),
					eventtype = F('event_type__name'), incident_id = F('id'), status = F('state__name'),
					affected_system = F('system__name')
				).order_by('-date_created'))
				for incident in incidents:
					incident_updates = list(
						IncidentLogService().filter(incident__id = incident.get('incident_id')).values(
							'description', 'priority_level', 'date_created', 'date_modified',
							user_name = F('user__username'), status = F('state__name')
						).order_by('-date_created'))
					incident.update(incident_updates = incident_updates)

				data.append({'date': date, 'incidents': incidents})

			return {'code': '800.200.001', 'data': data}
		except Exception as ex:
			lgr.exception("Get incidents exception %s" % ex)
		return {'code': '800.400.001'}
