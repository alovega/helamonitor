# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api.models import App, ApiUser

# Register your models here.


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
	"""
	Admin for App model
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'state', 'date_modified', 'date_created')
	ordering = ('-date_created',)
	search_fields = ('id', 'name')


@admin.register(ApiUser)
class ApiUserAdmin(admin.ModelAdmin):
	"""
	Admin for ApiUser Model
	"""
	list_filter = ('date_created',)
	list_display = ('user', 'app_id', 'state', 'date_modified', 'date_created')
	ordering = ('-date_created',)
	search_fields = ('user__name', 'app_id')
