import pytest
from mixer.backend.django import mixer

from base.backend.services import StateService

pytestmark = pytest.mark.django_db


class TestStateService(object):
    """
	Test the State Model Services
	"""

    def test_get(self):
        """
		Test State get service
		"""
        mixer.blend('base.State', name="Active")
        state = StateService().get(name="Active")
        assert state is not None, 'Should have an State object'

    def test_filter(self):
        """
		Test State filter service
		"""
        mixer.cycle(3).blend('base.State')
        states = StateService().filter()
        assert len(states) == 3, 'Should have 3 State objects'

    def test_create(self):
        """
		Test State create service
		"""
        state = StateService().create(name = "Active")
        assert state is not None, 'Should have a State object'
        assert state.name == "Active", "Created State name is equals to Active"

    def test_update(self):
        """
		Test State update service
		"""
        state = mixer.blend('base.State')
        state = StateService().update(state.id, name = "Active")
        assert state.name == "Active", 'Should have the same name'