# -*- coding: utf-8 -*-
"""
The URLs for API endpoints
"""
from django.conf.urls import url

from api.views import report_event, create_incident, update_incident, health_check, get_incident, get_access_token, \
    get_incidents, get_system, create_rule, update_rule, get_rule, get_rules, delete_rule, create_system, \
    update_system, get_systems, delete_system

urlpatterns = [
    url(r'^report_event/$', report_event, name = 'report_event'),
    url(r'^create_incident/$', create_incident, name = 'create_incident'),
    url(r'^update_incident/$', update_incident, name = 'update_incident'),
    url(r'^health_check/$', health_check, name = 'health_check'),
    url(r'^get_incident/$', get_incident, name = 'get_incident'),
    url(r'^get_incidents/$', get_incidents, name = 'get_incidents'),
    url(r'^get_access_token/$', get_access_token, name = 'get_access_token'),
    url(r'^create_rule/$', create_rule, name = 'create_rule'),
    url(r'^update_rule/$', update_rule, name = 'update_rule'),
    url(r'^get_rule/$', get_rule, name = 'get_rule'),
    url(r'^get_rules/$', get_rules, name = 'get_rules'),
    url(r'^delete_rule/$', delete_rule, name = 'delete_rule'),
    url(r'^create_system/$', create_system, name = 'create_system'),
    url(r'^update_system/$', update_system, name = 'update_system'),
    url(r'^get_system/$', get_system, name = 'get_system'),
    url(r'^get_systems/$', get_systems, name = 'get_systems'),
    url(r'^delete_system/$', delete_system, name = 'delete_system'),
]
