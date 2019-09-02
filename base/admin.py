# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from base.models import State, EndpointType, NotificationType, IncidentType, EventType, PriorityLevel, LogType, \
    Occurrence, EscalationLevel


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    """
    Model Admin for State model
    """
    list_filter = ("date_created",)
    list_display = ('name', 'description', 'date_modified', 'date_created',)
    search_fields = ('name',)
    ordering = ('-date_created',)


@admin.register(EndpointType)
class EndpointTypeAdmin(admin.ModelAdmin):
    """
    Admin for IncidentType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')

@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    """
    Admin for NotificationType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(EscalationLevel)
class EscalationLevelAdmin(admin.ModelAdmin):
    """
    Admin for EscalationLevel model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(IncidentType)
class IncidentTypeAdmin(admin.ModelAdmin):
    """
    Admin for IncidentType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """
    Admin for EventType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(PriorityLevel)
class PriorityLevelAdmin(admin.ModelAdmin):
    """
    Admin for PriorityLevel model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(LogType)
class LogTypeAdmin(admin.ModelAdmin):
    """
    Admin for LogType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    """
    Admin for Occurrence model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')

