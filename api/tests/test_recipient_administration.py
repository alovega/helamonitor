import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User

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

	# def test_update_recipient(self):
	# 	state = mixer.blend('base.State', name = 'Active')
	# 	state2 = mixer.blend('base.State', name = 'Disabled')
	# 	notification_type = mixer.blend('base.NotificationType', state = state, name = 'Sms')
	# 	notification_type2 = mixer.blend('base.NotificationType', state = state, name = 'Email')
	# 	user = mixer.blend(User, name="kevin")
	# 	escalation_level = mixer.blend('base.EscalationLevel', state = state, name = "Level 1")
	# 	recipient = mixer.blend('core.Recipient', state = state, notification_type=notification_type, user=user)
	# 	system_recipient = mixer.blend('core.SystemRecipient', state=state, recipient=recipient,
	# 	                               escalation_level=escalation_level)
	# 	recipient_update = RecipientAdministrator.update_recipient(
	# 		recipient_id = recipient.id, state_id = state2.id, system_recipient_id = system_recipient.id,
	# 		last_name="kevin", first_name = "Alwa", email = "sampleMail@gmail.com", phone_number = 'phone_number',
	# 		notification_type_id = notification_type2.id
	# 	)
	# 	recipient_update2 = RecipientAdministrator.update_recipient(
	# 		recipient_id = recipient.id, state_id = state2.id, system_recipient_id = system_recipient.id,
	# 		last_name = "kevin", first_name = "", email = "sampleMail@gmail.com", phone_number = 'phone_number',
	# 		notification_type_id = notification_type2.id
	# 	)
	# 	assert recipient_update.get('code') == '800.200.001'
	# 	assert recipient_update2.get('code') == '800.400.002'
	#
	# def test_get_system_recipients(self):
	# 	state = mixer.blend('base.State', name = 'Active')
	# 	escalation_level = mixer.blend('base.EscalationLevel', state = state, name = "Level 1")
	# 	recipient = mixer.blend('core.Recipient', state = state)
	# 	recipient2 = mixer.blend('core.Recipient', state = state)
	# 	system1 = mixer.blend('core.System', state = state)
	# 	system2 = mixer.blend('core.System', state = state)
	# 	system_recipients1 = mixer.cycle(4).blend('core.SystemRecipient', state=state, system=system1,
	# 	                                          recipient=recipient, escalation_level=escalation_level)
	# 	system_recipients2 = mixer.cycle(5).blend('core.SystemRecipient', state=state, system=system2,
	# 	                                          recipient=recipient2, escalation_level=escalation_level)
	# 	recipient1 = RecipientAdministrator.get_system_recipients(
	# 		system_id = system1.id, escalation_level_id = escalation_level.id
	# 	)
	# 	recipient3 = RecipientAdministrator.get_system_recipients(
	# 		system_id = system2, escalation_level_id = escalation_level
	# 	)
	#
	# 	assert recipient1.get('code') == '800.200.001', "should get system endpoints"
	# 	assert recipient3.get('code') == '800.400.002'
	#
	# def test_get_system_recipient(self):
	# 	state = mixer.blend('base.State', name = 'Active')
	# 	escalation_level = mixer.blend('base.EscalationLevel', state = state, name = "Level 1")
	# 	recipient = mixer.blend('core.Recipient', state = state)
	# 	recipient2 = mixer.blend('core.Recipient', state = state)
	# 	system1 = mixer.blend('core.System', state = state)
	# 	system2 = mixer.blend('core.System', state = state)
	# 	system_recipients1 = mixer.cycle(4).blend('core.SystemRecipient', state=state, system=system1,
	# 	                                          recipient=recipient, escalation_level=escalation_level)
	# 	system_recipients2 = mixer.cycle(5).blend('core.SystemRecipient', state=state, system=system2,
	# 	                                          recipient=recipient2, escalation_level=escalation_level)
	# 	recipient1 = RecipientAdministrator.get_system_recipient(
	# 		system_id = system1.id,
	# 		recipient_id = recipient.id, escalation_level_id = escalation_level.id
	# 	)
	# 	recipient3 = RecipientAdministrator.get_system_recipient(
	# 		recipient_id = system1.id, escalation_level_id = escalation_level, system_id = system1.id
	# 	 )
	#
	# 	assert recipient1.get('code') == '800.200.001', "should get system endpoints"
	# 	assert recipient3.get('code') == '800.400.002'
