import datetime
import logging

import requests

from core.backend.services import SystemMonitorService, EndpointService
from base.backend.services import StateService, EventTypeService

# from api.backend.processors.event_log import EventLog

lgr = logging.getLogger(__name__)


class MonitorProcessor(object):
	"""
	class for logging status  of  system micro-services
	"""
	@staticmethod
	def perform_health_check():
		"""
		@return: system status
		"""
		systems_status = {}
		try:
			for endpoint in EndpointService().filter(
					system__state__name ="Active", endpoint_type__is_queried = True, state__name='Active'
			):
				health_state = requests.get(endpoint.endpoint)  # this stores the response of the  http request on url
				status_data = {
					"system": endpoint.system,
					"response_time": datetime.timedelta(seconds = health_state.elapsed.total_seconds()),
					"endpoint": endpoint, "response": health_state.content, "state": StateService().get(name='Active')
				}
				if health_state.status_code == 200:
					if (health_state.elapsed > endpoint.optimal_response_time) and (
							health_state.elapsed < datetime.timedelta(seconds=2)):
						status_data.update({
							"response_time_speed": 'Slow', "event_type": EventTypeService().get(name='Debug'),
							"description": 'Response time is not within the expected time'
						})
					elif (health_state.elapsed > endpoint.optimal_response_time) and (
							health_state.elapsed > datetime.timedelta(seconds=2)):
						status_data.update({
							"response_time_speed": 'Extremely Slow',
							"event_type": EventTypeService().get(name = 'Warning'),
							"description": 'The system response is extremely'
						})
					else:
						status_data.update({
							"response_time_speed": 'Normal',
						})
				else:
					status_data.update({
						"response_time_speed": None,
						"event_type": EventTypeService().get(name='Critical'),
						"description": 'The system response is extremely',
						"state": StateService().get(name='Down')
					})
					#  to do an event log by calling its processor
				system_status = SystemMonitorService().create(
					system=status_data.get("system"), response_time=status_data.get("response_time"),
					response_time_speed = status_data.get("response_time_speed"), response=status_data.get(
						"response"), endpoint=status_data.get("endpoint"), state = status_data.get('state')
				)
				# if status_data.get("event_type") is not None:
				# 	event = EventLog().log_event(
				# 		event_type=status_data.get("event_type"), system=status_data.get("system"),
				# 		description=status_data.get("description"), response= status_data.get('response'),
				# 		request= health_state.request
				# 	)
				if system_status is not None:  # and event is not None:
					systems_status.update({"system": system_status.system.name, "status": system_status.state.name})
				else:
					return {"code": "200.400.004"}
			return {"systems": systems_status}
		except Exception as e:
			lgr.exception("Health Status exception:  %s" % e)
			return {"message": "Error while logging"}

	def generate_status_report(self):
		pass
