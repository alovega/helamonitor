# -*- coding: utf-8 -*-
"""
This is the Api services tests module.
"""
import datetime
import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from api.backend.services import OauthService, AppUserService, AppService

pytestmark = pytest.mark.django_db


class TestOauthService(object):
    """Tests for the Oauth model services"""

    def test_get(self):
        """
        Test Oauth get service
        """
        mixer.blend('api.Oauth', token = "12345")
        oauth = OauthService().get(token = "12345")
        assert oauth is not None, 'Should have an oauth object'

    def test_filter(self):
        """
        Test Oauth filter service
        """
        mixer.cycle(3).blend('api.oauth')
        oauths = OauthService().filter()
        assert len(oauths) == 3, 'Should have 3 Oauth objects'

    def test_create(self):
        """
        Test Oauth create service
        """
        app_user = mixer.blend('api.AppUser')
        oauth = OauthService().create(token = "12345", app_user = app_user, state = mixer.blend('base.State'))
        assert oauth is not None, 'Should have an Oauth object'
        assert oauth.token == "12345", "Created Oauth token is equals to 12345"

    def test_update(self):
        """
        Test Oauth update service
        """
        oauth = mixer.blend('api.Oauth')
        oauth = OauthService().update(oauth.id, token = "12345")
        assert oauth.token == "12345", 'Should have the same token'


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
        system = mixer.blend('core.System')
        app = AppService().create(name="Helaplan", state=state, system=system)
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
        mixer.blend('api.AppUser', app=app, user=user)
        app_user = AppUserService().get(app_id__name="Helaplan")
        assert app_user is not None, 'Should have an app object'

    def test_filter(self):
        """
        Test System filter service
        """
        mixer.cycle(3).blend('api.AppUser')
        app_user = AppUserService().filter()
        assert len(app_user) == 3, 'Should have 3 app objects'

    def test_create(self):
        """
        Test System create service
        """
        state = mixer.blend('base.State')
        app = mixer.blend('api.App', name = "Helaplan")
        user = mixer.blend(User, name = "Kevin")
        app_user = AppUserService().create(app=app, state=state, user=user)
        assert app_user is not None, 'Should have a System object'
        assert app_user.user.name == "Kevin", "Created App name is equals to Helaplan"

    def test_update(self):
        """
        Test System update service
        """
        app = mixer.blend('api.App', name = "Helaplan")
        app_user = mixer.blend('api.AppUser')
        app_user = AppUserService().update(app_user.id, app = app)
        assert app_user.app.name == "Helaplan", 'Should have the same name'
