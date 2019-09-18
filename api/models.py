# -*- coding: utf-8 -*-
"""
api models
"""
from __future__ import unicode_literals

from django.db import models
import uuid
from django.contrib.auth.models import User
from base.models import BaseModel, GenericBaseModel, State
from core.models import System


class App(GenericBaseModel):
	id = models.ForeignKey(System)
	state = models.ForeignKey(State)

	def __str__(self):
		return "%s %s" % (self.name, self.state)


class ApiUser(BaseModel):
	username = models.ForeignKey(User)
	app_id = models.ForeignKey(App)
	password = models.CharField(max_length = 100)
	state = models.ForeignKey(State)
