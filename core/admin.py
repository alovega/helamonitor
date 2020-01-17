# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User, System, Interface, SystemCredential, Recipient, SystemRecipient, SystemMonitor, \
    Event, EscalationRule, Incident, IncidentEvent, IncidentLog, Notification, Endpoint


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin for User model"""
    admin_fieldsets = list(UserAdmin.fieldsets)
    admin_fieldsets[1] = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')})
    )
    admin_fieldsets = tuple(admin_fieldsets)
    fieldsets = admin_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'phone_number', 'first_name', 'last_name'),
        }),
    )


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    """
    Admin for System model
    """
    list_filter = ('date_created', )
    list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name',)


@admin.register(SystemCredential)
class SystemCredentialAdmin(admin.ModelAdmin):
    """
    Admin for System credential model
    """
    list_filter = ('date_created', )
    list_display = ('username', 'system', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('username', 'system__name')


@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    """
    Admin for Interface model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'system', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name', 'system__name')


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    """
    Admin for Endpoint model
    """
    list_filter = ('date_created', 'endpoint_type')
    list_display = ('name', 'description', 'endpoint_type', 'system', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name', 'description', 'endpoint_type__name')


@admin.register(SystemMonitor)
class SystemMonitorAdmin(admin.ModelAdmin):
    """
    Admin for System monitor model
    """
    list_filter = ('date_created',)
    list_display = ('system', 'endpoint', 'state', 'response_time', 'date_modified', 'date_created')
    ordering = ('-date_created',)


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    """
    Admin for Recipient Model
    """
    list_filter = ('date_created', )
    list_display = (
        'user', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('first_name', 'last_name')


@admin.register(SystemRecipient)
class SystemRecipient(admin.ModelAdmin):
    """
    Admin for System recipient model
    """
    list_filter = ('date_created',)
    list_display = ('recipient', 'system', 'state', 'escalation_level', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('system__name',)


@admin.register(IncidentEvent)
class IncidentEvent(admin.ModelAdmin):
    """
    Admin for IncidentEvent model
    """
    list_filter = ('date_created',)
    list_display = ('incident', 'event', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('incident__name', 'event__name')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin for Event Model
    """
    list_filter = ('date_created',)
    list_display = ('code', 'event_type', 'method', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('event_level__name', 'code')


@admin.register(EscalationRule)
class EscalationRuleAdmin(admin.ModelAdmin):
    """
    Admin for EscalationRule model
    """
    list_filter = ('date_created',)
    list_display = (
        'name', 'nth_event', 'duration', 'event_type', 'system', 'date_modified', 'date_created'
    )
    ordering = ('-date_created',)
    search_fields = ('name', 'nth_event', 'event_type__name', 'system__name')


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    """
    Admin for Incident Model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'incident_type', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('name', 'incident_type__name')


@admin.register(IncidentLog)
class IncidentLogAdmin(admin.ModelAdmin):
    """
    Admin for IncidentLog Model
    """
    list_filter = ('date_created', )
    list_display = ('incident', 'description', 'state', 'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('incident__name', 'description')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin for Notification Model
    """
    list_filter = ('date_created', 'state__name')
    list_display = ('message', 'notification_type', 'state',  'date_modified', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('message', 'notification_type__name')
