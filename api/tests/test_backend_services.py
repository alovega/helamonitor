# -*- coding: utf-8 -*-
"""
This is the Api services tests module.
"""
import datetime
import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User

# noinspection SpellCheckingInspection
from core.backend.services import SystemService, InterfaceService, SystemCredentialService, \
	RecipientService, SystemRecipientService, SystemMonitorService, EventService, IncidentService, \
	IncidentEventService, IncidentLogService, EndpointService, EscalationRuleService
from api.backend.services import OauthService

pytestmark = pytest.mark.django_db


class TestOauthService(object):
	"""Tests for the Oauth model services"""

	def test_get(self):
		"""
		Test Oauth get service
		"""
		mixer.blend('core.Oauth', token = "12345")
		oauth = OauthService().get(token = "12345")
		assert oauth is not None, 'Should have an oauth object'

	def test_filter(self):
		"""
		Test Oauth filter service
		"""
		mixer.cycle(3).blend('core.oauth')
		oauths = OauthService().filter()
		assert len(oauths) == 3, 'Should have 3 Oauth objects'

	def test_create(self):
		"""
		Test Oauth create service
		"""
		oauth = OauthService().create(token = "12345")
		assert oauth is not None, 'Should have an Oauth object'
		assert oauth.token == "12345", "Created Oauth token is equals to 12345"

	def test_update(self):
		"""
		Test Oauth update service
		"""
		oauth = mixer.blend('core.Oauth')
		oauth = OauthService().update(oauth.id, token = "12345")
		assert oauth.token == "12345", 'Should have the same token'

