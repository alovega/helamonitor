# -*- coding: utf-8 -*-
"""
core Models
"""
from __future__ import unicode_literals

import uuid

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


class EndpointType(GenericBaseModel):
    """
    EndpointType model to manage types of endpoints to be used in the system
    """
    is_queried = models.BooleanField(default = False)
    state = models.ForeignKey(State)

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

    class Meta(object):
        ordering = ('name',)
        unique_together = ('name',)


class EscalationLevel(GenericBaseModel):
    """
    Model for managing escalation levels
    """
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ('name',)
        unique_together = ('name',)


class IncidentType(GenericBaseModel):
    """
    Model for managing defined incident types e.g realtime, scheduled
    """
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ('name',)
        unique_together = ('name',)


class EventType(GenericBaseModel):
    """
    Manages types of events e.g error, warning, info, debug
    """
    state = models.ForeignKey(State)

    def priority_level(self):
        """
        Returns the event_type's priority level if used within incident creation
        @return: priority_level
        @rtype: int
        """
        if self.name == "Info":
            return 2
        elif self.name == "Warning":
            return 3
        elif self.name == "Error":
            return 4
        elif self.name == "Critical":
            return 5
        else:
            return 1

    def __str__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ('name',)
        unique_together = ('name',)
