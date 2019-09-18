# -*- coding: utf-8 -*-
"""
This is the Api services tests module.
"""
import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User

from api.backend.services import ApiUserService, AppService

pytestmark = pytest.mark.django_db


class TestAppService(object):
    """
    Test the App Model Services
    """

    def test_get(self):
        """
        Test System get service
        """
        mixer.blend('api.App', name="Helaplan")
        app = AppService().get(name="Helaplan")
        assert app is not None, 'Should have an app object'

    def test_filter(self):
        """
        Test System filter service
        """
        mixer.cycle(3).blend('api.App')
        app = AppService().filter()
        assert len(app) == 3, 'Should have 3 app objects'

    def test_create(self):
        """
        Test System create service
        """
        state = mixer.blend('base.State')
        app = AppService().create(name="Helaplan", state=state)
        assert app is not None, 'Should have a System object'
        assert app.name == "Helaplan", "Created App name is equals to Helaplan"

    def test_update(self):
        """
        Test System update service
        """
        app = mixer.blend('api.App')
        app = AppService().update(app.id, name = "Helaplan")
        assert app.name == "Helaplan", 'Should have the same name'


class TestApiUserService(object):
    """
    Test the App Model Services
    """

    def test_get(self):
        """
        Test System get service
        """
        app = mixer.blend('api.App', name="Helaplan")
        user = mixer.blend(User, name="Kevin")
        mixer.blend('api.ApiUser', app_id=app, user=user)
        app = ApiUserService().get(app_id__name="Helaplan")
        assert app is not None, 'Should have an app object'

    def test_filter(self):
        """
        Test System filter service
        """
        mixer.cycle(3).blend('api.ApiUser')
        api_user = ApiUserService().filter()
        assert len(api_user) == 3, 'Should have 3 app objects'

    def test_create(self):
        """
        Test System create service
        """
        state = mixer.blend('base.State')
        app = mixer.blend('api.App', name = "Helaplan")
        user = mixer.blend(User, name = "Kevin")
        app = ApiUserService().create(app_id=app, state=state)
        assert app is not None, 'Should have a System object'
        assert app.name == "Helaplan", "Created App name is equals to Helaplan"

    def test_update(self):
        """
        Test System update service
        """
        app = mixer.blend('api.App')
        app = AppService().update(app.id, name = "Helaplan")
        assert app.name == "Helaplan", 'Should have the same name'
