
import logging

from core.backend.services import SystemMonitorService, EventService, InterfaceService, SystemService, EndpointService
from base.backend.services import StateService, EventTypeService, EscalationLevelService

lgr = logging.getLogger(__name__)


class MonitorProcessor(object):
	"""
	class for logging status  of  system micro-services
	"""
	system_status = None

	def save_system_status(self, **kwargs):
		"""
		This method  creates  system status for monitoring purposes
		:param kwargs:
		:return: system_status
		"""
		if self.system_status is None:
			if kwargs['code'] == 200:
				system = SystemService().get(name=kwargs['system'])
				status = StateService().get(name='operational')
				endpoint = EndpointService().get(endpoint=kwargs['url'])
				data1 = {
					"system": system,
					"status_code": kwargs['response']['code'],
					"code": kwargs['code'],
					"version": system.version,
					"response_time": kwargs['response_time'],
					"endpoint": endpoint,
					"state": status
				}
				try:
					self.system_status = SystemMonitorService().create(**data1)  # creates a system_status object
					# event = self.analyse_system_status(
					# 	system_status = self.system_status, desired_time = self.system_status.endpoint.default_time,
					# 	**data1
					# )  # analyse whether to create an event based on the logged status and response time
					return self.system_status #event
				except Exception as e:
					lgr.exception("Status Log exception: %s" % e)

			else:
				system = SystemService().get(name = kwargs['system'])
				interface = InterfaceService().get(system=kwargs['system']),
				event_type = EventTypeService.get(name='Error'),
				escalation_level = EscalationLevelService.get(name='High'),
				status = StateService().get(name='not operational')
				data1 = {
					"system": system,
					"version": system.version,
					"response_time": None,
					"description": kwargs['message'],
					"interface": interface,
					"method": kwargs['message'],
					"response": kwargs['response'].json(),
					"request": kwargs['response'].request.method,
					"event_type": event_type,
					"state": status,
					"escalation_level": escalation_level,
					"status_code": kwargs['response']['code'],
				}

				try:
					self.system_status = SystemMonitorService().create(**data1)  # creates a system_status object
					event = EventTypeService().create(**data1) # creates an Event object
					return self.system_status, event
				except Exception as e:
					lgr.exception("Status Log exception: %s" % e)

	@staticmethod
	def analyse_system_status(system_status, desired_time, **kwargs):
		"""
		This method analyses the created system_status response time is within the desired time
		:param system_status:
		:param desired_time: a set time that a response_time must meet for it's request to be considered okay
		:param kwargs: this is a dictionary of data to be used by EventService() object
		:return: event
		"""
		if system_status.response_time > desired_time:
			description = "%s is okay but with a slow response time" % system_status.endpoint
			event_type = EventTypeService.get(name='Debug')
			escalation_level = EscalationLevelService.get(name = 'Low')
			method = None
			response = kwargs['response'].json()
			request = kwargs['response'].request.method
			interface = InterfaceService().get(system = kwargs['system']),

			try:
				event = EventService().create(
					description, event_type, escalation_level, method, request, response, interface,  **kwargs
				)
				return event
			except Exception as e:
				lgr.exception("Event Log exception: %s" % e)

	def generate_status_report(self):
		pass
