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


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin for Event Model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description')