import pytest
from mixer.backend.django import mixer

from api.backend.interfaces.notification_interface import NotificationLogger
from core.models import User

pytestmark = pytest.mark.django_db


class TestIncidentLogger(object):
	"""
	Class for testing incident logger
	"""

	def test_notification_logger(self):
		"""Tests successful notification sending"""
		mixer.blend('base.State', name = 'Sent')
		mixer.blend('base.State', name = 'Failed')
		state = mixer.blend('base.State', name = 'Active')
		mixer.cycle(2).blend(User, state = state)
		message_type = mixer.blend('base.NotificationType', name = 'Email')
		system = mixer.blend('core.System', name='System 1')
		notification = NotificationLogger().send_notification(
			recipients = ["alovegakevin@gmail.com", "kevin@yahoo.com"], message = 'Hey Listen to BBC news today',
			message_type = message_type.name, system_id = system.id
		)
		assert notification.get('code') == '800.200.001', "Should successfully send and log notifications"

	def test_calling_send_notification_with_missing_parameters(self):
		"""Tests  send notification function missing parameters"""
		mixer.blend('base.State', name = 'Sent')
		mixer.blend('base.State', name = 'Failed')
		state = mixer.blend('base.State', name = 'Active')
		system = mixer.blend('core.System', state = state)
		mixer.blend('base.EscalationLevel')
		recipient= mixer.blend(User, first_name = 'Kevin', phone_number= +254776054478)
		mixer.blend(User, first_name = 'Elly', email= 'alovegakevin@gmail.com')
		message_type = mixer.blend('base.NotificationType', name = 'SMS')
		notification = NotificationLogger().send_notification(
			recipients =[recipient.id], message = 'sample', message_type = message_type.name, system_id = system.id
		)
		notification2 = NotificationLogger().send_notification(
			recipients = [recipient.id], message = 'sample', message_type = message_type.id, system_id = system.id
		)
		notification3 = NotificationLogger().send_notification(
			recipients = '', message = '', message_type = '', system_id = ''
		)

		assert notification.get('code') == '800.200.001', "Should return code for missing parameters"
		assert notification2.get('code') == '200.400.005', "Should return error code showing no message data was " \
		                                                   "created"
		assert notification3.get('code') == '800.400.002', "error code for missing parameters"

