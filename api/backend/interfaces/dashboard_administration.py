# coding=utf-8
"""
Class for dashboard data
"""
import logging
import dateutil.parser
import calendar
import traceback

from datetime import datetime, timedelta
from django.db.models import F, Q
from django.utils import timezone

from api.backend.interfaces.notification_interface import NotificationLogger
from core.backend.services import IncidentService, IncidentLogService, EventService, SystemService, \
	SystemRecipientService, RecipientService, EndpointService, SystemMonitorService
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
			for incident in current_incidents:
				incident_updates = list(IncidentLogService().filter(incident__id = incident.get('id')).values(
					'description', 'priority_level', 'date_created', 'date_modified', user_name = F('user__username'),
					status = F('state__name')
				).order_by('-date_created'))
				incident.update(incident_updates = incident_updates)
			status_data = {'system_id': system.id, 'incidents': current_incidents, 'current_state': {}}
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
					system = system, date_created__gte = date, date_created__lt = date + timedelta(1)).exclude(
					~(Q(state__name = 'Resolved') | Q(state__name = 'Completed'))
				).values(
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

	@staticmethod
	def dashboard_widgets_data(system, date_from = None, date_to = None):
		"""
		Retrieves historical data within a specified start and end date range within a system
		@param system: System where the incident is created in
		@type system: str
		@param date_from: Start date limit applied
		@type date_from: str | None
		@param date_to: End date limit to be applied
		@type date_to: str | None
		@return: incidents | response code to indicate errors retrieving the data
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
				date_from = datetime.combine(datetime.now(), datetime.min.time()) + timedelta(days = 1)
				date_to = date_from - timedelta(days = 1)
			reported_events = EventService().filter(
				system = system, date_created__lte = date_from, date_created__gte = date_to).count()
			open_incidents = IncidentService().filter(
				system = system, incident_type__name = 'Realtime', date_created__lte = date_from, date_created__gte =
				date_to).exclude(state__name = 'Resolved').count()
			closed_incidents = IncidentService().filter(
				system = system, incident_type__name = 'Realtime', state__name = 'Resolved', date_created__lte =
				date_from, date_created__gte = date_to).count()
			scheduled_incidents = IncidentService().filter(
				system = system, incident_type__name = 'Scheduled', date_created__lte = date_from, date_created__gte =
				date_to).exclude(state__name = 'Completed').count()
			data = {
				'reported_events': reported_events, 'open_incidents': open_incidents, 'closed_incidents':
					closed_incidents, 'scheduled_incidents': scheduled_incidents
			}
			return {'code': '800.200.001', 'data': data}
		except Exception as ex:
			lgr.exception("Get incidents exception %s" % ex)
		return {'code': '800.400.001'}

	@staticmethod
	def get_error_rate(system_id, start_date, end_date):
		"""
		Calculates and returns the error rate of a system based on logged events
		@param: system_id: Id of the system
		@type system_id: str
		@param start_date: Start point of the data to be presented
		@type: start_date: str
		@param: end_date: End date of the period for which the data is to be extracted
		@type end_date: str
		@return: Response code indicating status and error rate graph data
		"""
		try:
			system = SystemService().get(pk = system_id, state__name = 'Active')
			if not system:
				return {'code': '800.400.200'}
			now = timezone.now()
			start_date = dateutil.parser.parse(start_date)
			end_date = dateutil.parser.parse(end_date)
			period = start_date - end_date
			labels = []
			dataset = []
			if period.days <= 1:
				for i in range(1, 25):
					past_hour = now - timedelta(hours = i, minutes = 0)
					current_hour = past_hour + timedelta(hours = 1)
					current_errors = EventService().filter(
						system = system, event_type__name = 'Error', date_created__lte = current_hour,
						date_created__gte = past_hour).count()
					past_hour = past_hour.replace(minute = 0)
					labels.append(past_hour.strftime("%m/%d/%y  %H:%M"))
					dataset.append(current_errors)
			elif period.days <= 7:
				for i in range(0, 7):
					current_day = now - timedelta(days = i, hours = 0, minutes = 0)
					past_day = current_day + timedelta(days = 1)
					current_errors = EventService().filter(
						system = system, event_type__name = 'Error', date_created__lte = past_day,
						date_created__gte = current_day).count()
					past_day = past_day.replace(hour = 0, minute = 0)
					labels.append(past_day.strftime("%m/%d/%y  %H:%M"))
					dataset.append(current_errors)
			elif period.days <= 31:
				for i in range(0, 31):
					current_day = now - timedelta(days = i, hours = 0, minutes = 0)
					past_day = current_day + timedelta(days = 1)
					current_errors = EventService().filter(
						system = system, event_type__name = 'Error', date_created__lte = past_day,
						date_created__gte = current_day).count()
					past_day = past_day.replace(hour = 0, minute = 0)
					labels.append(past_day.strftime("%m/%d/%y"))
					dataset.append(current_errors)
			elif period.days <= 365:
				current_date = now.replace(day = 1, hour = 0, minute = 0, second = 0, microsecond = 0)
				current_month = now.month
				current_date = current_date.replace(
					day = 1, hour = 0, minute = 0, second = 0, microsecond = 0) + timedelta(
					days = calendar.monthrange(current_date.year, current_month)[1] - 1)
				for i in range(1, 13):
					if current_month > 1:
						month_name = calendar.month_name[current_month]
						end_date = current_date
						start_date = current_date - timedelta(
							days = calendar.monthrange(end_date.year, end_date.month)[1] - 1)
						current_date = current_date - timedelta(
							days = calendar.monthrange(current_date.year, current_month)[1])
						current_month = current_month - 1
					else:
						month_name = calendar.month_name[current_month]
						end_date = current_date
						start_date = current_date - timedelta(
							days = calendar.monthrange(end_date.year, end_date.month)[1] - 1)
						current_date = current_date - timedelta(
							days = calendar.monthrange(current_date.year, current_month)[1])
						current_month = current_date.month
					current_errors = EventService().filter(
						system = system, event_type__name = 'Error', date_created__lte = end_date,
						date_created__gte = start_date).count()
					labels.append('%s, %s' % (month_name, current_date.year))
					dataset.append(current_errors)
			else:
				intervals = 24
				for i in range(1, intervals + 1):
					past_hour = now - timedelta(hours = i, minutes = 0)
					current_hour = past_hour + timedelta(hours = 1)
					current_errors = EventService().filter(
						system = system, event_type__name = 'Error', date_created__lte = current_hour,
						date_created__gte = past_hour).count()
					past_hour = past_hour.replace(minute = 0)
					labels.append(past_hour.strftime("%m/%d/%y  %H:%M"))
					dataset.append(current_errors)
			return {'code': '800.200.001', 'data': {'labels': labels, 'datasets': dataset}}
		except Exception as ex:
			lgr.exception("Get Error rate Exception %s" % ex)
		return {'code': '800.400.001'}

	@staticmethod
	def calculate_system_availability(system, date_from = None, date_to = None):
		"""
		Calculates the system availability percentage within a specified start and end date range within a system
		@param system: System whose availability percentage is to be computed
		@type system: str
		@param date_from: Start date limit applied
		@type date_from: str | None
		@param date_to: End date limit to be applied
		@type date_to: str | None
		@return: system_availability_metric data | response code to indicate errors retrieving availability trend of
		the system
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system, state__name = 'Active')
			if not system:
				return {'code': '800.400.002', 'message': 'Invalid system %s' % system}
			if date_from and date_to:
				date_from = dateutil.parser.parse(date_from)
				date_to = dateutil.parser.parse(date_to)
			else:
				date_from = datetime.combine(datetime.now(), datetime.min.time())
				date_to = date_from + timedelta(days = 7)
			endpoints = EndpointService().filter(system = system)
			total_system_downtime = timedelta()
			for endpoint in endpoints:
				previous_monitor = {'state': None, 'date': None}
				saved_monitors = list(SystemMonitorService().filter(
					endpoint = endpoint, date_created__gt = date_to, date_created__lt = date_from).order_by(
					'date_created').values('date_created', state_name = F('state__name')))
				for monitor in saved_monitors:
					total_monitor_downtime = timedelta()
					if monitor.get('state_name') != 'Operational':
						previous_monitor = {'state': 'Down', 'date': monitor.get('date_created')} if \
							previous_monitor.get('state') == 'Up' else previous_monitor
						if previous_monitor.get('state') == 'Up':
							previous_monitor.update(state = 'Down', date = monitor.get('date_created'))
						if not previous_monitor.get('date') and (saved_monitors.index(monitor) == -1 or len(
								saved_monitors) == 1):
							total_monitor_downtime += date_from - monitor.get('date_created')
						else:
							if not previous_monitor.get('date'):
								previous_monitor.update(state = 'Down', date = monitor.get('date_created'))
							total_monitor_downtime += monitor.get('date_created') - previous_monitor.get('date')
						previous_monitor.update(state = 'Down', date = monitor.get('date_created'))
					else:
						if not previous_monitor.get('date'):
							previous_monitor.update(state = 'Up', date = monitor.get('date_created'))
						total_monitor_downtime += monitor.get('date_created') - previous_monitor.get('date')
						previous_monitor.update(state = 'Up', date = monitor.get('date_created'))
					total_system_downtime += total_monitor_downtime
			return {
				'code': '800.200.001', 'data': {
					'start_date': date_to.isoformat(), 'end_date': date_from.isoformat(), 'total_period': str(
						date_from - date_to), 'total_uptime': str((date_from - date_to) - total_system_downtime),
					'total_downtime': str(total_system_downtime),
					'uptime_percentage': round(((date_from - date_to) - total_system_downtime).total_seconds() / (
							date_from - date_to).total_seconds() * 100, 2),
					'downtime_percentage': round(
						total_system_downtime.total_seconds() / (date_from - date_to).total_seconds() * 100, 2)}}
		except Exception as ex:
			lgr.exception("Calculate downtime percentage exception %s" % ex)
		return {'code': '800.400.001', 'msg': 'Error. Could not calculate total system availability'}

	@staticmethod
	def availability_trend(system, interval):
		"""
		Calculates the system availability percentage within a specified start and end date range within a system
		@param system: System whose availability percentage is to be computed
		@type system: str
		@param interval: Time interval to be applied in retrieving metric data points
		@return: Total system availability data points | response code to indicate errors while retrieving
		availability trend of the system as data points to be plotted in a graph
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system, state__name = 'Active')
			if not system and interval:
				return {'code': '800.400.002', 'message': 'Missing or invalid parameters'}
			today = datetime.now(timezone.utc)
			dataset = []
			labels = []
			if interval == 'day':
				time_intervals = 24
				interval_length = 1
				identifier = 'day'
			elif interval == 'week':
				time_intervals = 7
				interval_length = 24
				identifier = 'week'
			elif interval == 'month':
				time_intervals = 30
				interval_length = 24
				identifier = 'month'
			else:
				return {'code': '800.400.002', 'message': 'Invalid time interval'}
			for i in range(1, time_intervals):
				past_interval = today - timedelta(hours = i * interval_length)
				current_interval = past_interval + timedelta(hours = interval_length)
				availability_percentage_result = DashboardAdministration.calculate_system_availability(
					system = system.id, date_from = current_interval.isoformat(), date_to = past_interval.isoformat())
				if availability_percentage_result.get('code') == '800.200.001':
					availability_percentage = availability_percentage_result.get('data').get('uptime_percentage')
				else:
					return {'code': '800.400.001', 'message': availability_percentage_result}
				current_interval = (current_interval + timedelta(hours = 1)).replace(minute = 0)
				labels.append(current_interval.strftime("%m/%d/%y  %H:%M"))
				dataset.append(availability_percentage)
			return {'code': '800.200.001', 'data': {
				'labels': labels, 'dataset': dataset, 'time_intervals': time_intervals, 'identifier': identifier}}
		except Exception as ex:
			lgr.exception("Get uptime trend data exception %s" % ex)
		return {'code': '800.400.001', 'msg': 'Error. Could not retrieve system up time trend data'}
