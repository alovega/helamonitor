# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api.models import App, AppUser, Oauth


@admin.register(Oauth)
class OauthAdmin(admin.ModelAdmin):
	"""
	Admin for Oauth model
	"""
	list_filter = ('date_created',)
	list_display = ('token', 'expires_at', 'state', 'date_modified', 'date_created')
	ordering = ('-date_created',)
	search_fields = ('app_user__app__name', )


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
	"""
	Admin for App model
	"""
	list_filter = ('date_created',)
	list_display = ('id','name', 'state', 'date_modified', 'date_created')
	ordering = ('-date_created',)
	search_fields = ('name',)


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
	"""
	Admin for ApiUser Model
	"""
	list_filter = ('date_created',)
	list_display = ('user', 'app', 'state', 'date_modified', 'date_created')
	ordering = ('-date_created',)
	search_fields = ('user__username', 'app__name')
