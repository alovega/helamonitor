# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from core.models import State, NotificationType, EscalationLevel, IncidentType, Event, Incident, IncidentEvent,\
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
