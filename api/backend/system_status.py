
import logging

import requests

from core.backend.services import SystemMonitorService, EventService, InterfaceService, EndpointService, SystemService
from base.backend.services import StateService, EventTypeService

lgr = logging.getLogger(__name__)


class MonitorProcessor(object):
	"""
	class for logging status  of  system micro-services
	"""

	def __init__(self):
		super(MonitorProcessor, self).__init__()

	def save_system_status(self,  **kwargs):
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
				status_data = {
					"system": system, "response_time": response_time, "endpoint": endpoint, "state": state
				}
				try:
					system_status = SystemMonitorService().create(**status_data)  # creates a system_status object
					event = self.analyse_response_time(
						system_status=system_status, desired_time = system_status.endpoint.optimal_response_time,
						**kwargs
					)
					print system_status.endpoint.optimal_response_time
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
	def analyse_response_time(system_status, desired_time, **kwargs):
		"""
		This method analyses the created system_status response time is within the desired time
		:param system_status:
		:param desired_time: a set time that a response_time must meet for it's request to be considered okay
		:return: event
		"""
		if system_status.response_time > desired_time:
			description = "%s is okay but with a slow response time" % system_status.endpoint
			event_type = EventTypeService().get(name = 'Debug')
			method = None
			response = None
			request = None
			code = kwargs.get('code')
			interface = InterfaceService().get(system = system_status.system)
			event_data = {
				"system": system_status.system, "response_time": system_status.response_time,
				"description": description, "method": method, "response": response, "request": request,
				"interface": interface, "event_type": event_type, "state": system_status.state, "code": code,
			}
			try:
				# should refactor and  call the processor for creating event
				event = EventService().create(**event_data)
				return event
			except Exception as e:
				lgr.exception("Event Log exception: %s" % e)

	def generate_status_report(self):
		pass


def query_health():
	"""
	This function is supposed to filter out all the registered system to be monitored, once it does that from
	the system it got query all the existing endpoints that are supposed to be queried then perform a get request
	on the endpoint from the response create data that is going to be used by the monitor processor and perform
	a call to it and pass data
	"""
	try:
		systems = SystemService().filter()  # get all the registered system
		for system in systems:
			# get all the endpoints belonging to the system that are queried
			endpoints = EndpointService().filter(system = system, endpoint_is_queried = True)
			for endpoint in endpoints:
				url = endpoint.get('endpoint')  # this will have the url that will be queried
				health_state = requests.get(url) # this stores the response of the  http request on url
				status_code = health_state.status_code  # this has the response code for the response
				response_time = health_state.elapsed.total_seconds()
				response = health_state.json()
				request = health_state.request.method
				code = response.get('code')

				# data will be used by MonitorProcessor save_system_status method as a method variable
				data = {
					url: url, status_code: status_code, response_time: response_time, request: request, code: code
				}
				MonitorProcessor().save_system_status(**data)  # logs a system status based on the data
	except Exception as e:
		lgr.exception("Health Status exception:  %s" % e)
