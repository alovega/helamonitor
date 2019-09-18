# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from api.models import Oauth


@admin.register(Oauth)
class OauthAdmin(admin.ModelAdmin):
	"""
	Admin for oauth model
	"""
	list_filter = ('-date_created',)
	list_display = ('token', 'expires_at', 'state', 'date_modified', 'date_created')
	ordering = ('-date_created',)
	search_fields = ('app_user__app__name', )
