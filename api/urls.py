# -*- coding: utf-8 -*-
"""
The URLs for API endpoints
"""
from django.conf.urls import url

from api.views import report_event, create_incident, update_incident, health_check, get_incident, get_access_token, \
    get_incidents, get_systems

urlpatterns = [
    url(r'^report_event/$', report_event, name = 'report_event'),
    url(r'^create_incident/$', create_incident, name = 'create_incident'),
    url(r'^update_incident/$', update_incident, name = 'update_incident'),
    url(r'^health_check/$', health_check, name = 'health_check'),
    url(r'^get_incident/$', get_incident, name = 'get_incident'),
    url(r'^get_incidents/$', get_incidents, name = 'get_incidents'),
    url(r'^get_systems/$', get_systems, name = 'get_systems'),
    url(r'^get_access_token/$', get_access_token, name = 'get_access_token'),
]
