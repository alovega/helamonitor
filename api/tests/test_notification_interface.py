import pytest
from mixer.backend.django import mixer

from api.backend.interfaces.notification_interface import NotificationLogger
from core.backend.services import SystemRecipientService

pytestmark = pytest.mark.django_db


class TestIncidentLogger(object):
	"""
	Class for testing incident logger
	"""

	def test_notification_logger(self):
		state = mixer.blend('base.State', name = 'Active')
		system = mixer.blend('core.System', state = state)
		state2 = mixer.blend('base.State', name = 'Sent')
		escalation_level = mixer.blend('base.EscalationLevel')
		recipient = mixer.blend('core.Recipient', first_name = 'Kevin', state = state)
		system_recipient = SystemRecipientService().create(
			recipient = recipient, system = system, state = state, escalation_level = escalation_level
		)
		message_type = mixer.blend('base.NotificationType', name = 'SMS')
		message = 'Hey Listen to BBC news today'

		notification = NotificationLogger().send_notification(
			recipient = recipient, message = message, message_type = message_type,
		)

		assert notification == {'code': '800.200.001'}, "Should create an incident %s " % notification
