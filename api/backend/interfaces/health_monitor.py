import datetime
import logging

import requests

from core.backend.services import SystemMonitorService, EndpointService
from base.backend.services import StateService, ResponseTimeStateService

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
		systems = {}
		try:
			for endpoint in EndpointService().filter(
					system__state__name ="active", endpoint_type__is_queried = True, state__name='active'
			):
				health_state = requests.get(endpoint.endpoint)  # this stores the response of the  http request on url
				system_status = SystemMonitorService().create(
					system = endpoint.system,
					response_time = datetime.timedelta(seconds = health_state.elapsed.total_seconds()),
					endpoint = endpoint, response = health_state.content, state = StateService().get(name = 'UP')
				)
				print 1234
				print endpoint.optimal_response_time
				if system_status is not None:
					if health_state.status_code == 200:
						system_status = system_status
						if health_state.elapsed > endpoint.optimal_response_time:
							system_status = SystemMonitorService().update(
								system_status.id, response_time_state=ResponseTimeStateService().get(name='Slow')
							)
							# to do an event log by calling its processor
						else:
							system_status = SystemMonitorService().update(
								system_status.id, response_time_state = ResponseTimeStateService().get(name = 'Okay')
							)
					return {"message": "system status logged", "code": 200.001, 'system': system_status}
				else:
					system_status = SystemMonitorService().update(
						system_status.id, state=StateService().get(name='Down')
					)
					#  to do an event log by calling its processor
					event = 'some event'
					if system_status and event:
						return {'system_status': system_status, 'event': event}
					return {"message": "unable to log a the system status", "code": 200.002}

		except Exception as e:
			lgr.exception("Health Status exception:  %s" % e)
			return {"message": "Error while logging"}

	def generate_status_report(self):
		pass



