import pytest
from mixer.backend.django import mixer

from api.backend.interfaces.notification_interface import NotificationLogger
from django.contrib.auth.models import User

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
		notification = NotificationLogger().send_notification(
			recipients = ["alovegakevin@gmail.com", "kevin@yahoo.com"], message = 'Hey Listen to BBC news today',
			message_type = message_type.name,
		)
		assert notification.get('code') == '800.200.001', "Should successfully send and log notifications"

	def test_fail_notification_logger(self):
		"""Tests failed notification send due to invalid parameters"""
		state = mixer.blend('base.State', name = 'Active')
		mixer.blend('core.System', state = state)
		mixer.blend('base.EscalationLevel')
		mixer.cycle(2).blend(User)
		notification = NotificationLogger().send_notification(
			recipients = [0773444333], message = 'Hey Listen to BBC news today', message_type = 'Invalid',
		)
		assert notification.get('code') == '200.400.005', "Should return a code show that notifications were not sent"

	def test_calling_send_notification_with_missing_parameters(self):
		"""Tests failed notification send due to missing parameters"""
		mixer.blend('base.State', name = 'Sent')
		mixer.blend('base.State', name = 'Failed')
		state = mixer.blend('base.State', name = 'Active')
		mixer.blend('core.System', state = state)
		mixer.blend('base.EscalationLevel')
		mixer.blend(User, first_name = 'Kevin', phone_number= +254776054478)
		mixer.blend(User, first_name = 'Elly', email= 'alovegakevin@gmail.com')
		mixer.blend('base.NotificationType', name = 'SMS')
		notification = NotificationLogger().send_notification(
			recipients ='', message = '', message_type = '',
		)

		assert notification.get('code') == '800.400.002', "Should return code for missing parameters"
