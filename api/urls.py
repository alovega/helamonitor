# -*- coding: utf-8 -*-
"""
The URLs for API endpoints
"""
from django.conf.urls import url

from api.views import report_event, get_error_rates, create_incident, update_incident, health_check, get_incident, \
    get_access_token, get_incidents, delete_incident, get_system, create_rule, update_rule, get_rule, get_rules, \
    delete_rule, create_system, update_system, get_systems, delete_system, create_user, get_user, get_users, \
    get_endpoints, create_endpoints, update_endpoint, get_recipients, create_recipient, update_recipient, get_recipient, \
    get_endpoint, delete_recipient, delete_endpoint, get_look_up_data, get_notifications

urlpatterns = [
    url(r'^report_event/$', report_event, name = 'report_event'),
    url(r'^get_error_rates/$', get_error_rates, name = 'get_error_rates'),
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
    url(r'^get_incidents/$', get_incidents, name = 'get_incidents'),
    url(r'^get_systems/$', get_systems, name = 'get_systems'),
    url(r'get_endpoint/$', get_endpoint, name = 'get_endpoint'),
    url(r'^get_recipient', get_recipient, name = 'get_recipient'),
    url(r'^delete_recipient', delete_recipient, name = 'delete_recipient'),
    url(r'^delete_endpoint', delete_endpoint, name = 'delete_endpoint'),
    url(r'^get_lookup', get_look_up_data, name = 'get_look_up_data'),
    url(r'^get_notifications', get_notifications, name = 'get_notifications'),
    url(r'^get_incidents/$', get_incidents, name = 'get_incidents'),
    url(r'^delete_incident/$', delete_incident, name = 'delete_incident'),
    url(r'^get_endpoints/$', get_endpoints, name = 'get_endpoints'),
    url(r'^get_recipients/$', get_recipients, name = 'get_recipients'),
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
    url(r'^create_user/$', create_user, name = 'create_user'),
    url(r'^get_user/$', get_user, name = 'get_user'),
    url(r'^get_users/$', get_users, name = 'get_users'),
]
