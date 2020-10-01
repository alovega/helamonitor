import pytest
from mixer.backend.django import mixer

from api.backend.interfaces.recipient_administration import RecipientAdministrator

pytestmark = pytest.mark.django_db


class TestRecipientAdministration(object):
	"""
	class for testing recipient Administration
	"""

	def test_delete_system_recipient(self):
		state = mixer.blend('base.State', name = 'Active')
		recipient = mixer.blend('core.User', state = state)
		data = RecipientAdministrator.delete_recipient(system_recipient_id=recipient.id)
		data2 = RecipientAdministrator.delete_recipient(system_recipient_id = '')
		assert data.get('code') == '800.200.001'
		assert data2.get('code') == '800.400.002'

	def test_create_system_recipients(self):
		state = mixer.blend('base.State', name = 'Active')
		escalation_level = mixer.blend('base.EscalationLevel', state = state)
		recipient = mixer.blend('core.User', state = state)
		notification = mixer.blend('core.Notification', state=state)
		system = mixer.blend('core.System', state = state)
		data = RecipientAdministrator.create_system_recipient(
			system_id = system.id,
			escalations = [{"NotificationType": notification.id, "EscalationLevel": escalation_level.id}],
			user_id = recipient.id
		)
		data2 = RecipientAdministrator.create_system_recipient(
			system_id = system.id,
			escalations = [{"NotificationType": notification.id, "EscalationLevel": escalation_level.id}],
			user_id = recipient.id
		)
		assert data.get('code') == '800.200.001', "should create system recipients"
		assert data2.get('code') == '800.400.001', "Should return Error indicating unable to create system recipient "

	def test_update_system_recipients(self):
		state = mixer.blend('base.State', name = 'Active')
		escalation_level = mixer.blend('base.EscalationLevel', state = state)
		recipient = mixer.blend('core.User', state = state)
		notification = mixer.blend('core.Notification', state=state)
		system = mixer.blend('core.System', state = state)
		system_recipient = mixer.blend('core.SystemRecipient', recipient=recipient)
		data = RecipientAdministrator.update_system_recipient(
			recipient_id = recipient.id,
			escalations = [{"NotificationType": notification.id, "EscalationLevel":escalation_level.id}],
		)
		data2 = RecipientAdministrator.update_system_recipient(
			recipient_id = system.id,
			escalations = [{"NotificationTYpe": notification.id, "EscalationLevel": escalation_level.id}],
		)
		assert data.get('code') == '800.200.001', "should update system recipients"
		assert data2.get('code') == '800.400.001', "Should return an error showing unable to update system recipient"

	def test_get_system_recipients(self):
		state = mixer.blend('base.State', name = 'Active')
		recipient = mixer.blend('core.User', state = state)
		system = mixer.blend('core.System', state = state)
		system_recipient = mixer.blend('core.SystemRecipient', recipient = recipient)
		data = RecipientAdministrator.get_system_recipient(
			user_id = recipient.id, system_id = system.id
		)
		data2 = RecipientAdministrator.get_system_recipient(
			user_id = system.id,
			system_id = state.id
		)
		assert data.get('code') == '800.200.001', "should update system recipients"
		assert data2.get(
			'code') == '800.400.001', "Should return an error showing unable to update system recipient"

	def test_delete_system_recipient(self):
		state = mixer.blend('base.State', name = 'Active')
		recipient = mixer.blend('core.User', state = state)
		system = mixer.blend('core.System', state = state)
		system_recipient = mixer.blend('core.SystemRecipient', recipient = recipient)
		data = RecipientAdministrator.delete_system_recipient(system_recipient_id = system_recipient.id)
		data2 = RecipientAdministrator.delete_system_recipient(system_recipient_id = system.id)
		assert data.get('code') == '800.200.001', "should update system recipients"
		assert data2.get(
			'code') == '800.400.002', "Should return an error showing unable to update system recipient"
