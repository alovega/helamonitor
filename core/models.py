# -*- coding: utf-8 -*-
"""
core Models
"""
from __future__ import unicode_literals

from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from base.models import BaseModel, GenericBaseModel, State, NotificationType, EventType, \
    IncidentType, EndpointType, EscalationLevel


def response_time_speed():
    """
    returns a collection of response time state to chose from
    @return: response_time states
    @retype tuple
    """
    return ('Slow', 'Slow'), ('Normal', 'Normal'),


class System(GenericBaseModel):
    """
    Model for managing defined system
    """
    version = models.CharField(max_length = 10, default='1.0.0')
    admin = models.ForeignKey(User)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name


class Interface(GenericBaseModel):
    """
    Model for managing defined system interfaces
    """
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (self.name, self.system, self.state)


class Endpoint(GenericBaseModel):
    """
    Model for managing endpoint of a system
    """
    system = models.ForeignKey(System)
    endpoint_type = models.ForeignKey(EndpointType, help_text='Endpoint type e.g an health-check endpoint')
    url = models.CharField(max_length=250)
    optimal_response_time = models.DurationField(default= timedelta(milliseconds = 3000))
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name


class SystemCredential(BaseModel):
    """
    Model for managing credentials for system users
    """
    system = models.ForeignKey(System)
    username = models.CharField(max_length=100, help_text='Similar to a client_ID')
    password = models.CharField(max_length=100, help_text='Similar to a client_Secret')
    token = models.CharField(max_length=100, help_text='Authorization token')
    expires_at = models.DateTimeField(null=True, blank=True, help_text='Expiry time of the authorization token')
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (
            self.username, self.system, self.state
        )


class SystemMonitor(BaseModel):
    """
    Model for managing monitoring of a system
    """
    response_time = models.DurationField(default=timedelta(), null = True, blank = True)
    endpoint = models.ForeignKey(Endpoint)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)
    response_time_speed = models.CharField(max_length = 20, choices=response_time_speed(), default='Normal',
                                           null = True, blank = True)
    response = models.CharField(max_length=100, help_text='response returned when calling an endpoint')

    def __str__(self):
        return "%s %s %s %s" % (self.endpoint, self.system, self.state, self.response_time_speed)


class Recipient(BaseModel):
    """
    Model for managing the recipient of a system
    """
    user = models.ForeignKey(User)
    phone_number = models.CharField(max_length=100)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.user


class SystemRecipient(BaseModel):
    """
    Model for managing recipient and a system
    """
    system = models.ForeignKey(System)
    recipient = models.ForeignKey(Recipient)
    escalation_level = models.ForeignKey(EscalationLevel)
    notification_type = models.ForeignKey(NotificationType)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (self.recipient, self.system, self.state)


class Event(BaseModel):
    """
    Model for managing events
    """
    system = models.ForeignKey(System)
    event_type = models.ForeignKey(EventType)
    interface = models.ForeignKey(Interface, null=True, blank=True)
    method = models.CharField(max_length=100, null=True, help_text="Method where the error is origination from")
    request = models.TextField(max_length=1000, null=True, blank=True)
    response = models.TextField(max_length=1000, null=True, blank=True)
    stack_trace = models.TextField(max_length=1000, null=True, blank=True)
    description = models.TextField(max_length=100, help_text="Informative description of the event", null=True,
                                   blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (
            self.event_type, self.description, self.state
        )


class EscalationRule(GenericBaseModel):
    """
    Manages Escalation rules to be applied on events to determine whether they should be escalated or not
    """
    nth_event = models.IntegerField(default=1, help_text="Limit of n events to satisfy this rule")
    duration = models.PositiveIntegerField(
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
    scheduled_for = models.DateTimeField(
        null = True, blank = True, help_text = "Time the scheduled maintenance should begin")
    scheduled_until = models.DateTimeField(
        null = True, blank = True, help_text = "Time the scheduled maintenance should end")
    event_type = models.ForeignKey(EventType, null=True, blank=True)
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
    priority_level = models.IntegerField()
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
    recipient = models.CharField(max_length = 255)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (self.message, self.notification_type, self.state)
