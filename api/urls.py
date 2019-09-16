# -*- coding: utf-8 -*-
"""
The URLs for API endpoints
"""
from django.conf.urls import url

from api.views import report_event, create_incident, update_incident, health_check, send_notification, get_incident

urlpatterns = [
	url(r'^report_event/$', report_event, name = 'report_event'),
	url(r'^create_incident/$', create_incident, name = 'create_incident'),
	url(r'^update_incident/$', update_incident, name = 'update_incident'),
	url(r'^health_check/$', health_check, name = 'health_check'),
	url(r'^send_notification', send_notification, name = 'send_notification'),
	url(r'^get_incident/$', get_incident, name = 'get_incident')
]
