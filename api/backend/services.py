# -*- coding: utf-8 -*-
"""
Services for Api module
"""
from base.backend.services import ServiceBase
from api.models import Oauth


class OauthService(ServiceBase):
    """
    Class for Oauth CRUD
    """
    manager = Oauth.objects


from api.models import AppUser, App


class AppService(ServiceBase):
    """
    Class for App CRUD
    """
    manager = App.objects


class AppUserService(ServiceBase):
    """
    Class for ApiUser CRUD
    """
    manager = AppUser.objects

