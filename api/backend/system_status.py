
import logging

from core.backend.services import SystemMonitorService, EventService, InterfaceService, EndpointService
from base.backend.services import StateService, EventTypeService

lgr = logging.getLogger(__name__)


class MonitorProcessor(object):
	"""
	class for logging status  of  system micro-services
	"""

	def __init__(self, **kwargs):
		self.kwargs = kwargs

	def save_system_status(self, **kwargs):
		"""
		:param kwargs:
			This is a variable type dictionary containing data that my request method will return
			The kwargs will contain :-
				1.response_status whether 200 or 4**(error) which will be used to determine whether an event will be created
				2.response this will be the response the request has returned
				3.request this is the http request method that was performed
				4.url this is the endpoint url that was used. It is tied to an endpoint
				5.response_time lastly the response_time self explanatory
		:return: system_status
		"""
		try:
			endpoint = EndpointService().get(endpoint=kwargs.get('url'))
			response_time = kwargs.get('response_time')
			system = endpoint.system
			interface = InterfaceService().get(system = system)
			state = StateService().get(name='UP')
			request = kwargs.get('request')
			response = kwargs.get('response')
			code = kwargs.get('code')
			method = kwargs.get('method', None)
		except Exception as e:
			lgr.exception("Status Log exception: %s" % e)

		if kwargs is not None:
			if kwargs['status_code'] == 200:
				status_data = {"system": system, "response_time": response_time, "endpoint": endpoint, "state": state}
				try:
					system_status = SystemMonitorService().create(**status_data)  # creates a system_status object
					event = self.analyse_response_time(
						system_status=system_status, desired_time = system_status.endpoint.optimal_response_time
					)
					return system_status, event
				except Exception as e:
					lgr.exception("Status Log exception: %s" % e)

			else:
				new_state = StateService().get(name='Down')
				event_type = EventTypeService().get(name='Critical')
				status_data = {"system": system, "response_time": None, "endpoint": endpoint, "state": new_state}
				event_data = {
					"system": system, "response_time": None, "description": response,
					"method": method, "response": response, "request": request, "interface": interface,
					"event_type": event_type, "state": new_state, "code": code,
				}
				try:
					# creates a system_status object
					system_status = SystemMonitorService().create(**status_data)
					# should refactor and  call the processor for creating event
					event = EventService().create(**event_data)
					return system_status, event
				except Exception as e:
					lgr.exception("Status Log exception: %s" % e)

	@staticmethod
	def analyse_response_time(system_status, desired_time):
		"""
		This method analyses the created system_status response time is within the desired time
		:param system_status:
		:param desired_time: a set time that a response_time must meet for it's request to be considered okay
		:return: event
		"""
		if system_status.response_time > desired_time:
			description = "%s is okay but with a slow response time" % system_status.endpoint
			event_type = EventTypeService.get(name = 'Debug')
			method = None
			response = None
			request = None
			code = None
			interface = InterfaceService().get(system = system_status.system)
			event_data = {
				"system": system_status.system, "response_time": system_status.response_time,
				"description": description,"method": method, "response": response, "request": request,
				"interface": interface,"event_type": event_type, "state": system_status.state, "code": code,
			}
			try:
				# should refactor and  call the processor for creating event
				event = EventService().create(**event_data)
				return event
			except Exception as e:
				lgr.exception("Event Log exception: %s" % e)

	def generate_status_report(self):
		pass
