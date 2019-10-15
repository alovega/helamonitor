import pytest
from mixer.backend.django import mixer

from api.backend.interfaces.endpoint_administration import EndpointAdministrator

pytestmark = pytest.mark.django_db


class TestEndpointAdministration(object):
	"""
    class for testing endpoint administration
    """

	def test_create_endpoint(self):
		state = mixer.blend('base.State', name = 'Active')
		endpoint_type = mixer.blend('base.EndpointType', state = state, name = 'health_endpoint')
		system = mixer.blend('core.System', state = state)
		endpoint = EndpointAdministrator.create_endpoint(
			state_id = state.id, endpoint_type_id = endpoint_type.id, system_id = system.id,
			endpoint = "https://mail.google.com", name = "mail", description = "Endpoint for Google mail",
			response_time = 5
		)
		endpoint2 = EndpointAdministrator.create_endpoint(
			state_id = state.id, endpoint_type_id = endpoint_type.id, system_id = system.id,
			endpoint = "https://mail.google.com", name = "mail", description = "Endpoint for Google mail",
			response_time = 5
		)
		endpoint3 = EndpointAdministrator.create_endpoint(
			state_id = state.id, endpoint_type_id = endpoint_type.id, system_id = system.id,
			endpoint = "https://mail.google.com", name = "", description = "Endpoint for Google mail",
			response_time = 5
		)
		assert endpoint.get('code') == '800.200.001', "Should create an endpoint"
		assert endpoint2.get('code') == '200.400.007', "Should return error code"
		assert endpoint2.get('message') == 'An endpoint with this url or name exists'
		assert endpoint3.get('code') == '800.400.002', "Should return error code for missing parameters"

	def test_update_endpoint(self):
		state = mixer.blend('base.State', name = 'Active')
		endpoint_type = mixer.blend('base.EndpointType', state = state, name = 'health_endpoint')
		system = mixer.blend('core.System', state = state)
		endpoint = mixer.blend(
			'core.Endpoint', state = state, endpoint_type = endpoint_type, system = system,
			endpoint = "https://mail.google.com", name = "mail", description = "Endpoint for Google mail",
			response_time = 5
		)
		updated_endpoint = EndpointAdministrator.update_endpoint(
			endpoint.id,  state.id, description = "Google mail", response_time = 3,
			endpoint = "https://mail.googl.com", name = "mail"
		)
		updated_endpoint2 = EndpointAdministrator.update_endpoint(
			endpoint.id, state.id, description = "Google mail", response_time = 3,
			endpoint = "https://mail.googl.com", name = ""
		)
		assert updated_endpoint.get('code') == '800.200.001', "Should update an endpoint"
		assert updated_endpoint2.get('code') == '800.400.002', "Should update an endpoint"
