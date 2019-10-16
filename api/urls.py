# -*- coding: utf-8 -*-
"""
The URLs for API endpoints
"""
from django.conf.urls import url

from api.views import report_event, create_incident, update_incident, health_check, get_incident, get_access_token, \
    get_endpoints, create_endpoints, update_endpoint, get_recipients, create_recipient, update_recipient

urlpatterns = [
    url(r'^report_event/$', report_event, name = 'report_event'),
    url(r'^create_incident/$', create_incident, name = 'create_incident'),
    url(r'^create_endpoints/$', create_endpoints, name = 'create_endpoints'),
    url(r'^create_recipients/$', create_recipient, name = 'create_recipient'),
    url(r'^update_incident/$', update_incident, name = 'update_incident'),
    url(r'^update_endpoints/$', update_endpoint, name = 'update_endpoint'),
    url(r'^update_recipient/$', update_recipient, name = 'update_recipient'),
    url(r'^health_check/$', health_check, name = 'health_check'),
    url(r'^get_incident/$', get_incident, name = 'get_incident'),
    url(r'^get_endpoints/$', get_endpoints, name = 'get_endpoints'),
    url(r'^get_recipients/$', get_recipients, name = 'get_recipients'),
    url(r'^get_access_token/$', get_access_token, name = 'get_access_token'),
]
