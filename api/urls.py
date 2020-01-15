# -*- coding: utf-8 -*-
"""
The URLs for API endpoints
"""
from django.conf.urls import url

from api.views import report_event, get_events, get_event, get_error_rates, create_incident, update_incident, \
    health_check, dashboard_widgets_data, incidents, incident_events, \
    get_incident, get_access_token, verify_token, get_incidents, get_incident_events, delete_incident, get_system, \
    create_rule, \
    update_rule, get_rule, get_rules, delete_rule, create_system, update_system, get_systems, delete_system, \
    create_user, get_user, delete_user, get_users, create_endpoints, update_endpoint, edit_user, \
    create_recipient, update_recipient, get_endpoint, get_recipient, \
    get_look_up_data, delete_recipient, delete_endpoint, get_notifications, get_logged_in_user_details, \
    get_system_status, edit_logged_in_user_details, get_logged_in_user_recent_notifications, past_incidents, \
    get_logged_in_user_notifications, edit_logged_in_user_password, get_system_recipient, \
    update_system_recipient, create_system_recipient, delete_system_recipient, get_system_response_time_data, \
    endpoint_table_data, recipient_table_data, system_recipient_table_data, event_table_data, active_users, \
    escalation_rules, notification_table_data, PublicEndpoints

urlpatterns = [
    url(r'^report_event/$', report_event, name = 'report_event'),
    url(r'^get_events/$', get_events, name = 'get_events'),
    url(r'^get_event/$', get_event, name = 'get_event'),
    url(r'^get_error_rates/$', get_error_rates, name = 'get_error_rates'),
    url(r'^get_system_status/$', get_system_status, name= 'get_system_status'),
    url(r'^create_incident/$', create_incident, name = 'create_incident'),
    url(r'^create_endpoints/$', create_endpoints, name = 'create_endpoints'),
    url(r'^create_recipient/$', create_recipient, name = 'create_recipient'),
    url(r'^create_system_recipient/$', create_system_recipient, name = 'create_system_recipient'),
    url(r'^update_incident/$', update_incident, name = 'update_incident'),
    url(r'^update_endpoints/$', update_endpoint, name = 'update_endpoint'),
    url(r'^update_recipient/$', update_recipient, name = 'update_recipient'),
    url(r'^health_check/$', health_check, name = 'health_check'),
    url(r'^get_incident/$', get_incident, name = 'get_incident'),
    url(r'^get_incidents/$', get_incidents, name = 'get_incidents'),
    url(r'^past_incidents/$', past_incidents, name = 'past_incidents'),
    url(r'^get_incident_events/$', get_incident_events, name = 'get_incident_events'),
    url(r'^delete_incident/$', delete_incident, name = 'delete_incident'),
    url(r'^get_system_recipient/$', get_system_recipient, name = 'get_system_recipient'),
    url(r'^update_system_recipient/$', update_system_recipient, name = 'update_system_recipient'),
    url(r'^get_incidents/$', get_incidents, name = 'get_incidents'),
    url(r'^get_systems/$', get_systems, name = 'get_systems'),
    url(r'^get_endpoint/$', get_endpoint, name = 'get_endpoint'),
    url(r'^get_endpoints/$', PublicEndpoints.get_endpoints, name = 'get_endpoints'),
    url(r'^get_recipient/$', get_recipient, name = 'get_recipient'),
    url(r'^delete_recipient', delete_recipient, name = 'delete_recipient'),
    url(r'^delete_system_recipient', delete_system_recipient, name = 'delete_system_recipient'),
    url(r'^delete_endpoint', delete_endpoint, name = 'delete_endpoint'),
    url(r'^get_lookup', get_look_up_data, name = 'get_look_up_data'),
    url(r'^get_notifications', get_notifications, name = 'get_notifications'),
    url(r'^get_access_token/$', get_access_token, name = 'get_access_token'),
    url(r'^verify_token/$', verify_token, name = 'verify_token'),
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
    url(r'^get_logged_in_user_details', get_logged_in_user_details, name='get_users'),
    url(r'^edit_logged_in_user', edit_logged_in_user_details, name = 'edit_logged_in_user'),
    url(r'^update_logged_in_user_password', edit_logged_in_user_password, name = 'edit_logged_in_user_password'),
    url(r'^get_logged_in_user_recent_notifications', get_logged_in_user_recent_notifications,
        name = '^get_logged_in_user_recent_notifications'),
    url(r'^get_logged_in_user_notifications', get_logged_in_user_notifications,
        name = '^get_logged_in_user_notifications'),
    url(r'^delete_user/$', delete_user, name = 'delete_user'),
    url(r'^get_users/$', get_users, name = 'get_users'),
    url(r'^edit_user/$', edit_user, name = 'edit_user'),
    url(r'^get_user/$', get_user, name = 'get_user'),
    url(r'^get_response_time_data/$', get_system_response_time_data, name = 'get_response_time_data'),
    url(r'^dashboard_widgets_data/$', dashboard_widgets_data, name = 'dashboard_widgets_data'),
    url(r'^get_endpoints_data/$', endpoint_table_data, name = 'endpoints_table_data'),
    url(r'^get_recipients_data/$', recipient_table_data, name = 'recipient_table_data'),
    url(r'^get_system_recipient_data/$', system_recipient_table_data, name = 'system_recipient_table_data'),
    url(r'^get_notification_data/$', notification_table_data, name = 'notification_table_data'),
    url(r'^events_data/$', event_table_data, name = 'events_data'),
    url(r'^active_users/$', active_users, name = 'active_users'),
    url(r'^escalation_rules/$', escalation_rules, name = 'escalation_rules'),
    url(r'^incidents/$', incidents, name = 'incidents'),
    url(r'^incident_events/$', incident_events, name = 'incident_events'),
    url(r'^get_availability_trend/$', PublicEndpoints.get_availability_trend, name = 'get_availability_trend'),
]
