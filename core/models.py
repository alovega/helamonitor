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


class Event(BaseModel):
    interface = models.ForeignKey(Interface)
    system = models.ForeignKey(System)
    escalation_level = models.ForeignKey(EscalationLevel)
    method = models.CharField(max_length=100, help_text="Method where the error is origination from")
    response = models.TextField(max_length=255)
    request = models.TextField(max_length=255)
    code = models.CharField(max_length=100)
    response_time = models.DecimalField(decimal_places=3, max_digits=6)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s%s%s" % (
            self.code, self.escalation_level, self.state
        )


class Incident(GenericBaseModel):
    incident_type = models.ForeignKey(IncidentType)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s%s%s" % (
            self.name, self.incident_type, self.state
        )


class IncidentEvent(BaseModel):
    incident = models.ForeignKey(Incident)
    event = models.ForeignKey(Event)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s%s%s%s" % (
            self.incident, self.event, self.date_created, self.date_modified
        )


class IncidentLog(BaseModel):
    description = models.TextField(max_length=255, blank=True, null=True)
    incident = models.ForeignKey(Incident)
    user = models.ForeignKey(User)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s%s%s%s%s" % (
            self.description, self.incident, self.date_created, self.date_modified, self.user
        )


class Notification(BaseModel):
    message = models.TextField(max_length=255)
    notification_type = models.ForeignKey(NotificationType)
    incident = models.ForeignKey(Incident)
    recipient = models.ForeignKey(Recipient)
    system = models.ForeignKey(System)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s%s%s%s%s" % (
            self.recipient, self.message, self.incident, self.notification_type, self.date_created
        )

