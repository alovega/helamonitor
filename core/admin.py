# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from core.models import NotificationType, EscalationLevel, IncidentType, EventType, EndpointType, LogType, \
    PriorityLevel, Occurrence, System, Interface, SystemCredential, Recipient, SystemRecipient, SystemMonitor, \
    Event, EscalationRule, Incident, IncidentEvent, IncidentLog, Notification


@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    """
    Admin for NotificationType model
    """
    list_filter = ('date_created', 'state')
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(EscalationLevel)
class EscalationLevelAdmin(admin.ModelAdmin):
    """
    Admin for EscalationLevel model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(IncidentType)
class IncidentTypeAdmin(admin.ModelAdmin):
    """
    Admin for IncidentType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """
    Admin for EventType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(PriorityLevel)
class PriorityLevelAdmin(admin.ModelAdmin):
    """
    Admin for PriorityLevel model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(PriorityLevel)
class IncidentTypeAdmin(admin.ModelAdmin):
    """
    Admin for IncidentType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(LogType)
class LogTypeAdmin(admin.ModelAdmin):
    """
    Admin for LogType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(EndpointType)
class EndpointTypeAdmin(admin.ModelAdmin):
    """
    Admin for IncidentType model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    """
    Admin for Occurrence model
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'state', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('name', 'description')


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


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    """
    Admin for Endpoint model
    """
    list_filter = ('date_created', 'endpoint_type')
    list_display = ('name', 'description', 'endpoint_type', 'system', 'state')
    ordering = ('-date_created',)
    search_fields = ('name', 'description', 'endpoint_type__name')


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


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin for Event Model
    """
    list_filter = ('date_created',)
    list_display = ('code', 'event_type', 'method', 'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('event_level__name', 'code')


@admin.register(EscalationRule)
class EscalationRuleAdmin(admin.ModelAdmin):
    """
    Admin for EscalationRule model
    """
    list_filter = ('date_created',)
    list_display = ('occurrence_type', 'occurrence_count', 'duration', 'event_type', 'system', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('occurrence_type__name', 'event_type__name', 'system__name')


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
    list_display = ('message', 'notification_type', 'state',  'date_created', 'date_modified')
    ordering = ('-date_created',)
    search_fields = ('message', 'notification_type__name')
