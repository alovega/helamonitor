# -*- coding: utf-8 -*-
"""
api models
"""
from __future__ import unicode_literals

from django.db import models
import uuid
from django.contrib.auth.models import User
from base.models import BaseModel, GenericBaseModel, State


class App(GenericBaseModel):
	id = models.UUIDField(max_length = 100, default = uuid.uuid4, unique = True, editable = False, primary_key = True)
	state = models.ForeignKey(State)


class ApiUser(BaseModel):
	user = models.ForeignKey(User)
	app_id = models.ForeignKey(App)
	password = models.CharField(max_length = 100)
	state = models.ForeignKey(State)
