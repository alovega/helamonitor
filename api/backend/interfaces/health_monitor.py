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
		systems_status = {}
		try:
			for endpoint in EndpointService().filter(
					system__state__name ="Active", endpoint_type__is_queried = True, state__name='Active'
			):
				health_state = requests.get(endpoint.endpoint)  # this stores the response of the  http request on url
				system_status = SystemMonitorService().create(
					system = endpoint.system,
					response_time = datetime.timedelta(seconds = health_state.elapsed.total_seconds()),
					endpoint = endpoint, response = health_state.content, state = StateService().get(name = 'Active')
				)
				if system_status is not None:
					if health_state.status_code == 200:
						system_status = system_status
						if health_state.elapsed > endpoint.optimal_response_time:
							system_status = SystemMonitorService().update(
								system_status.id, response_time_state=ResponseTimeStateService().get(name='Slow')
							)
							# to do an event log by calling its processor
							systems_status[system_status.system.name] = system_status

						else:
							system_status = SystemMonitorService().update(
								system_status.id, response_time_state = ResponseTimeStateService().get(name = 'Okay')
							)
							systems_status[system_status.system.name] = system_status

					else:
						system_status = SystemMonitorService().update(
							system_status.id, state=StateService().get(name='Down')
						)
						#  to do an event log by calling its processor
						event = 'some event'
						if system_status is not None and event is not None:
							systems_status[system_status.system.name] = system_status
			return {"systems": systems_status}
		except Exception as e:
			lgr.exception("Health Status exception:  %s" % e)
			return {"message": "Error while logging"}

	def generate_status_report(self):
		pass
