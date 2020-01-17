import pytest
from mixer.backend.django import mixer

from api.backend.interfaces.recipient_administration import RecipientAdministrator

pytestmark = pytest.mark.django_db


class TestRecipientAdministration(object):
	"""
	class for testing recipient Administration
	"""

	def test_create_recipient(self):
		user = mixer.blend('core.User')
		state = mixer.blend('base.State', name = 'Active')
		recipient = RecipientAdministrator.create_recipient(
			phone_number = '07XXXXXXX', state_id = state.id, user_id = user.id
		)
		recipient_2 = RecipientAdministrator.create_recipient(
			phone_number = '07XXXXXXX', state_id = '', user_id = user.id
		)
		recipient_3 = RecipientAdministrator.create_recipient(
			phone_number = '07XXXXXXX', state_id = state.id, user_id = 5
		)
		assert recipient.get('code') == '800.200.001', "successfully created a recipient"
		assert recipient_2.get('code') == '800.400.002', "Error indicating a recipient with that record exists"
		assert recipient_3.get('code') == '800.400.001', "Error while creating recipient"

	def test_update_recipient(self):
		state = mixer.blend('base.State', name = 'Active')
		state2 = mixer.blend('base.State', name = 'Disabled')
		user = mixer.blend('core.User', name="kevin", email="alovega@gmail.com")
		recipient = mixer.blend('core.Recipient', state = state, user=user)
		recipient_update = RecipientAdministrator.update_recipient(
			recipient_id = recipient.id, state_id = state2.id, phone_number = "74991010xxx"
		)
		recipient_update2 = RecipientAdministrator.update_recipient(
			recipient_id = recipient.id, state_id = state2.id, phone_number = ""
		)
		assert recipient_update.get('code') == '800.200.001'
		assert recipient_update2.get('code') == '800.400.002'

	def test_get_recipient(self):
		user = mixer.blend('core.User')
		state = mixer.blend('base.State', name = 'Active')
		recipient = mixer.blend('core.Recipient', state = state, user = user)
		data = RecipientAdministrator.get_recipient(recipient_id = recipient.id)
		assert data.get('code') == '800.200.001'

	def test_delete_recipient(self):
		user = mixer.blend('core.User')
		state = mixer.blend('base.State', name = 'Active')
		recipient = mixer.blend('core.Recipient', state = state, user = user)
		data = RecipientAdministrator.delete_recipient(recipient_id=recipient.id)
		data2 = RecipientAdministrator.delete_recipient(recipient_id = '')
		assert data.get('code') == '800.200.001'
		assert data2.get('code') == '800.400.002'

	def test_create_system_recipients(self):
		state = mixer.blend('base.State', name = 'Active')
		escalation_level = mixer.blend('base.EscalationLevel', state = state)
		recipient = mixer.blend('core.Recipient', state = state)
		notification = mixer.blend('core.Notification', state=state)
		system = mixer.blend('core.System', state = state)
		data = RecipientAdministrator.create_system_recipient(
			system_id = system.id,
			escalations = [{"NotificationType": notification.id, "EscalationLevel": escalation_level.id}],
			recipient_id = recipient.id
		)
		data2 = RecipientAdministrator.create_system_recipient(
			system_id = system.id,
			escalations = [{"NotificationType": notification.id, "EscalationLevel": escalation_level.id}],
			recipient_id = recipient.id
		)
		assert data.get('code') == '800.200.001', "should create system recipients"
		assert data2.get('code') == '800.400.002', "Should return Error indicating unable to create system recipient "

	def test_update_system_recipients(self):
		state = mixer.blend('base.State', name = 'Active')
		escalation_level = mixer.blend('base.EscalationLevel', state = state)
		recipient = mixer.blend('core.Recipient', state = state)
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
		assert data2.get('code') == '800.400.002', "Should return an error showing unable to update system recipient"

	def test_get_system_recipients(self):
		state = mixer.blend('base.State', name = 'Active')
		recipient = mixer.blend('core.Recipient', state = state)
		system = mixer.blend('core.System', state = state)
		system_recipient = mixer.blend('core.SystemRecipient', recipient = recipient)
		data = RecipientAdministrator.get_system_recipient(
			recipient_id = recipient.id, system_id = system.id
		)
		data2 = RecipientAdministrator.get_system_recipient(
			recipient_id = system.id,
			system_id = state.id
		)
		assert data.get('code') == '800.200.001', "should update system recipients"
		assert data2.get(
			'code') == '800.400.002', "Should return an error showing unable to update system recipient"

	def test_delete_system_recipient(self):
		state = mixer.blend('base.State', name = 'Active')
		recipient = mixer.blend('core.Recipient', state = state)
		system = mixer.blend('core.System', state = state)
		system_recipient = mixer.blend('core.SystemRecipient', recipient = recipient)
		data = RecipientAdministrator.delete_system_recipient(system_recipient_id = system_recipient.id)
		data2 = RecipientAdministrator.delete_system_recipient(system_recipient_id = system.id)
		assert data.get('code') == '800.200.001', "should update system recipients"
		assert data2.get(
			'code') == '800.400.002', "Should return an error showing unable to update system recipient"
