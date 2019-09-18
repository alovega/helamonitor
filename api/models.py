# -*- coding: utf-8 -*-
"""
api models
"""
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from base.models import BaseModel, GenericBaseModel, State
from core.models import System


class App(GenericBaseModel):
	system = models.ForeignKey(System)
	state = models.ForeignKey(State)

	def __str__(self):
		return "%s" % self.name


class AppUser(BaseModel):
	user = models.ForeignKey(User)
	app = models.OneToOneField(App)
	state = models.ForeignKey(State)

	def __str__(self):
		return "%s" % self.user
