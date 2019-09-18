# coding=utf-8
"""
Tests for models in api module
"""

import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestAppModels(object):
	"""
	Test class for api models
	"""

	def test_app(self):
		app = mixer.blend("api.App")
		assert app is not None, "Should create an app model"
		assert type(str(app)) == str, "app Should be a str object"

	def test_app_user(self):
		app_user = mixer.blend("api.AppUser")
		assert app_user is not None, "Should create an ApiUser"
		assert type(str(app_user)) == str, "ApiUser Should be a str object"
