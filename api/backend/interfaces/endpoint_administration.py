import datetime
import logging

from django.db.models import F
from django.utils.duration import duration_string

from core.backend.services import SystemService, EndpointService
from core.models import Endpoint
from base.backend.services import StateService, EndpointTypeService

lgr = logging.getLogger(__name__)


class EndpointAdministrator(object):
	"""
	class for Endpoint Administration
	"""

	@staticmethod
	def create_endpoint(name, description, url, system_id, response_time, endpoint_type_id, state_id):
		"""
		@param name: name of endpoint to be created
		@type name:str
		@param description: description of endpoint to be created
		@type description: str
		@param endpoint: url of endpoint to be created
		@type: str
		@param system_id: id of system the endpoint will belong to
		@type : int
		@param response_time: average response time the endpoint should take
		@type: int
		@param endpoint_type_id: id of endpoint type the endpoint will belong to
		@type endpoint_type_id: int
		@param state_id: the id of  initial state of the created endpoint will have
		@type state_id: int
		@return: Response code dictionary to indicate if the endpoint was created or not
		@rtype:dict
		"""
		try:
			system = SystemService().get(id = system_id, state__name = "Active")
			endpoint_type = EndpointTypeService().get(id = endpoint_type_id, state__name = "Active")
			state = StateService().get(id = state_id)

			if not (system and endpoint_type and state and name and description and response_time and url):
				return {"code": "800.400.002", "message": "Missing parameters"}
			exist = True if EndpointService().filter(system = system, url = url) \
				else EndpointService().filter(system = system, name = name)
			if exist:
				return {"code": "200.400.007", "message": "An endpoint with this url or name exists"}
			endpoint = EndpointService().create(
				name = name, description = description, url = url, system = system,
				endpoint_type = endpoint_type,
				optimal_response_time = datetime.timedelta(seconds = int(response_time)), state = state
			)
			return {"code": "800.200.001", "message": "successfully created endpoint: %s" % endpoint.name}
		except Exception as ex:
			lgr.exception("Endpoint Administration exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error when creating an endpoint"}

	@staticmethod
	def update_endpoint(endpoint_id, state_id, description, url, response_time, name):
		"""
		@param endpoint_id: id of the endpoint to be edited
		@type endpoint_id: int
		@param name: name of endpoint to be created
		@type name: str
		@param description: description of endpoint to be created
		@type description: str
		@param url:url of endpoint to be created
		@type url: str
		@param response_time:average response time the endpoint should take
		@type response_time: int
		@param state_id:the id of  initial state of the created endpoint will have
		@type state_id: int
		@return: Response code dictionary to indicate if the endpoint was updated or not
		@rtype: dict
		"""

		try:
			update_endpoint = EndpointService().get(pk = endpoint_id)
			state = StateService().get(id = state_id)
			if not (state and name and description and response_time and url and update_endpoint):
				return {
					"code": "800.400.002", "message": "Error missing parameters"
				}
			endpoint = EndpointService().update(
				pk = update_endpoint.id, description = description, state = state,
				optimal_response_time = datetime.timedelta(seconds = int(response_time)), url = url
			)
			return {"code": "800.200.001", "message": "successfully updated endpoint: %s" % endpoint.name}

		except Exception as ex:
			lgr.exception("Endpoint Administration exception: %s" % ex)
		return {"code": "800.400.001", "message": "Error when updating an endpoint"}

	@staticmethod
	def get_system_endpoints(system_id):
		"""

		@param system_id: id for an existing system the endpoints belong to
		@type: char
		@return: endpoints:a dictionary containing a success code and a list of dictionaries containing  system
							endpoints data
		@rtype: dict
		"""
		try:
			data = {}
			system = SystemService().get(id = system_id)
			if not system:
				return {"code": "800.400.002", "message": "It seems there is no existing system with such endpoints"}
			endpoints = list(EndpointService().filter(system = system).values(
				'id', 'name', 'description', 'date_modified', 'system__name', dateCreated=F(
					'date_created'), responseTime=F('optimal_response_time'), endpointUrl=F('url'),
				status= F(
					'state__name'),
				type=F('endpoint_type__name')
			).order_by('-date_created'))
			data.update(endpoints = endpoints)
			return {'code': '800.200.001', 'data': data}
		except Exception as ex:
			lgr.exception("Endpoint Administration exception: %s" % ex)
		return {'code': '800.400.001 ', "message": "Error when fetching system endpoints"}

	@staticmethod
	def get_endpoint(endpoint_id):
		"""
		@param endpoint_id: id of the endpoint that is being fetched
		@type endpoint_id:str
		@return: endpoints:a dictionary containing a success code and a list of dictionary containing endpoint data
		@rtype: dict
		"""
		try:
			data = {}
			endpoint = list(EndpointService().filter(id = endpoint_id).values(
				'id', 'name', 'description', 'url', 'optimal_response_time',
				'date_created', 'date_modified', 'system__name', 'endpoint_type__name', 'state__name'
			))
			if not endpoint:
				return {'code': '800.400.001', 'message': 'The endpoint requested does not exist'}
			data.update(endpoint = endpoint)
			return {'code': '800.200.001', 'data': data}
		except Exception as ex:
			lgr.exception("Endpoint Administration exception: %s" % ex)
		return {'code': '800.400.001', "message": "Error when fetching an endpoint"}

	@staticmethod
	def delete_endpoint(endpoint_id):
		"""
		@param endpoint_id:id of the recipient belong you are fetching
		@type endpoint_id: str
		@return:recipients:a dictionary containing a success code and a list of dictionaries containing  system
							endpoint data
		@rtype:dict
		"""
		try:
			if not endpoint_id:
				return {"code": '800.400.002 %s' %endpoint_id}
			endpoint = Endpoint.objects.get(id = endpoint_id)
			endpoint.delete()
			return {'code': '800.200.001', 'message': 'successfully deleted the endpoint'}
		except Exception as ex:
			lgr.exception("Endpoint Administration Exception: %s" % ex)
		return {"code": "800.400.001 ", "message": "Error while deleting endpoint"}
