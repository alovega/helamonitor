# -*- coding: utf-8 -*-
"""
The URLs for API endpoints
"""
from django.conf.urls import url

from api.views import report_event, health_check

urlpatterns = [
    url(r'^report_event/$', report_event, name = 'report_event'),
    url(r'^health_check/$', health_check, name = 'monitor_health')
]
