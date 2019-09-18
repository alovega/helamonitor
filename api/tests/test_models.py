# -*- coding: utf-8 -*-
"""
Tests for Api models
"""
import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestApiModels(object):
	"""Test class for Api models"""
	def test_oauth(self):
		oauth = mixer.blend('core.Oauth')
		assert oauth is not None, 'Should create an oauth object'
		assert type(str(oauth)) == str, 'Oauth should be a str object'
