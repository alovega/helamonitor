import datetime
import logging

import requests
from django.db.models import F
from django.utils import timezone
from datetime import timedelta
from core.backend.services import SystemMonitorService, EndpointService, SystemService
from base.backend.services import StateService, EventTypeService

from api.backend.interfaces.event_log import EventLog

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
				health_state = requests.get(endpoint.url)  # this stores the response of the  http request on url
				status_data = {
					"system": endpoint.system,
					"response_time": datetime.timedelta(seconds = health_state.elapsed.total_seconds()),
					"endpoint": endpoint, "response": health_state.content,
					"state": StateService().get(name = 'Active')
				}
				if health_state.status_code == 200:
					if health_state.elapsed > endpoint.optimal_response_time:
						status_data.update({
							"response_time_speed": 'Slow', "event_type": EventTypeService().get(name = 'Warning'),
							"description": 'Response time is not within the expected time'
						})
					else:
						status_data.update({
							"response_time_speed": 'Normal',
						})
				else:
					status_data.update({
						"response_time_speed": None,
						"event_type": EventTypeService().get(name = 'Critical'),
						"description": 'The system is not accessible',
						"state": StateService().get(name = 'Down')
					})
				system_status = SystemMonitorService().create(
					system = status_data.get("system"), response_time = status_data.get("response_time"),
					response_time_speed = status_data.get("response_time_speed"), response = status_data.get(
						"response"), endpoint = status_data.get("endpoint"), state = status_data.get('state')
				)
				if system_status is not None:
					systems.append({
						"system": system_status.system.name, "status": system_status.state.name,
						"endpoint": endpoint.url
					})
				else:
					systems.append({
						"system": system_status.system.name, "status": "failed", "endpoint": endpoint.endpoint
					})

				if status_data.get("event_type") is not None:
					event = EventLog.log_event(
						event_type = status_data.get("event_type").name, system = status_data.get("system").name,
						description = status_data.get("description"), response = status_data.get('response'),
						request = health_state.request
					)
					if event['code'] != "800.200.001":
						lgr.warning("Event creation failed %s" % event)
			return {"code": "800.200.001", "data": {"systems": systems}}
		except Exception as e:
			lgr.exception("Health Status exception:  %s" % e)
		return {"code": "800.400.001", "data": "Error while logging system status"}

	@staticmethod
	def get_system_endpoint_response_time(system_id):
		"""
		Returns the response time of every endpoint for a specific system
		@param: system_id: Id of the system
		@type system_id: str
		@return: Response code indicating status and response time graph data
		"""
		try:
			system = SystemService().get(pk = system_id, state__name = 'Active')
			if not system:
				return {'code': '800.400.200'}
			now = timezone.now()
			labels = []
			label = []
			dataset = []
			for i in range(1, 25):
				past_hour = now - timedelta(hours = i, minutes = 0)
				current_hour = past_hour + timedelta(hours = 1)
				response_times = list(SystemMonitorService().filter(
					system = system, date_created__lte = current_hour,
					date_created__gte = past_hour).values(
					name= F('endpoint__name'), responseTime = F('response_time'),
					dateCreated=F('date_created')))
				past_hour = past_hour.replace(minute = 0)
				label.append(past_hour.strftime("%m/%d/%y  %H:%M"))
				result = {"Initial": {"data": [0]}}
				for response_time in response_times:
					response_time.update(
						responseTime=timedelta.total_seconds(response_time.get('responseTime')),
						dateCreated= response_time["dateCreated"].strftime("%m/%d/%y  %H:%M")
					)
					dataset.append(response_time)
					labels.append(response_time['dateCreated'])
				if dataset:
					label = []
					[label.append(item) for item in labels if item not in label]
					result = {}
					for row in dataset:
						if row["name"] in result:
							result[row["name"]]["data"].append(row["responseTime"])
							result[row["name"]]["dateCreated"].append(row["dateCreated"])
						else:
							result[row["name"]] = {
								"label": row["name"],
								"data": [row["responseTime"]],
								"dateCreated": [row["dateCreated"]],
							}
			return {'code': '800.200.001', 'data': {'labels': label, 'datasets': result}}
		except Exception as ex:
			lgr.exception("Get Error rate Exception %s" % ex)
		return {'code': '800.400.001'}
