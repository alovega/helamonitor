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


