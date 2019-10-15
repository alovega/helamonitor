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
		endpoint_type = mixer.blend('base.EndpointType', state=state, name = 'health_endpoint')
		system = mixer.blend('core.System', state=state)
		endpoint = EndpointAdministrator.create_endpoint(
			state_id=state.id, endpoint_type_id=endpoint_type.id, system_id = system.id,
			endpoint = "https://mail.google.com", name = "mail", description = "Endpoint for Google mail",
			response_time = 5
		)
		endpoint2 = EndpointAdministrator.create_endpoint(
			state_id = state.id, endpoint_type_id = endpoint_type.id, system_id = system.id,
			endpoint = "https://mail.google.com", name = "mail", description = "Endpoint for Google mail",
			response_time = 5
		)
		assert endpoint.get('code') == '800.200.001', "Should create an endpoint"
		assert endpoint2.get('code') == '200.400.007', "Should return error code"
		assert endpoint2.get('message') == 'An endpoint with this url exists'
