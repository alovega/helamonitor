# -*- coding: utf-8 -*-
"""
api models
"""
from __future__ import unicode_literals

from django.db import models
from base.models import BaseModel, GenericBaseModel, State
from core.models import System


class App(GenericBaseModel):
	system = models.ForeignKey(System)
	state = models.ForeignKey(State)

	def __str__(self):
		return "%s" % self.name


class AppUser(BaseModel):
	username = models.CharField(max_length = 240)
	password = models.CharField(max_length = 240)
	app = models.ForeignKey(App, unique = True)
	state = models.ForeignKey(State)

	def __str__(self):
		return "%s" % self.username
