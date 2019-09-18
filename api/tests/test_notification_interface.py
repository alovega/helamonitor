import pytest
from mixer.backend.django import mixer

from api.backend.interfaces.notification_interface import NotificationLogger
from django.contrib.auth.models import User
from core.backend.services import SystemRecipientService

pytestmark = pytest.mark.django_db


class TestIncidentLogger(object):
	"""
	Class for testing incident logger
	"""

	def test_notification_logger(self):
		state2 = mixer.blend('base.State', name = 'Sent')
		state3 = mixer.blend('base.State', name = 'Failed')
		state = mixer.blend('base.State', name = 'Active')
		recipient1 = mixer.blend(User, first_name = 'Kevin', email = 'alovegakevin@gmail.com', state = state)
		recipient2 = mixer.blend(User, first_name = 'Elly', email='kevin@yahoo.com',
		                         state = state
		)
		message_type = mixer.blend('base.NotificationType', name = 'Email')

		message = 'Hey Listen to BBC news today'

		notification = NotificationLogger().send_notification(
			recipients = ["alovegakevin@gmail.com", "kevin@yahoo.com"], message = message, message_type =
			message_type.name,
		)

		assert notification == {'code': '800.200.001'}, "Should create an incident %s " % notification

	def test_fail_notification_logger(self):
		state2 = mixer.blend('base.State', name = 'Sent')
		state3 = mixer.blend('base.State', name = 'Failed')
		state = mixer.blend('base.State', name = 'Active')
		system = mixer.blend('core.System', state = state)
		escalation_level = mixer.blend('base.EscalationLevel')
		recipient1 = mixer.blend(User, first_name = 'Kevin', email = 'alovegakevin@gmail.com')
		recipient2 = mixer.blend(User, first_name = 'Elly', email='alwavegaKevin@gmail.com')

		message_type = mixer.blend('base.NotificationType', name = 'SMS')

		message = 'Hey Listen to BBC news today'

		notification = NotificationLogger().send_notification(
			recipients = [0773444333], message = message, message_type = message_type.name,
		)

		assert notification == {'code': '800.200.001'}, "Should create a notification %s " % notification

	def test_calling_send_notification_with_missing_parameters(self):
		state2 = mixer.blend('base.State', name = 'Sent')
		state3 = mixer.blend('base.State', name = 'Failed')
		state = mixer.blend('base.State', name = 'Active')
		system = mixer.blend('core.System', state = state)
		escalation_level = mixer.blend('base.EscalationLevel')
		recipient1 = mixer.blend(User, first_name = 'Kevin', phone_number= +254776054478)
		recipient2 = mixer.blend(User, first_name = 'Elly', email= 'alovegakevin@gmail.com')
		message_type = mixer.blend('base.NotificationType', name = 'SMS')

		message = 'Hey Listen to BBC news today'

		notification = NotificationLogger().send_notification(
			recipients ='', message = '', message_type = '',
		)

		assert notification == {'code': '800.400.002'}, "Should return code for missing parameters %s " % notification
