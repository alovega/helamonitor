# coding=utf-8
"""
Tests for models in core module
"""

import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestBaseModels(object):
    """
    Test class for core models
    """
    def test_state(self):
        state = mixer.blend("base.State")
        assert state is not None, "Should create a State model"
        assert type(str(state)) == str, "State should be a str object"








