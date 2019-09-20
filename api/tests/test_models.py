# -*- coding: utf-8 -*-
"""
Tests for Api models
"""
import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestAppModels(object):
	"""
	Test class for api models
	"""
	def test_app(self):
		"""Tests from app model"""
		app = mixer.blend("api.App")
		assert app is not None, "Should create an app model"
		assert type(str(app)) == str, "app Should be a str object"

	def test_app_user(self):
		"""Tests for app_user model"""
		app_user = mixer.blend("api.AppUser")
		assert app_user is not None, "Should create an ApiUser"
		assert type(str(app_user)) == str, "ApiUser Should be a str object"

	def test_oauth(self):
		"""Tests for oauth model"""
		oauth = mixer.blend('api.Oauth')
		assert oauth is not None, 'Should create an oauth object'
		assert type(str(oauth)) == str, 'Oauth should be a str object'
