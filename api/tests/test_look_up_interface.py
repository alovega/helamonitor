import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User

from api.backend.interfaces.look_up_interface import LookUpInterface

pytestmark = pytest.mark.django_db


class TestLookupInterface(object):
	"""
	class for testing look up interface
	"""
	def test_get_look_up_data(self):
		state = mixer.cycle(2).blend('base.State')
		event_type = mixer.cycle(2).blend('base.EventType')
		escalation_level = mixer.cycle(2).blend('base.EscalationLevel')
		states = LookUpInterface.get_look_up_data()
		assert states.get('code') == '800.200.001'
