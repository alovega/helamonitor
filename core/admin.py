# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from core.models import State, NotificationType, EscalationLevel, IncidentType
from core.models import System, Interface, SystemCredential, Recipient, SystemRecipient, SystemMonitor

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    """
    Model Admin for State model
    """
    list_filter = ("date_created",)
    list_display = ('name', 'description', 'date_created', 'date_modified',)
    search_fields = ('name',)


@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    """
    Admin for NotificationType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name',)


@admin.register(EscalationLevel)
class EscalationLevelAdmin(admin.ModelAdmin):
    """
    Admin for EscalationLevel model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name',)


@admin.register(IncidentType)
class IncidentTypeAdmin(admin.ModelAdmin):
    """
    Admin for IncidentType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name',)


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    """
    Admin for System model
    """
    list_filter = ('date_created', )
    list_display = ('name', 'description', 'health_check_endpoint', 'credential_endpoint', 'date_created',
                    'state')
    ordering = ('-date_created',)
    search_fields = ('name',)


@admin.register(SystemCredential)
class SystemCredentialAdmin(admin.ModelAdmin):
    """
    Admin for System credential model
    """
    list_filter = ('date_created', )
    list_display = ('username', 'system', 'state')
    ordering = ('-date_created',)
    search_fields = ('username', 'system')


@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    """
    Admin for Interface model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'system', 'state')
    ordering = ('-date_created',)
    search_fields = ('name', 'system')


@admin.register(SystemMonitor)
class SystemMonitorAdmin(admin.ModelAdmin):
    """
    Admin for System monitor model
    """
    list_filter = ('date_created',)
    list_display = ('system', 'state', 'response_time')
    ordering = ('-date_created',)


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    """
    Admin for Recipient Model
    """
    list_filter = ('date_created', )
    list_display = ('first_name', 'last_name', 'email', 'system', 'state')
    ordering = ('-date_created',)
    search_fields = ('last_name', 'email')


@admin.register(SystemRecipient)
class SystemRecipient(admin.ModelAdmin):
    """
    Admin for System recipient model
    """
    list_filter = ('date_created',)
    list_display = ('recipient', 'system', 'state')
    ordering = ('-date_created',)
    search_fields = ('system',)