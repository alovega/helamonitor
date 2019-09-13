import datetime
import logging

import requests

from core.backend.services import SystemMonitorService, EndpointService
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
			for endpoint in EndpointService().filter(
					system__state__name = "Active", endpoint_type__is_queried = True, state__name = 'Active'
			):
				health_state = requests.get(endpoint.endpoint)  # this stores the response of the  http request on url
				status_data = {
					"system": endpoint.system,
					"response_time": datetime.timedelta(seconds = health_state.elapsed.total_seconds()),
					"endpoint": endpoint, "response": health_state.content, "state": StateService().get(name = 'Active')
				}
				if health_state.status_code == 200:
					if health_state.elapsed > endpoint.optimal_response_time:
						status_data.update({
							"response_time_speed": 'Slow', "event_type": EventTypeService().get(name = 'Debug'),
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
							"endpoint": endpoint.endpoint
						})
				else:
					systems.append({
							"system": system_status.system.name, "status": "failed", "endpoint": endpoint.endpoint
						})

				if status_data.get("event_type") is not None:
					event = EventLog().log_event(
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
