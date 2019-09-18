# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel, State


def token_expiry():
    """
    Calculates token expiry time from the current time and extends it with the configured expiry time
    @return: Time at which the token will expire
    @rtype: datetime
    """
    return timezone.now() + timedelta(minutes = settings.EXPIRY_SETTINGS)


class Oauth(BaseModel):
    """
    Manages authentication tokens for configured apps and users
    """
    app = models.ForeignKey(App)
    token = models.CharField(max_length = 255)
    user = models.ForeignKey(User)
    expires_at = models.DateTimeField(default = token_expiry)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s %s" % (self.app.name, self.user.username, self.token, self.state)
