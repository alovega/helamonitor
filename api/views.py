# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.backend.interfaces.event_log import EventLog
from base.backend.utilities import get_request_data

lgr = logging.getLogger(__name__)


@csrf_exempt
def report_event(request):
	"""
	Creates an event reported from an external system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful event creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		event = EventLog().log_event(
			data.get('event_type'), data.get('system'), data.get('interface', None), data.get('response', None),
			data.get('request', None), data.get('code', None), data.get('description', None)
		)
		return JsonResponse(event)
	except Exception as ex:
		lgr.exception("Event logging exception" % ex)
	return JsonResponse({'code': '800.500.001'})
