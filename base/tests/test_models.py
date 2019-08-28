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

    def test_base_model(self):
        base_model = mixer.blend("base.BaseModel")
        assert base_model is not None, "Should create a Base model"
        assert type(str(base_model)) == str, "base should be a str object"

    def test_generic_base_model(self):
        generic_model = mixer.blend("Base.GenericBaseModel")
        assert generic_model is not None, "Should create a GenericBaseModel model"
        assert type(str(generic_model)) == str, "generic_model should be a str object"







