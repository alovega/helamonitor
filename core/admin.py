# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from core.models import State, NotificationType, EscalationLevel, IncidentType, System, Interface, \
    SystemCredential, Recipient, SystemRecipient, SystemMonitor, Event, Incident, IncidentEvent, \
    IncidentLog, Notification


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    """
    Model Admin for State model
    """
    list_filter = ("date_created",)
    list_display = ('name', 'description', 'date_created', 'date_modified',)
    search_fields = ('name',)
    ordering = ('-date_created',)


@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    """
    Admin for NotificationType model
    """
    list_filter = ('date_created', 'state')
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name',)


@admin.register(EscalationLevel)
class EscalationLevelAdmin(admin.ModelAdmin):
    """
    Admin for EscalationLevel model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name',)


@admin.register(IncidentType)
class IncidentTypeAdmin(admin.ModelAdmin):
    """
    Admin for IncidentType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin for Event Model
    """
    list_filter = ('date_created',)
    list_display = ('code', 'escalation_level', 'method', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('escalation_level__name', 'code')


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    """
    Admin for Incident Model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'incident_type', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name', 'incident_type__name')


@admin.register(IncidentLog)
class IncidentLogAdmin(admin.ModelAdmin):
    """
    Admin for IncidentLog Model
    """
    list_filter = ('date_created', )
    list_display = ('incident', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('incident__name', )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin for Notification Model
    """
    list_filter = ('date_created',)
    list_display = ('message', 'notification_type', 'state', 'incident',  'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('notification_type', 'incident__name')


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
    list_display = ('first_name', 'last_name', 'email', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('first_name', 'last_name')


@admin.register(SystemRecipient)
class SystemRecipient(admin.ModelAdmin):
    """
    Admin for System recipient model
    """
    list_filter = ('date_created',)
    list_display = ('recipient', 'system', 'state')
    ordering = ('-date_created',)
    search_fields = ('system',)


@admin.register(IncidentEvent)
class IncidentEvent(admin.ModelAdmin):
    """
    Admin for IncidentEvent model
    """
    list_filter = ('date_created',)
    list_display = ('incident', 'event', 'state')
    ordering = ('-date_created',)
    search_fields = ('incident', 'event')