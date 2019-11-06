# -*- coding: utf-8 -*-
"""
api models
"""
from __future__ import unicode_literals

from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from core.models import System
from base.models import BaseModel, GenericBaseModel, State


def token_expiry():
    """
    Calculates token expiry time from the current time and extends it with the configured expiry time
    @return: Time at which the token will expire
    @rtype: datetime
    """
    return timezone.now() + timedelta(minutes = settings.EXPIRY_SETTINGS)


class App(GenericBaseModel):
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name


class AppUser(BaseModel):
    user = models.ForeignKey(User)
    app = models.ForeignKey(App)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.user


class Oauth(BaseModel):
    """
    Manages access tokens for configured apps and users
    """
    app_user = models.ForeignKey(AppUser)
    token = models.CharField(max_length = 255)
    expires_at = models.DateTimeField(default = token_expiry)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s %s" % (self.app_user.app.name, self.app_user.user.username, self.token, self.state)
