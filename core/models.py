# -*- coding: utf-8 -*-
"""
core Models
"""
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """
    Define repeating fields to avoid redefining these in each model
    """
    id = models.UUIDField(max_length=100, default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        abstract = True


class GenericBaseModel(BaseModel):
    """
    Define repeating fields to avoid redefining these in each model
    """
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta):
        abstract = True


class State(GenericBaseModel):
    """
    States for objects lifecycle e.g. "Active"
    """
    def __str__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ('name',)
        unique_together = ('name',)


class NotificationType(GenericBaseModel):
    """
    Types for notifications e.g "sms", "email"
    """
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name


class EscalationLevel(GenericBaseModel):
    """
    Model for managing escalation levels
    """
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name


class IncidentType(GenericBaseModel):
    """
    Model for managing defined incident types e.g "realtime", "scheduled"
    """
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name


def versions():
    """
    returns a collection of salutation titles to chose from
    :return: salutation choices
    @retype tuple
    """
    return ('1', '1.0.0'),


class System(GenericBaseModel):
    """
    model for managing defined system
    """

    health_check_endpoint = models.CharField(max_length=100, help_text='endpoint used in accessing this system')
    credential_endpoint = models.CharField(
        max_length=100, help_text='endpoint used for getting credentials for this system'
    )
    code = models.CharField(max_length = 100, unique=True, db_index=True)
    version = models.CharField(max_length = 5, choices=versions(), default='1')
    admin = models.ForeignKey(User)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s %s %s" % (
            self.name, self.code, self.state, self.credential_endpoint, self.health_check_endpoint
        )


class Interface(GenericBaseModel):
    """
    model for managing defined system interfaces
    """
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (self.name, self.system, self.state)


class SystemCredential(BaseModel):
    """
    model for managing credentials for system users
    """
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s%s%s" % (
            self.username, self.system, self.state
        )


class SystemMonitor(BaseModel):
    """
    model for managing monitoring for my added system
    """
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)
    response_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s %s %s" % (self.system, self.state, self.response_time)


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
        return "%s%s%s%s%s" % (self.first_name, self.last_name, self.email, self.phone_number, self.state)


class SystemRecipient(BaseModel):
    """
    models for managing recipient and a system
    """
    recipient = models.ForeignKey(Recipient)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s%s%s" % (self.recipient, self.system, self.state)


class Event(BaseModel):
    """
    Model for managing events
    """
    interface = models.ForeignKey(Interface)
    system = models.ForeignKey(System)
    escalation_level = models.ForeignKey(EscalationLevel)
    state = models.ForeignKey(State)
    method = models.CharField(max_length=100, help_text="Method where the error is origination from")
    response = models.TextField(max_length=255)
    request = models.TextField(max_length=255)
    code = models.CharField(max_length=100)
    response_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s%s%s" % (
            self.code, self.escalation_level, self.state
        )


class EscalationLevelRecipient(BaseModel):
    escalation_level = models.ForeignKey(EscalationLevel)
    recipient = models.ForeignKey(Recipient)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s%s%s" % (self.escalation_level, self.recipient, self.state)


class Incident(GenericBaseModel):
    """
    Manages Incidents created from escalation points
    """
    incident_type = models.ForeignKey(IncidentType)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s%s%s" % (self.name, self.description, self.state)


class IncidentEvent(BaseModel):
    """
    Represents a ManyToMany association between incidents and events
    """
    incident = models.ForeignKey(Incident)
    event = models.ForeignKey(Event)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s%s%s%s" % (self.incident, self.event, self.state)


class IncidentLog(BaseModel):
    """
    Manages logs of incidences and keeps track of resolution history
    """
    description = models.TextField(max_length=255, blank=True, null=True)
    incident = models.ForeignKey(Incident)
    user = models.ForeignKey(User)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s%s%s" % (
            self.description, self.incident, self.user
        )


class Notification(BaseModel):
    """
    Manages logs of notifications sent out to recipients based on incidents
    """
    message = models.TextField(max_length=255)
    notification_type = models.ForeignKey(NotificationType)
    incident = models.ForeignKey(Incident)
    recipient = models.ForeignKey(Recipient)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s %s" % (self.message, self.notification_type, self.recipient)

