# -*- coding: utf-8 -*-
"""
core Models
"""
from __future__ import unicode_literals

from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from base.models import BaseModel, GenericBaseModel, State, NotificationType, EventType, LogType,\
    IncidentType, EndpointType, EscalationLevel


def versions():
    """
    returns a collection of version choices to chose from
    :return: version choices
    @retype tuple
    """
    return ('1', '1.0.0'),


class System(GenericBaseModel):
    """
    model for managing defined system
    """
    code = models.CharField(max_length = 100, unique=True, db_index=True)
    version = models.CharField(max_length = 5, choices=versions(), default='1')
    admin = models.ForeignKey(User)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name


class Interface(GenericBaseModel):
    """
    model for managing defined system interfaces
    """
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (self.name, self.system, self.state)


class Endpoint(GenericBaseModel):
    endpoint = models.CharField(max_length=100)
    system = models.ForeignKey(System)
    optimal_response_time = models.DurationField(default= timedelta(milliseconds = 3000))
    endpoint_type = models.ForeignKey(EndpointType, help_text='Endpoint type e.g an health-check endpoint')
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name


class SystemCredential(BaseModel):
    """
    model for managing credentials for system users
    """
    username = models.CharField(max_length=100, help_text='Similar to a client_ID')
    password = models.CharField(max_length=100, help_text='Similar to a client_Secret')
    token = models.CharField(max_length=100, help_text='Authorization token')
    expires_at = models.DateTimeField(null=True, blank=True, help_text='Expiry time of the authorization token')
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (
            self.username, self.system, self.state
        )


class SystemMonitor(BaseModel):
    """
    model for managing monitoring for my added system
    """
    response_time = models.DurationField(default=timedelta(), null=True, blank=True)
    endpoint = models.ForeignKey(Endpoint)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (self.endpoint, self.system, self.state)


class Recipient(BaseModel):
    """
    models for managing the recipient of a system
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=100)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s %s %s" % (self.first_name, self.last_name, self.email, self.phone_number, self.state)


class SystemRecipient(BaseModel):
    """
    models for managing recipient and a system
    """
    recipient = models.ForeignKey(Recipient)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)
    escalation_level = models.ForeignKey(EscalationLevel)

    def __str__(self):
        return "%s %s %s" % (self.recipient, self.system, self.state)


class Event(BaseModel):
    """
    Model for managing events
    """
    description = models.CharField(max_length=100, help_text="Informative description of the event", null=True,
                                   blank=True)
    interface = models.ForeignKey(Interface, null=True, blank=True)
    system = models.ForeignKey(System)
    event_type = models.ForeignKey(EventType)
    state = models.ForeignKey(State)
    method = models.CharField(max_length=100, null=True, help_text="Method where the error is origination from")
    response = models.TextField(max_length=255, null=True, blank=True)
    request = models.TextField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    response_time = models.DurationField(default=timedelta(), null=True, blank=True)

    def __str__(self):
        return "%s %s %s" % (
            self.event_type, self.description, self.state
        )


class EscalationRule(GenericBaseModel):
    """
    Manages Escalation rules to be applied on events to determine whether they should be escalated or not
    """
    nth_event = models.IntegerField(default=1, help_text="Limit of n events to satisfy this rule")
    duration = models.DurationField(
        help_text="Time period within which the nth occurrence of an event type will be escalated", null=True,
        blank = True
    )
    event_type = models.ForeignKey(EventType)
    escalation_level = models.ForeignKey(EscalationLevel)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name


class Incident(GenericBaseModel):
    """
    Manages Incidents created from escalation points
    """
    incident_type = models.ForeignKey(IncidentType)
    priority_level = models.IntegerField(default = 1)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name


class IncidentEvent(BaseModel):
    """
    Represents a ManyToMany association between incidents and events
    """
    incident = models.ForeignKey(Incident)
    event = models.ForeignKey(Event)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s" % (self.incident, self.event)


class IncidentLog(BaseModel):
    """
    Manages logs of incidences and keeps track of resolution history
    """
    description = models.TextField(max_length=255, blank=True, null=True)
    incident = models.ForeignKey(Incident)
    log_type = models.ForeignKey(LogType, null = True)
    user = models.ForeignKey(User, null=True, blank=True)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (
            self.state, self.incident, self.user
        )


class Notification(BaseModel):
    """
    Manages logs of notifications sent out to recipients based on incidents
    """
    message = models.TextField(max_length=255)
    notification_type = models.ForeignKey(NotificationType)
    incident = models.ForeignKey(Incident, null=True)
    recipient = models.ForeignKey(Recipient)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (self.message, self.notification_type, self.recipient)
