import logging

import requests
import dateutil.parser
import calendar
from django.db.models import F
from django.utils import timezone
from datetime import timedelta
from core.backend.services import SystemMonitorService, EndpointService, SystemService
from base.backend.services import StateService, EventTypeService

from api.backend.interfaces.event_administration import EventLog

lgr = logging.getLogger(__name__)


class MonitorInterface(object):
	"""
	class for logging status  of  system micro-services
	"""

	@staticmethod
	def perform_health_check():
		"""
		This method formats system  data and logs system status to system monitor model
		@return: Systems: a dictionary containing a success code and a list of dictionaries containing  system status
						data
		@rtype:dict
		"""
		systems = []
		try:
			for endpoint in EndpointService().filter(system__state__name = "Active", endpoint_type__is_queried = True):
				try:
					health_state = requests.get(endpoint.url)
					monitor_data = {
						'system': endpoint.system.name,
						'endpoint': endpoint.name,
						'response_body': health_state.content,
						'response_code': health_state.status_code,
						'state': StateService().get(name = 'Operational').name,
					}
					if health_state.status_code == 200:
						if health_state.elapsed > endpoint.optimal_response_time:
							monitor_data.update({
								"response_time_speed": 'Slow', "event_type": EventTypeService().get(name = 'Warning'),
								"description": 'Response time is not within the expected time',
								"state": StateService().get(name = 'Degraded Performance'), "response_time":
									health_state.elapsed.total_seconds()
							})
						else:
							monitor_data.update({
								'response_time_speed': 'Normal', "response_time": health_state.elapsed.total_seconds()
							})
					else:
						monitor_data.update({
							"response_time_speed": None, "event_type": EventTypeService().get(name = 'Critical'),
							"description": 'The system is not accessible', "state": StateService().get(
								name = 'Major Outage')
						})
					system_status = SystemMonitorService().create(
						system = SystemService().get(name = monitor_data.get('system')),
						response_time = timedelta(seconds = int(monitor_data.get('response_time'))),
						response_time_speed = monitor_data.get("response_time_speed"),
						state = StateService().get(name = monitor_data.get('state')),
						response_body = monitor_data.get("response_body"),
						endpoint = EndpointService().get(name = monitor_data.get("endpoint")),
						response_code = monitor_data.get("response_code")
					)
					if system_status is not None:
						systems.append({
							"system": system_status.system.name, "status": system_status.state.name,
							"endpoint": endpoint.url
						})
					else:
						systems.append({
							"system": system_status.system, "status": "failed", "endpoint": endpoint
						})
					if monitor_data.get("event_type") is not None:
						event = EventLog.log_event(
							event_type = monitor_data.get("event_type").name, system = monitor_data.get("system").id,
							description = monitor_data.get("description"), response = monitor_data.get('response'),
							request = health_state.request
						)
						if event['code'] != "800.200.001":
							lgr.warning("Event creation failed %s" % event)
				except requests.ConnectionError as e:
					lgr.exception('Endpoint health check failed:  %s' % e)
			return {"code": "800.200.001", "data": {"systems": systems}}
		except Exception as ex:
			lgr.exception("Health Status exception:  %s" % ex)
		return {"code": "800.400.001", "message": "Error while performing health check"}

	@staticmethod
	def get_system_endpoint_response_time(system_id, start_date, end_date):
		"""
		Returns the response time of every endpoint for a specific system
		@param end_date: End date of the period of which the data is to be extracted
		@type:str
		@param start_date: Start point of the data to be presented
		@type: str
		@param: system_id: Id of the system
		@type system_id: str
		@return: Response code indicating status and response time graph data
		"""
		try:
			system = SystemService().get(pk = system_id, state__name = 'Active')
			if not system:
				return {'code': '800.400.200'}
			now = timezone.now()
			start_date = dateutil.parser.parse(start_date)
			end_date = dateutil.parser.parse(end_date)
			period = start_date - end_date
			dataset = []
			if period.days <= 1:
				for i in range(1, 25):
					past_hour = now - timedelta(hours = i, minutes = 0)
					current_hour = past_hour + timedelta(hours = 1)
					response_times = list(SystemMonitorService().filter(
						system = system, date_created__lte = current_hour,
						date_created__gte = past_hour).values(
						color = F('endpoint__color'),
						name = F('endpoint__name'), responseTime = F('response_time'),
						dateCreated = F('date_created')))
					result = {"Initial": {"data": [0]}}
					for response_time in response_times:
						response_time.update(
							responseTime = timedelta.total_seconds(response_time.get('responseTime')),
							dateCreated = response_time["dateCreated"]
						)
						dataset.append(response_time)
					if dataset:
						result = join_repetitive_dictionaries(dataset)

			elif period.days <= 7:
				for i in range(0, 7):
					current_day = now - timedelta(days = i, hours = 0, minutes = 0)
					past_day = current_day + timedelta(days = 1)
					response_times = list(SystemMonitorService().filter(
						system = system, date_created__lte = past_day,
						date_created__gte = current_day).values(
						color = F('endpoint__color'),
						name = F('endpoint__name'), responseTime = F('response_time'),
						dateCreated = F('date_created')))
					result = {"Initial": {"data": [0]}}
					for response_time in response_times:
						response_time.update(
							responseTime = timedelta.total_seconds(response_time.get('responseTime')),
							dateCreated = response_time["dateCreated"]
						)
						dataset.append(response_time)
					if dataset:
						result = join_repetitive_dictionaries(dataset)
			elif period.days <= 31:
				for i in range(0, 31):
					current_day = now - timedelta(days = i, hours = 0, minutes = 0)
					past_day = current_day + timedelta(days = 1)
					response_times = list(SystemMonitorService().filter(
						system = system, date_created__lte = past_day,
						date_created__gte = current_day).values(
						color = F('endpoint__color'),
						name = F('endpoint__name'), responseTime = F('response_time'),
						dateCreated = F('date_created')))
					result = {"Initial": {"data": [0]}}
					for response_time in response_times:
						response_time.update(
							responseTime = timedelta.total_seconds(response_time.get('responseTime')),
							dateCreated = response_time["dateCreated"]
						)
						dataset.append(response_time)
					if dataset:
						result = join_repetitive_dictionaries(dataset)
			elif period.days <= 365:
				current_date = now.replace(day = 1, hour = 0, minute = 0, second = 0, microsecond = 0)
				current_month = now.month
				current_date = current_date.replace(
					day = 1, hour = 0, minute = 0, second = 0, microsecond = 0) + timedelta(
					days = calendar.monthrange(current_date.year, current_month)[1] - 1)
				for i in range(1, 13):
					if current_month > 1:
						end_date = current_date
						start_date = current_date - timedelta(
							days = calendar.monthrange(end_date.year, end_date.month)[1] - 1)
						current_date = current_date - timedelta(
							days = calendar.monthrange(current_date.year, current_month)[1])
						current_month = current_month - 1
					else:
						end_date = current_date
						start_date = current_date - timedelta(
							days = calendar.monthrange(end_date.year, end_date.month)[1] - 1)
						current_date = current_date - timedelta(
							days = calendar.monthrange(current_date.year, current_month)[1])
						current_month = current_date.month
					response_times = list(SystemMonitorService().filter(
						system = system, date_created__lte = end_date,
						date_created__gte = start_date).values(
						'color',
						name = F('endpoint__name'), responseTime = F('response_time'),
						dateCreated = F('date_created')))
					result = {"Initial": {"data": [0]}}
					for response_time in response_times:
						response_time.update(
							responseTime = timedelta.total_seconds(response_time.get('responseTime')),
							dateCreated = response_time["dateCreated"]
						)
						dataset.append(response_time)
					if dataset:
						result = join_repetitive_dictionaries(dataset)

			return {'code': '800.200.001', 'data': result}
		except Exception as ex:
			lgr.exception("Get Error rate Exception %s" % ex)
		return {'code': '800.400.001'}


def join_repetitive_dictionaries(data):
	"""

	@param data: a dictionary holding data
	@type: dict
	@return:
	"""
	result = {}
	graph_data = []
	colors = []
	for row in data:
		if row["name"] in result:
			result[row["name"]]["series"].append(dict(value=row["responseTime"], name=row["dateCreated"]))
		else:
			result[row["name"]] = {
				"name": row["name"],
				"series": [dict(value = row["responseTime"], name = row["dateCreated"])],
				"color": row["color"]
			}
	for key in result.keys():
		graph_data.append(result[key])
	return graph_data
