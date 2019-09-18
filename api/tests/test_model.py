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
		event = mixer.blend("api.App")
		assert event is not None, "Should create an app model"
		assert type(str(event)) == str, "app Should be a str object"

	def test_incident(self):
		incident = mixer.blend("api.ApiUser")
		assert incident is not None, "Should create an ApiUser"
		assert type(str(incident)) == str, "ApiUser Should be a str object"
