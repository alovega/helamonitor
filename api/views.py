# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import calendar
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

from api.backend.interfaces.recipient_administration import RecipientAdministrator
from api.models import token_expiry
from api.backend.interfaces.event_log import EventLog
from api.backend.interfaces.incident_administration import IncidentAdministrator
from api.backend.interfaces.endpoint_administration import EndpointAdministrator
from api.backend.interfaces.health_monitor import MonitorInterface
from api.backend.services import OauthService, AppUserService
from api.backend.decorators import ensure_authenticated
from base.backend.utilities import get_request_data, generate_access_token
from base.backend.services import StateService


lgr = logging.getLogger(__name__)


@csrf_exempt
@ensure_authenticated
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
@ensure_authenticated
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
@ensure_authenticated
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
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
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
@ensure_authenticated
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


@csrf_exempt
def get_access_token(request):
	"""
	Generates an access token for valid app users
	@param request:
	@type request: DJANGO WSGIRequest
	@return: An access token and its expiry time or a response code indicating invalid credentials supplied
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		app_user = AppUserService().get(app__id = data.get('client_id'), user__username = data.get('username'))
		if app_user is not None:
			user = check_password(data.get('password'), app_user.user.password)
			if user:
				oauth = OauthService().filter(
					app_user = app_user, expires_at__gt = timezone.now(), state__name = 'Active').first()
				if oauth:
					oauth = OauthService().update(pk = oauth.id, expires_at = token_expiry())
				else:
					oauth = OauthService().create(
						app_user = app_user, token = generate_access_token(), state = StateService().get(name = 'Active')
					)
				if not oauth:
					return JsonResponse({'code': '800.400.001'})
				return JsonResponse({'code': '800.200.001', 'data': {
					'token': str(oauth.token), 'expires_at': calendar.timegm(oauth.expires_at.timetuple())}
				})
		return JsonResponse({'code': '800.403.001'})
	except Exception as ex:
		lgr.exception("Get Access token Exception %s " % ex)
	return JsonResponse({'code': '800.400.001'})


@csrf_exempt
def get_endpoints(request):
	"""
	Get a specific systems endpoints
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: The requested endpoints or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		endpoints = EndpointAdministrator.get_system_endpoints(
			system_id = data.get('system_id')
		)
		return JsonResponse(endpoints)
	except Exception as ex:
		lgr.exception('Endpoint get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
def create_endpoints(request):
	"""
	Creates endpoints from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful endpoint creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		endpoint = EndpointAdministrator.create_endpoint(
			state_id = data.get('state_id'), endpoint_type_id = data.get('endpoint_type_id'),
			system_id = data.get('system_id'), name = data.get('name'), description = data.get('description'),
			endpoint = data.get('endpoint'), response_time = data.get('response_time')
		)
		return JsonResponse(endpoint)
	except Exception as ex:
		lgr.exception('Endpoint creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
def update_endpoint(request):
	"""
	Updates an existing incident's priority, resolution status or user assignment
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful endpoint update or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		updated_endpoint = EndpointAdministrator.update_endpoint(
			endpoint_id = data.get('endpoint_id'), state_id = data.get('state_id'),
			response_time = data.get('response_time'), description = data.get('description'),
			endpoint = data.get('endpoint'), name = data.get('name')
		)
		return JsonResponse(updated_endpoint)
	except Exception as ex:
		lgr.exception('Endpoint update Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
def get_recipients(request):
	"""
	Get a specific systems endpoints
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: The requested recipients or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		recipients = RecipientAdministrator.get_system_recipients(
			system_id = data.get('system_id'), escalation_level_id = data.get('escalation_level_id')
		)
		return JsonResponse(recipients)
	except Exception as ex:
		lgr.exception('Recipient get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
def create_recipient(request):
	"""
	Creates endpoints from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful recipient creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		recipient = RecipientAdministrator.create_recipient(
			state_id = data.get('state_id'), notification_type_id = data.get('notification_type_id'),
			system_id = data.get('system_id'), escalation_level_id = data.get('escalation_level_id'),
			first_name = data.get('first_name'), last_name = data.get('last_name'),
			email = data.get('email'), phone_number = data.get('phone_number'), user_id = data.get('user_id')
		)
		return JsonResponse(recipient)
	except Exception as ex:
		lgr.exception('Recipient creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
def update_recipient(request):
	"""
	Updates an existing incident's priority, resolution status or user assignment
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful recipient update or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		updated_recipient = RecipientAdministrator.update_recipient(
			recipient_id = data.get('recipient_id'), state_id = data.get('state_id'),
			system_recipient_id = data.get('system_recipient_id'), notification_type_id = data.get(
				'notification_type_id'),
			first_name = data.get('first_name'), last_name = data.get('last_name'), email = data.get('email'),
			phone_number = data.get('phone_number')
		)
		return JsonResponse(updated_recipient)
	except Exception as ex:
		lgr.exception('Recipient update Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})
