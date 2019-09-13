# -*- coding: utf-8 -*-
"""
The URLs for API endpoints
"""
from django.conf.urls import url

from api.views import report_event

urlpatterns = [
    url(r'^report_event/$', report_event, name = 'report_event'),
]
