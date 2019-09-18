# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import calendar
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

from api.backend.interfaces.event_log import EventLog, IncidentAdministrator
from api.backend.interfaces.health_monitor import MonitorInterface
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
		event = EventLog.log_event(
			event_type = data.get('event_type'), system = data.get('system'), interface = data.get('interface'),
			response = data.get('response'), request = data.get('request'), code = data.get('code'),
			description = data.get('description')
		)
		return JsonResponse(event)
	except Exception as ex:
		lgr.exception("Event logging Exception: %s" % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
def create_incident(request):
	"""
	Creates incidents from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful incident creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		incident = IncidentAdministrator.log_incident(
			incident_type = data.get('incident_type'), system = data.get('system'), name = data.get('name'),
			escalation_level = data.get('escalation_level'), description = data.get('description'),
			priority_level = data.get('priority_level'), event_type = data.get('event_type', None),
			state = data.get('state', 'Investigating'), escalated_events = data.get('escalated_events', None),
			scheduled_for = data.get('scheduled_for'), scheduled_until = data.get('scheduled_until')
		)
		return JsonResponse(incident)
	except Exception as ex:
		lgr.exception('Incident creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
def update_incident(request):
	"""
	Updates an existing incident's priority, resolution status or user assignment
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful incident creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		updated_incident = IncidentAdministrator.update_incident(
			incident_id = data.get('incident_id'), escalation_level = data.get('escalation_level'),
			state = data.get('state'), description = data.get('description'), user = data.get('user'),
			priority_level = data.get('priority_level'), name = data.get('name')
		)
		return JsonResponse(updated_incident)
	except Exception as ex:
		lgr.exception('Incident update Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001 %s ' % ex})


@csrf_exempt
def health_check(request):
	"""
	Performs health check for all registered systems
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code of a success/fail and a data containing dictionary containing a list of registered
	system statuses
	@rtype:dict
	"""
	try:
		data = MonitorInterface.perform_health_check()
		return JsonResponse(data)
	except Exception as ex:
		lgr.exception('Health check interface  Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
def get_incident(request):
	"""
	Get a specific incident
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: The requested incident or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		incident = IncidentAdministrator.get_incident(
			system = data.get('system'), incident_id = data.get('incident_id')
		)
		return JsonResponse(incident)
	except Exception as ex:
		lgr.exception('Incident get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


def get_access_token(request):
	"""
	Generates an access token for valid systems or extends the token expiry for those with expired tokens
	@param request:
	@type request: DJANGO WSGIRequest
	@return:
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		app = AppService().get(pk = data.get('client_id'), state__name = 'Active')
		if app is not None:
			app_user = AppUserService().get(app__id = app.id, user__username = data.get('username'))
			user = check_password(data.get('password'), app_user.user.password)
			if app_user is not None and user is not None:
				oauth = OauthService().filter(
					app_user = app_user, expires_at__gt = timezone.now(), state__name = 'Active').first()
				if oauth is None:
					# TODO add token generation logic
					pass
				return {'code': '800.200.001', 'data': {
					'token': str(oauth.token), 'expires_at': calendar.timegm(oauth.expires_at.timetuple())}
				}
			return {'code': '800.400.002'}  # TODO add invalid credentials response code
	except Exception as ex:
		lgr.exception("Get Access token Exception %s " % ex)
	return {'code': '800.400.001'}
